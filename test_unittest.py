import unittest
from negar.virastar import PersianEditor


class Test(unittest.TestCase):
    # @unittest.skip("")
    def test_trim_leading_trailing_whitespaces(self):
        input_ = "فضا های         خالی     بیش          از       حد"
        output_ = "فضاهای خالی بیش از حد"
        self.assertEqual(f"{PersianEditor(input_)}", output_, 'trim leading trailing whitespaces')

    def test_fix_hamzeh(self):
        input_ = "کلماتی که با 'ی' پسوند همراه هستند مانند 'همه ی ' -- و البته امکان جایگزینی آن با حمزه 'ء' ( در صورت انتخاب کاربر )"
        output_ = "کلماتی که با «ی» پسوند همراه هستند مانند «همه‌ی» – و البته امکان جایگزینی آن با حمزه «ء» (در صورت انتخاب کاربر)"
        self.assertEqual(f"{PersianEditor(input_)}", output_, 'fix hamzeh')

    def test_fix_parantheses(self):
        input_ = "پرانتز ها  یا دیگر علایم ؛ ( نگار )"
        output_ = "پرانتزها یا دیگر علایم؛ (نگار)"
        self.assertEqual(f"{PersianEditor(input_)}", output_, 'fix parantheses')



if __name__ == '__main__':
    unittest.main()
