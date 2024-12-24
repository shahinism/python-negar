#!/usr/bin/env python
# ruff: noqa: T201

import enum
import re
import sys
from pathlib import Path

import regex

sys.path.append(
    Path(__file__).parent.parent.as_posix()
)  # https://stackoverflow.com/questions/16981921
from negar.constants import DATAFILE, INFO, URLREGX, USERFILE  # noqa: E402


class State(enum.Enum):
    save = 1
    restore = 2


class PersianEditor:
    """Persian Text Editor for some sanitization task called Virastary in Persian."""

    def __init__(self, text, *args):
        # Check to see if `arg` exists in `args` or not
        parse_args = lambda arg: arg not in args  # noqa: E731
        self._prepositions = (
            "از|در|به|با|بر|برای|بی|درباره|تا|را|جز|بدون|چون|مانند|مثل"
            "|زیر|روی|همراه|مگر|الا|اندر|زی|برت|الا|زی|چو|سوای|پایین"
            "|پشت|پهلوی|پس|پیش|بالای|بیرون|درون|توی|غیر|کنار|مقابل|بهر"
        )
        self.text = text
        self._cleanup_zwnj = False
        # checking for undesired options
        self._aggresive                         = parse_args("aggresive")
        self._fix_hamzeh                        = parse_args("fix-hamzeh")
        self._fix_dashes                        = parse_args("fix-dashes")
        self._fix_three_dots                    = parse_args("fix-three-dots")
        self._hamzeh_with_yeh                   = parse_args("hamzeh-with-yeh")
        self._fix_prefix_spacing                = parse_args("fix-p-spacing")
        self._fix_prefix_separate               = parse_args("fix-p-separate")
        self._fix_suffix_spacing                = parse_args("fix-s-spacing")
        self._fix_suffix_separate               = parse_args("fix-s-separate")
        self._fix_english_quotes                = parse_args("fix-english-quotes")
        self._fix_arabic_numbers                = parse_args("fix-arabic-num")
        self._fix_english_numbers               = parse_args("fix-english-num")
        self._cleanup_spacing                   = parse_args("cleanup-spacing")
        self._cleanup_kashidas                  = parse_args("cleanup-kashidas")
        self._cleanup_extra_marks               = parse_args("cleanup-ex-marks")
        self._exaggerating_zwnj                 = parse_args("exaggerating-zwnj")
        self._fix_misc_non_persian_chars        = parse_args("fix-non-persian-chars")
        self._fix_spacing_for_braces_and_quotes = parse_args("fix-spacing-bq")
        self._trim_leading_trailing_whitespaces = parse_args("trim-lt-whitespaces")

        ImmutableWords()  # to generate the immutable words
        self.cleanup()

    def cleanup(self):
        self._handle_urls(State.save)
        # fix punctuation spaces at first
        # : ; , ! ? and their Persian counterparts should have one space after and no space before
        # An exception is triple dots, which should be handled first
        self.fix_three_dots() if self._fix_three_dots else None
        self.aggressive() if self._aggresive else None
        self.text = re.sub(
            r"[ ‌ ]*([…:;,؛،.؟!]{1})[ ‌ ]*",
            r"\1 ",
            self.text,
        )
        if self._trim_leading_trailing_whitespaces:
            self.text = "\n".join([line.strip() for line in self.text.split("\n")])
        self.fix_dashes()           if self._fix_dashes else None
        self.fix_english_quotes()   if self._fix_english_quotes else None
        self.fix_hamzeh()           if self._fix_hamzeh else None
        self.cleanup_zwnj()         if self._cleanup_zwnj else None
        self.char_validator()       if self._fix_misc_non_persian_chars else None
        self.fix_arabic_numbers()   if self._fix_arabic_numbers else None
        self.fix_english_numbers()  if self._fix_english_numbers else None
        self.fix_prefix_spacing()   if self._fix_prefix_spacing else None
        self.fix_prefix_separate()  if self._fix_prefix_separate else None
        self.fix_suffix_spacing()   if self._fix_suffix_spacing else None
        self.fix_suffix_separate()  if self._fix_suffix_separate else None
        self.fix_spacing_for_braces_and_quotes() \
            if self._fix_spacing_for_braces_and_quotes else None
        self.cleanup_redundant_zwnj()
        self.cleanup_spacing() if self._cleanup_spacing else None
        self.text = re.sub(
            r"…([.؟!])",
            r"… \1",
            self.text,
        )
        if self._trim_leading_trailing_whitespaces:
            self.text = "\n".join([line.strip() for line in self.text.split("\n")])
        self._handle_urls(State.restore)
        return self.text

    def __repr__(self):
        return self.text

    __str__ = __repr__

    def _handle_urls(self, state):
        """Remove URLs and putting them back at the end of the process."""
        if state == State.save:
            self.urls = list(set(re.findall(URLREGX, self.text, re.M | re.I | re.X)))
            self.urls.sort(key=lambda x: len(x), reverse=True)
            for i, url in enumerate(self.urls):
                self.text = regex.sub(rf"{re.escape(url)}", rf"__URL__#{i}__", self.text)
        if state == State.restore:
            for i, url in enumerate(self.urls):
                self.text = re.sub(f"__URL__#{i}__", url, self.text)

    def fix_dashes(self):
        """Replace double and triple dashes with `ndash` and `mdash`, respectively."""
        self.text = re.sub(r"-{3}", r"—", self.text)
        self.text = re.sub(r"-{2}", r"–", self.text)

    def fix_three_dots(self):
        """Replace three dots with an ellipsis."""
        self.text = re.sub(r"\s*\.{3,}(\s)*", r"…\1", self.text)

    def fix_english_quotes(self):
        """Replace English quotes with their Persian counterparts."""
        self.text = re.sub(r"([\"'`]+)(.+?)(\1)", r"«\2»", self.text)

    def fix_hamzeh(self):
        """Replace trailing 'ه ی' with 'هٔ' or 'ه‌ی'.

        --the last one is achievable if hamzeh_with_yeh set.
        """
        if self._hamzeh_with_yeh:
            self.text = re.sub(r"(\S)(ه[\s]+[یي])(\b)", r"\1ه‌ی\3", self.text)
        else:
            self.text = re.sub(r"(\S)(ه[\s]+[یي])(\b)", r"\1هٔ\3", self.text)

    def cleanup_zwnj(self):
        """Remove unnecessary ZWNJ that are succeeded/preceded by a space."""
        self.text = re.sub(r"\s+|\s+", r" ", self.text)

    def cleanup_redundant_zwnj(self):
        """Remove unwanted ZWNJs which are added by some sanitization tasks."""
        self.text = re.sub(r"([ءاأدذرزژوؤ])‌+", r"\1", self.text)
        self.text = re.sub(r"(‌)+", r"\1", self.text)

    def char_validator(self):
        """Replace invalid characters with valid ones."""
        bad_chars = ",;%يةك"
        good_chars = "،؛٪یهک"
        self.text = self.char_translator(bad_chars, good_chars, self.text)

    def fix_arabic_numbers(self):
        """Translate Arabic numbers to their Persian counterparts."""
        persian_numbers = "۱۲۳۴۵۶۷۸۹۰"
        arabic_numbers = "١٢٣٤٥٦٧٨٩٠"
        self.text = self.char_translator(
            arabic_numbers,
            persian_numbers,
            self.text,
        )

    def fix_english_numbers(self):
        """Translate English numbers to their Persian counterparts."""
        persian_numbers = "۱۲۳۴۵۶۷۸۹۰"
        english_numbers = "1234567890"
        self.text = self.char_translator(
            english_numbers,
            persian_numbers,
            self.text,
        )

        # Avoids to change English numbers in strings like 'Text12', 'Text_12', or 'A4'
        self.text = re.sub(
            r"[۰-۹]+[a-zA-Z_]{1,}[۰-۹]+|[a-zA-Z_]{1,}[۰-۹]+|[۰-۹]+[a-zA-Z_]{1,}",
            lambda m: self.char_translator(persian_numbers, english_numbers, m.group()),
            self.text,
        )

    def fix_prefix_spacing(self):
        """Put ZWNJ between a word and its prefix (mi* nemi* bi* na*)."""
        self.text = re.sub(r"\b(بی|نا)‌*(\s+)(?!(می)\b)", r"\1‌", self.text)
        # the following case is for the mi(n.) and nemi(n.)
        self.text = re.sub(rf"\b(ن?می)‌*(\s+)(?!(.|{self._prepositions})\b)", r"\1‌", self.text)

    def fix_prefix_separate(self):
        """Put ZWNJ between a word and its prefix (mi* nemi* bi*)."""
        # regx = re.compile(r"\b(بی|ن?می)‌*([^\[\]\(\)\s]+)") #  \b for words like سهمیه
        regx = regex.compile(
            r"""
        \b(بی|ن?می)‌*
        ([^\[\]\(\)\s]+)
        (?<!های|هایی|ها|شناس|شناسی|گذار|گذاری)\b
        """,
            re.VERBOSE,
        )  #  \b for words like سهمیه

        # Replace backslashes with a temporary placeholder
        text = self.text.replace("\\", "PN__BACKSLASH__PN")
        wlist = text.split(" ")
        for word in wlist:
            regx_iter = regx.finditer(word)
            for p in regx_iter:
                # Checks that the prefix (mi* nemi* bi*) is part a a word or not, like میلاد.
                if p.group() not in ImmutableWords.get():
                    text = re.sub(
                        re.escape(p.group()),
                        p.group(1) + "\u200c" + p.group(2),
                        text,
                    )
        # Restore the original backslashes
        self.text = text.replace("PN__BACKSLASH__PN", "\\")

    def fix_suffix_spacing(self):
        """Put ZWNJ between a word and its suffix (*ha[ye] *tar[in])."""
        regx = re.compile(
            r"""\s+
            (تر(ی(ن)?)?
            |[تمش]ان
            |ا[متش]
            |ا((ی(م|د)?)|ند)
            |ها(ی(ی|ت|م|ش|تان|شان)?)?
            |شناس(ی)?
            |گذار(ی)?|گزار(ی)?
            |مند|ور|پور
            )\b""",
            re.VERBOSE,
        )
        self.text = re.sub(regx, r"‌\1", self.text)

        # Some special cases like و شان خود
        regx = re.compile(r"\b(\w)‌([تمش]ان)\b", re.VERBOSE)
        self.text = re.sub(regx, r"\1 \2", self.text)

        # Ash(=اش) at the end of some words like خانه‌اش or پایانی‌اش
        regx = re.compile(r"\b(\w+)(ه|ی)\s+(اش)\b", re.VERBOSE)
        self.text = re.sub(regx, r"\1\2‌\3", self.text)

    def fix_suffix_separate(self):
        """Put ZWNJ between a word with its suffix (haye, ...)."""
        exag = (
            r"""
            تر(ی(ن)?)?|
            [تمش]ان|
            ها(ی(ی|ت|م|ش|تان|شان)?)?|"""
            if self._exaggerating_zwnj
            else ""
        )
        regx = re.compile(
            rf"""\b(\S+?) # not-greedy fetch to handle some case like هایشان instead شان
            ({exag}
            # تر(ی(ن)?)?
            # [تمش]ان|
            # ها(ی(ی|ت|م|ش|تان|شان)?)?|
            شناس(ی)?|
            گذار(ی)?|گزار(ی)?
            )\b""",
            re.VERBOSE,
        )
        # Replace backslashes with a temporary placeholder
        text = self.text.replace("\\", "PN__BACKSLASH__PN")
        wlist = text.split(" ")
        for word in wlist:
            regx_iter = regx.finditer(word)
            for p in regx_iter:
                # Checks that the suffix (tar* haye*) is part of a word or not, like بهتر.
                if p.group() not in ImmutableWords.get():
                    text = re.sub(
                        re.escape(p.group()),
                        p.group(1) + "\u200c" + p.group(2),
                        text,
                    )
        # Restore the original backslashes
        self.text = text.replace("PN__BACKSLASH__PN", "\\")

    def aggressive(self):
        """Reduce Aggressive Punctuation to one sign."""
        if self._cleanup_extra_marks:
            self.text = re.sub(r"(؟){2,}", r"\1", self.text)
            self.text = re.sub(r"(!){2,}", r"\1", self.text)

        if self._cleanup_kashidas:
            self.text = re.sub(r"ـ+", "", self.text)

    def fix_spacing_for_braces_and_quotes(self):
        """Fix the braces and quotes spacing problems."""
        # ()[]{}""«» should have one space before and no space after (inside)
        for begin, end in zip(["\(", "\[", "\{", '"', "«"], ["\)", "\]", "\}", '"', "»"]):
            self.text = re.sub(
                rf"[ ‌]*({begin})\s*([^{end}]+?)\s*?({end})[ ‌]*", r" \1\2\3 ", self.text
            )
            # self.text = re.sub(rf"^[ ‌]*(.*)[ ‌]*$",
            #     r"\1", self.text, flags=re.MULTILINE)
        # # : ; , ! ? and their Persian counterparts should have one space after and no space before
        self.text = re.sub(
            r"[ ‌ ]*([:;,؛،.؟!]{1})[ ‌ ]*",
            r"\1 ",
            self.text,
        )
        # special case for versioning numbers like 1.2.7
        self.text = re.sub(r"([\d])([.])\s([\d])([.])\s([\d])", r"\1\2\3\4\5", self.text)
        # special case for floating-point numbers like 12.7
        self.text = re.sub(r"([\d])([.])\s([\d])", r"\1\2\3", self.text)
        self.text = re.sub(
            r"[ ‌ ]*((؟\s+!){1})[ ‌ ]*",
            r"؟! ",
            self.text,
        )
        self.text = re.sub(
            r"([۰-۹]+):\s+([۰-۹]+)",
            r"\1:\2",
            self.text,
        )
        self.text = re.sub(
            r"(\d+):\s+(\d+)",
            r"\1:\2",
            self.text,
        )

    def cleanup_spacing(self):
        """Reduce multiple consecutive spaces to one."""
        self.text = re.sub(r"([ \t])+", r" ", self.text)
        # self.text = re.sub(r'([\n]+)[ ‌]', r'\1', self.text)
        self.text = re.sub(r"\n{2,}", r"\n\n", self.text)
        self.text = re.sub(r"[ \t]+(\n|$)", r"\1", self.text, re.MULTILINE)

    @classmethod
    def char_translator(cls, fromchar, tochar, string):
        """Translate the 'string' character by character from 'fromchar' to 'tochar'."""
        newstring = string
        for fc, tc in zip(fromchar, tochar):
            newstring = re.sub(fc, tc, newstring)
        return newstring


