# pylint: disable=too-many-instance-attributes
#!/usr/bin/env python

import re
from pathlib import Path
from constants import DATAFILE, USERFILE

class PersianEditor:
    """
    A class for Persian Text Sanitization
    """
    def __init__(self, text, *args):
        # Check to see if `arg` exists in `args` or not
        is_in_args = lambda arg: arg not in args

        self.text = text
        self.cleanup_zwnj = False
        self.fix_dashes = is_in_args('fix-dashes')
        self.fix_three_dots = is_in_args('fix-three-dots')
        self.fix_hamzeh = is_in_args('fix-hamzeh')
        self.hamzeh_with_yeh = is_in_args('hamzeh-with-yeh')
        self.fix_prefix_spacing = is_in_args('fix-p-spacing')
        self.fix_prefix_separate = is_in_args('fix-p-separate')
        self.fix_suffix_spacing = is_in_args('fix-s-spacing')
        self.fix_suffix_separate = is_in_args('fix-s-separate')
        self.aggresive = is_in_args('aggresive')
        self.cleanup_kashidas = is_in_args('cleanup-kashidas')
        self.fix_english_quotes = is_in_args('fix-english-quotes')
        self.cleanup_extra_marks = is_in_args('cleanup-ex-marks')
        self.cleanup_spacing = is_in_args('cleanup-spacing')
        self.fix_spacing_for_braces_and_quotes = is_in_args('fix-spacing-bq')
        self.fix_arabic_numbers = is_in_args('fix-arabic-num')
        self.fix_english_numbers = is_in_args('fix-english-num')
        self.fix_misc_non_persian_chars = is_in_args('fix-non-persian-chars')

        UnTouchable() # to generate the untouchable words
        self.cleanup()

    def cleanup(self):
        if self.fix_dashes: self.fix_dashes_func()
        if self.fix_three_dots: self.fix_three_dots_func()
        if self.fix_english_quotes: self.fix_english_quotes_func()
        if self.fix_hamzeh: self.fix_hamzeh_func()
        if self.cleanup_zwnj: self.cleanup_zwnj_func()
        if self.fix_misc_non_persian_chars: self.char_validator()
        if self.fix_arabic_numbers: self.fix_arabic_numbers_func()
        if self.fix_english_numbers: self.fix_english_numbers_func()
        if self.fix_prefix_spacing: self.fix_prefix_spacing_func()
        if self.fix_prefix_separate: self.fix_prefix_separate_func()
        if self.fix_suffix_spacing: self.fix_suffix_spacing_func()
        if self.fix_suffix_separate: self.fix_suffix_separate_func()
        if self.aggresive: self.aggresive_func()
        if self.cleanup_spacing: self.cleanup_spacing_func()
        if self.fix_spacing_for_braces_and_quotes:
            self.fix_spacing_for_braces_and_quotes_func()
        self.cleanup_redundant_zwnj()

        return self.text

    def __str__(self):
        return self.text

    __repr__ = __str__

    def fix_dashes_func(self):
        """
        This function will replace double dash to `ndash` and triple dash
        to `mdash`.
        """
        self.text = re.sub(r'-{3}', r'—', self.text)
        self.text = re.sub(r'-{2}', r'–', self.text)

    def fix_three_dots_func(self):
        """
        This function will replace three dots with ellipsis
        """
        self.text = re.sub(r'\s*\.{3,}', r'…', self.text)

    def fix_english_quotes_func(self):
        """
        This function will replace English quotes with their
        persian equivalent
        """
        self.text = re.sub(r"([\"'`]+)(.+?)(\1)", r'«\2»', self.text)

    def fix_hamzeh_func(self):
        """
        This function will replace end of any word which finished with
        'ه ی' with 'هٔ' or 'ه‌ی'(if self.hamzeh_with_yeh == True)
        """
        if self.hamzeh_with_yeh:
            self.text = re.sub(r'(\S)(ه[\s]+[یي])(\b)',r'\1ه‌ی\3',self.text)
        else:
            self.text = re.sub(r'(\S)(ه[\s]+[یي])(\b)',r'\1هٔ\3', self.text)

    def cleanup_zwnj_func(self):
        '''
        This function will remove unnecessary zwnj that are
        succeeded/preceded by a space
        '''
        self.text = re.sub(r'\s+|\s+', r' ', self.text)

    def cleanup_redundant_zwnj(self):
        """
        Some sanitization tasks add some unwanted zwmj which are cleaned by this method
        """
        self.text = re.sub(r'([ءاأدذرزژوؤ])‌+', r'\1', self.text)
        self.text = re.sub(r'(‌)+', r'\1', self.text)

    def char_validator(self):
        """
        This function will change invalid characters to valid ones.
        """
        bad_chars  = ",;%يةك"
        good_chars = "،؛٪یهک"
        self.text = self.char_translator(bad_chars, good_chars, self.text)

    def fix_arabic_numbers_func(self):
        """
        This function will translate Arabic numbers to their
        Persian counterparts.
        """
        persian_numbers = "۱۲۳۴۵۶۷۸۹۰"
        arabic_numbers = "١٢٣٤٥٦٧٨٩٠"
        self.text = self.char_translator(
            arabic_numbers,
            persian_numbers,
            self.text
        )

    def fix_english_numbers_func(self):
        """
        This function will translate English numbers to their
        Persian counterparts.

        It will avoid to do this translation at a English string!
        """
        persian_numbers = "۱۲۳۴۵۶۷۸۹۰"
        english_numbers = "1234567890"
        self.text = self.char_translator(
            english_numbers,
            persian_numbers,
            self.text
        )

        # Followilng commands will help Negar to avoid change english numbers in strings
        # like 'Text12', 'Text_12' & other string like this
        self.text = re.sub(
            r'[a-z\-_]{2,}[۰-۹]+|[۰-۹]+[a-z\-_]{2,}',
            lambda m:
            self.char_translator(persian_numbers, english_numbers, m.group()),
            self.text
        )

    def fix_prefix_spacing_func(self):
        """
        Put zwnj between word and prefix (mi* nemi*)

        there's a possible bug here: می and نمی could separate nouns and not prefix
        """
        # I added some persian punctioation characters
        # to prevent a bug: «می شود»
        self.text = re.sub(r"\b([\s«\(\{]*)(ن?می)\s+",r'\1\2‌', self.text)

    def fix_prefix_separate_func(self):
        """
        """
        # I removed punctioations here but I dont know why its work :D
        regex = re.compile(r"\A(ن?می)(\S+)") #  \A for words like سهمیه

        # This is a little parser that split whole string from spaces
        # and put it to list
        # all lists words will be test one by one and space if need
        wlist = self.text.split(" ")
        for word in wlist:
            p = regex.search(word)
            if p:
                # Here I'll check the word wasn't something like میلاد
                if p.group() not in UnTouchable.words:
                    # This little one was really tricky!
                    # regex grouping is really awesome ;-)
                    self.text = re.sub(
                        p.group(),
                        p.group(1) + r"‌" + p.group(2) ,
                        self.text
                    )

    def fix_suffix_spacing_func(self):
        """
        put zwnj between word and suffix (*ha[ye] *tar[in])
        """
        regex = re.compile(
            r"""\s+
            (تر(ی(ن)?)?
            |ها(ی(ی)?)?
            |[تمش]ان)
            \b""",
            re.VERBOSE
        )
        self.text = re.sub(regex, r'‌\1', self.text)

        # for some cases like و شان خود 
        regex = re.compile(r"\b(\w)‌([تمش]ان)\b", re.VERBOSE)
        self.text = re.sub(regex, r'\1 \2', self.text)

    def fix_suffix_separate_func(self):
        """
        to add virtual space in words with suffix (haye, ...)

        that are not spaced correctly ;-)
        """
        regex = re.compile(
            r"""(\S+)
            (تر(ی(ن)?)?
            |ها(ی(ی)?)?|
            [تمش]ان)\b""",
            re.VERBOSE
        )
        # This is a little parser that split whole string from spaces
        # and put it to list all lists words will be test
        # one by one and space if need
        wlist = self.text.split(" ")
        for word in wlist:
            p = regex.search(word)
            if p:
                # Here I'll check the word wasn't something like بهتر
                if p.group() not in UnTouchable.words:
                    self.text = re.sub(
                        p.group(),
                        p.group(1) + r"‌" + p.group(2) ,
                        self.text
                    )

    def aggresive_func(self):
        """
        Aggressive Editing
        """
        # replace more than one ! or ? mark with just one
        if self.cleanup_extra_marks:
            self.text = re.sub(r'(!){2,}', r'\1', self.text)
            self.text = re.sub(r'(؟){2,}', r'\1', self.text)

        # should remove all kashida
        if self.cleanup_kashidas:
            self.text = re.sub(r'ـ+', "", self.text)

    def fix_spacing_for_braces_and_quotes_func(self):
        """
        This function will fix the braces and quotes spacing problems.
        """
        # ()[]{}""«» should have one space before and one virtual
        # space after (inside)
        self.text = re.sub(
            r'[ ‌]*(\()\s*([^)]+?)\s*?(\))[ ‌]*',
            r' \1‌\2‌\3 ',
            self.text
        )
        self.text = re.sub(
            r'[ ‌]*(\[)\s*([^)]+?)\s*?(\])[ ‌]*',
            r' \1‌\2‌\3 ',
            self.text
        )
        self.text = re.sub(
            r'[ ‌]*(\{)\s*([^)]+?)\s*?(\})[ ‌]*',
            r' \1‌\2‌\3 ',
            self.text
        )
        self.text = re.sub(
            r'[ ‌]*(“)\s*([^)]+?)\s*?(”)[ ‌]*',
            r' \1‌\2‌\3 ',
            self.text
        )
        self.text = re.sub(
            r'[ ‌]*(«)\s*([^)]+?)\s*?(»)[ ‌]*',
            r' \1‌\2‌\3 ',
            self.text
        )
        # : ; , ! ? and their persian equivalents should have one space after
        # and no space before
        self.text = re.sub(
            r'[ ‌ ]*([:;,؛،.؟!]{1})[ ‌ ]*',
            r'‌\1 ',
            self.text
        )
        self.text = re.sub(
            r'([۰-۹]+):\s+([۰-۹]+)',
            r'\1:\2',
            self.text
        )
        # should fix inside spacing for () [] {} "" «»
        self.text = re.sub(
            r'(\()\s*([^)]+?)\s*?(\))',
            r'\1\2\3',
            self.text
        )
        self.text = re.sub(
            r'(\[)\s*([^)]+?)\s*?(\])',
            r'\1\2\3',
            self.text
        )
        self.text = re.sub(
            r'(\{)\s*([^)]+?)\s*?(\})',
            r'\1\2\3',
            self.text
        )
        self.text = re.sub(
            r'(“)\s*([^)]+?)\s*?(”)',
            r'\1\2\3',
            self.text
        )
        self.text = re.sub(
            r'(«)\s*([^)]+?)\s*?(»)',
            r'\1\2\3',
            self.text
        )

    def cleanup_spacing_func(self):
        """
        """
        self.text = re.sub(r'[ ]+', r' ', self.text)
        self.text = re.sub(r'([\n]+)[ ‌]', r'\1', self.text)

    @classmethod
    def char_translator(cls, fromchar, tochar, whichstring):
        """
        This function will translate the 'whichstring' character by character
        from 'fromchar' to 'tochar'. in this new function I can return
        the newstring, but I can't check the length of fromchar and tochar!
        Why? I don't know!
        """
        # TODO: check the length of `fromchar` and `tochar`!
        newstring = whichstring
        for i in range(len(fromchar)):
            newstring = re.sub(fromchar[i], tochar[i], newstring)
        return newstring


class UnTouchable:
    words = set() # a set storing all untouchable words

    @classmethod
    def __init__(cls):
        USERFILE.mkdir(parents=True, exist_ok=True)
        cls.generate()

    @classmethod
    def get(cls):
        return cls.words

    @classmethod
    def add(cls, word_list):
        with (USERFILE/"untouchable.dat").open('a') as f:
            for word in word_list:
                if word not in cls.words:
                    f.write(word+"\n")
                    cls.words.add(word)

    @classmethod
    def generate(cls):
        """
        A Unicode list from 'data/untouchable.dat' and '/home/.python-negar/untouchable.dat'
        containing such words like 'بهتر' or 'میلاد' won't receive any modifications.
        """
        with DATAFILE.open() as f:
            for line in f:
                cls.words.add(line.strip())
        try:
            with (USERFILE/"untouchable.dat").open() as f:
                for line in f:
                    cls.words.add(line.strip())
        except:
            pass

if __name__ == "__main__":
    print( "I'm a module, use ``negar'' instead. ;-)")