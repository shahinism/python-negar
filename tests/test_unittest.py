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


if __name__ == '__main__':
    unittest.main()