class ImmutableWords:
    words = set()  # a set storing all immutable words

    @classmethod
    def __init__(cls):
        USERFILE.mkdir(parents=True, exist_ok=True)
        cls.generate()

    @classmethod
    def get(cls):
        return cls.words

    @classmethod
    def add(cls, word_list):
        with (USERFILE / "immutable.words").open("a", encoding="utf8") as f:
            for word in word_list:
                if word not in cls.words:
                    f.write(word + "\n")
                    cls.words.add(word)

    @classmethod
    def generate(cls):
        """Make a list from immutable words.

        A Unicode list from 'data/immutable.words' and '~/.python-negar/immutable.words'
        containing such words like 'بهتر' or 'میلاد' won't receive any modifications.
        """
        with DATAFILE.open(encoding="utf8") as f:
            for line in f:
                cls.words.add(line.strip())
        try:
            # for compatibility with previous versions, since immutable.words was untouchable.dat before ver 1.2.10
            if (USERFILE / "untouchable.dat").exists():
                (USERFILE / "untouchable.dat").rename(USERFILE / "immutable.words")
            with (USERFILE / "immutable.words").open(encoding="utf8") as f:
                for line in f:
                    cls.words.add(line.strip())
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    print("I'm a module. If you'd like the GUI, use ``negar'' instead. ;-)")

    print(f"""\nUsage:
    from virastar import PersianEditor
    args = []
    # append your desired options
    modifedText = PersianEditor(text, *args))

    e.g.
    text = {INFO}
    print(PersianEditor(text, *['trim-lt-whitespaces']))
    """)
    print(PersianEditor(f"{INFO}", *["trim-lt-whitespaces"]))
