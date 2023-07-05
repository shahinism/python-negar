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
    @_assertEqual('trim leading trailing whitespaces')
    def test_trim_leading_trailing_whitespaces(self):
        self.input_ = "فضا های         خالی     بیش          از       حد"
        self.output_ = "فضاهای خالی بیش از حد"

    @_assertEqual('fix hamzeh')
    def test_fix_hamzeh(self):
        self.input_ = "کلماتی که با 'ی' پسوند همراه هستند مانند 'همه ی ' -- و البته امکان جایگزینی آن با حمزه 'ء' ( در صورت انتخاب کاربر )"
        self.output_ = "کلماتی که با «ی» پسوند همراه هستند مانند «همه‌ی» – و البته امکان جایگزینی آن با حمزه «ء» (در صورت انتخاب کاربر)"

    @_assertEqual('fix parantheses')
    def test_fix_parantheses(self):
        self.input_ = "پرانتز ها  یا دیگر علایم ؛ ( نگار )"
        self.output_ = "پرانتزها یا دیگر علایم؛ (نگار)"

    @_assertEqual('numbers as a version -- triple dots')
    def test_versioning_numbers_triple(self):
        """There is no space between dots of version number!"""
        self.input_ = "نسخه 1.2.4"
        self.output_ = "نسخه ۱.۲.۴"

    @_assertEqual('numbers as a version -- double dots')
    def test_versioning_numbers_double(self):
        """There is no space between dots of version number!"""
        self.input_ = "نسخه 1.2"
        self.output_ = "نسخه ۱.۲"

    @_assertEqual('consecutive dashes')
    def test_consecutive_dashes(self):
        self.input_ = "خط تیره های پیاپی نظیر (--) و (---) با معادل های استاندارد شان"
        self.output_ = "خط تیره‌های پیاپی نظیر (–) و (—) با معادل‌های استانداردشان"

    @_assertEqual('triple dots')
    def test_triple_dots(self):
        self.input_ = "سه نقطه ی پیاپی (...) با کاراکتر استانداردش در زبان فارسی"
        self.output_ = "سه نقطه‌ی پیاپی (…) با کاراکتر استانداردش در زبان فارسی"

    @_assertEqual('Persian quotations')
    def test_persian_quotations(self):
        self.input_ = "علایمی نظیر کتیشن فارسی با گیومه ؛  'نگار'"
        self.output_ = "علایمی نظیر کتیشن فارسی با گیومه؛ «نگار»"


if __name__ == '__main__':
    unittest.main()
