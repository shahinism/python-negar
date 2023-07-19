import unittest
import functools
from negar.virastar import PersianEditor


class Test(unittest.TestCase):
    def _assertEqual(message=""):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                func(self, *args, **kwargs)
                return self.assertEqual(f"{PersianEditor(self.input_)}", self.output_, message)
            return wrapper
        return decorator

    # @unittest.skip("")
    @_assertEqual("Trim Leading Trailing Whitespaces")
    def test_trim_leading_trailing_whitespaces(self):
        self.input_ = "فضا های         خالی     بیش          از       حد"
        self.output_ = "فضاهای خالی بیش از حد"

    @_assertEqual("Fix Hamzeh")
    def test_fix_hamzeh(self):
        self.input_ = "کلماتی که با 'ی' پسوند همراه هستند مانند 'همه ی ' -- و البته امکان جایگزینی آن با حمزه 'ء' ( در صورت انتخاب کاربر )" # noqa: E501
        self.output_ = "کلماتی که با «ی» پسوند همراه هستند مانند «همه‌ی» – و البته امکان جایگزینی آن با حمزه «ء» (در صورت انتخاب کاربر)"     # noqa: E501

    @_assertEqual("Numbers as a Version -- Triple Dots")
    def test_versioning_numbers_triple(self):
        """There is no space between dots of version number!"""
        self.input_ = "نسخه 1.2.4"
        self.output_ = "نسخه ۱.۲.۴"

    @_assertEqual("Numbers as a Version -- Double Dots")
    def test_versioning_numbers_double(self):
        """There is no space between dots of version number!"""
        self.input_ = "نسخه 1.2"
        self.output_ = "نسخه ۱.۲"

    @_assertEqual("Consecutive Dashes")
    def test_consecutive_dashes(self):
        self.input_ = "خط تیره های پیاپی نظیر (--) و (---) با معادل های استاندارد شان"
        self.output_ = "خط تیره‌های پیاپی نظیر (–) و (—) با معادل‌های استانداردشان"

    @_assertEqual("Triple Dots")
    def test_triple_dots(self):
        self.input_ = "سه نقطه ی پیاپی (...) با کاراکتر استانداردش در زبان فارسی"
        self.output_ = "سه نقطه‌ی پیاپی (…) با کاراکتر استانداردش در زبان فارسی"

    @_assertEqual("Persian Quotations")
    def test_persian_quotations(self):
        self.input_ = "علایمی نظیر کتیشن فارسی با گیومه ؛  'نگار'"
        self.output_ = "علایمی نظیر کتیشن فارسی با گیومه؛ «نگار»"

    @_assertEqual("Persian Numbers")
    def test_persian_numbers(self):
        self.input_ = "اعداد عربی '١٢٣٤٥٦٧٨٩٠' و انگلیسی '1234567890'  با معادل فارسی"
        self.output_ = "اعداد عربی «۱۲۳۴۵۶۷۸۹۰» و انگلیسی «۱۲۳۴۵۶۷۸۹۰» با معادل فارسی"

    @_assertEqual("Non-Persian Characters")
    def test_non_persian_characters(self):
        self.input_ = "کاراکتر های غیر فارسی نظیر ',;%يةك' با معادل های فارسی"
        self.output_ = "کاراکترهای غیر فارسی نظیر «، ؛ ٪یهک» با معادل‌های فارسی"

    @_assertEqual("Persian-Yeh as a Kasreh")
    def test_persian_yeh_as_a_kasreh(self):
        self.input_ = "کلماتی که با 'ی' پسوند همراه هستند مانند 'همه ی ' -- و البته امکان جایگزینی آن با حمزه 'ء' ( در صورت انتخاب کاربر )"
        self.output_ = "کلماتی که با «ی» پسوند همراه هستند مانند «همه‌ی» – و البته امکان جایگزینی آن با حمزه «ء» (در صورت انتخاب کاربر)"

    @_assertEqual("Fix Parantheses")
    def test_fix_parantheses(self):
        self.input_ = "پرانتز ها  یا دیگر علایم ؛ ( نگار )"
        self.output_ = "پرانتزها یا دیگر علایم؛ (نگار)"

    @_assertEqual("Fix Punctuations")
    def test_fix_punctuation(self):
        self.input_ = "علائم نقطه‌گذاری ؛ بدون فاصله از قبل و با یک فاصله از بعد به استثنای اعداد اعشاری/نسخه نرم‌افزاری مانند	12.4/1.2.4"
        self.output_ = "علائم نقطه‌گذاری؛ بدون فاصله از قبل و با یک فاصله از بعد به استثنای اعداد اعشاری/نسخه نرم‌افزاری مانند ۱۲.۴/۱.۲.۴"


if __name__ == "__main__":
    unittest.main()
