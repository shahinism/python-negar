import unittest
import functools
from unittest import mock
from negar.virastar import ImmutableWords, PersianEditor


# words dropped from data/immutable.words: the suffix/prefix rules alone must leave them intact
NO_LONGER_IMMUTABLE = (
    "آثارتان",
    "آسورتان",
    "اتان",
    "اتومبیل‌تان",
    "اختیارتان",
    "استعدادهایتان",
    "اسم‌تان",
    "اسم‌هایتان",
    "اعتمادتان",
    "اکباتان",
    "الخمیس",
    "انرژی‌درمان",
    "بازوهایتان",
    "باورتان",
    "بتان",
    "بدتان",
    "برنامه‌تان",
    "برنامه‌هایتان",
    "برنامه‌های‌تان",
    "بشناس",
    "بشناسی",
    "بگذار",
    "بگذاری",
    "بمان",
    "بمانی",
    "بها",
    "بهائیت",
    "بهایی",
    "بهاییت",
    "بهمانی",
    "بوتان",
    "بیابان‌ها",
    "بیابان‌های",
    "بیابان‌هایی",
    "بیان‌های",
    "بیانیه‌ها",
    "بیانیه‌های",
    "بیانیه‌هایی",
    "بیت‌التکمه‌ها",
    "بیتل‌ها",
    "بیت‌ها",
    "بیت‌های",
    "بیچاره‌ها",
    "بی‌خود",
    "بی‌درمان",
    "بی‌دست",
    "بیدها",
    "بیراهه‌ها",
    "بیراهه‌های",
    "بیراهه‌هایی",
    "بی‌سامان",
    "بیسکویت‌ها",
    "بی‌سی‌ای",
    "بیشه‌زارهای",
    "بیشه‌های",
    "بیضه‌ها",
    "بیغوله‌های",
    "بیگانه‌دوست‌ها",
    "بیگانه‌ها",
    "بی‌گذشت",
    "بیمارستان‌ها",
    "بیمارستان‌های",
    "بیماری‌ها",
    "بیماری‌های",
    "بیماری‌هایی",
    "بیم‌ها",
    "بیمه‌نامه‌های",
    "بیمه‌ها",
    "بیمه‌های",
    "بینش‌ها",
    "بینش‌های",
    "بینش‌هایی",
    "بیننده‌های",
    "بی‌نیش",
    "بیولوژیست‌های",
    "بیوم‌ها",
    "پاسخ‌هایتان",
    "پسرتان",
    "پندارتان",
    "پیامبرتان",
    "پیرتان",
    "پیشکسوتان",
    "پیش‌کسوتان",
    "تابلوهایتان",
    "تازه‌تان",
    "تلویزیون‌تان",
    "تنهایی‌ها",
    "تنهایی‌های",
    "تنهایی‌هایی",
    "چشمان‌تان",
    "چشمان‌شان",
    "چشمان‌مان",
    "خنده‌درمان",
    "داستان‌راستان",
    "رفتاردرمان",
    "رویاهایتان",
    "شتان",
    "شتر",
    "شتری",
    "شهادت",
    "غیرمحترمان",
    "فتان",
    "فیزیوتر",
    "قهرمان",
    "کارآگاها",
    "کارتری",
    "کتان",
    "کشان",
    "گفتاردرمان",
    "ماتریس",
    "متان",
    "متر",
    "متری",
    "مها",
    "میانجی‌گری‌های",
    "میانگین‌های",
    "میانه‌روهای",
    "میانوندها",
    "میثاق‌های",
    "میخچه‌ها",
    "میخ‌ها",
    "میخ‌های",
    "میدان‌ها",
    "میدان‌های",
    "میراب‌ها",
    "میراث‌های",
    "میرزاسالاری‌ها",
    "میرها",
    "میرهای",
    "میزان‌های",
    "میزبان‌های",
    "میزبانی‌ها",
    "میزگردها",
    "میزگردهای",
    "میزهای",
    "میکاشیت‌ها",
    "میکرب‌شناس",
    "میکرب‌شناسی",
    "میکروارگانیسم‌هایی",
    "میکروب‌شناس",
    "میکروب‌شناسی",
    "میکروب‌ها",
    "میکروب‌های",
    "میکروسکوپ‌ها",
    "میکروسکوپ‌های",
    "میکروفن‌ها",
    "میکروفون‌ها",
    "میگرن‌ها",
    "میل‌اژدها",
    "میله‌ستون‌ها",
    "میله‌ها",
    "میله‌های",
    "میلیاردها",
    "میلیون‌ها",
    "میم‌ها",
    "میمون‌ها",
    "میمونی‌ها",
    "مین‌گذاری",
    "مین‌ها",
    "مین‌های",
    "مین‌هایی",
    "مین‌یاب‌های",
    "مینیاتورها",
    "مینیاتورهای",
    "مینی‌بوس‌ها",
    "مینی‌بوس‌های",
    "میهمانی‌ها",
    "میهمانی‌های",
    "میوه‌ها",
    "میوه‌های",
    "میوه‌هایی",
    "نایب‌قهرمان",
    "نشان",
    "نشاند",
    "نشاندن",
    "نشاندند",
    "نشانده",
    "نشاندی",
    "نشاندیم",
    "نهاد",
    "نهایت",
    "نهایی",
    "همان",
    "همان‌ها",
    "همانی",
    "یادتان",
    "عمان",
    "کمان",
    "بی‌اساید",
    "ببخشای",
    "آبخازستان",
    "آبونمان",
    "آپارتمان",
    "آپارتمانتان",
    "آتشفشان",
    "آتش‌فشان",
    "آتش‌نشان",
    "آدمکشان",
    "آدم‌کشان",
    "آزادمنشان",
    "آژیرکشان",
    "آستان",
    "آسمان",
    "آقامنشان",
    "آلمان",
    "آمدنتان",
    "ابروکمان",
    "ادب‌دوستان",
    "ادبستان",
    "ارباب‌منشان",
    "اردستان",
    "ارمنستان",
    "ازبکستان",
    "استان",
    "اشراف‌منشان",
    "اطرافتان",
    "اطرافیانتان",
    "اطلاعاتتان",
    "اعمالتان",
    "افتان",
    "افشان",
    "افغانستان",
    "اگزیستان",
    "الشان",
    "الماس‌نشان",
    "المان",
    "امنیتتان",
    "انسان‌دوستان",
    "انقلابتان",
    "انگشتان",
    "انگلستان",
    "انگلشتان",
    "اهریمن‌صفتان",
    "بازستان",
    "باستان",
    "باشغیرستان",
    "باغستان",
    "بالنگستان",
    "باهنگستان",
    "بت‌پرستان",
    "بخستان",
    "بدبختان",
    "بدخشان",
    "بدگمان",
    "بدنتان",
    "بذرافشان",
    "براستان",
    "بربرستان",
    "برخاستتان",
    "برده‌صفتان",
    "بزرگ‌منشان",
    "بستان",
    "بشردوستان",
    "بغستان",
    "بکشان",
    "بلغارستان",
    "بلوچستان",
    "بنگستان",
    "بهارستان",
    "بودنتان",
    "بوستان",
    "بی‌خانمان",
    "بی‌رحمان",
    "بی‌گمان",
    "بی‌نشان",
    "پارلمان",
    "پاکستان",
    "پانسمان",
    "پخشان",
    "پرتوافشان",
    "پرسمان",
    "پروتستان",
    "پستان",
    "پسمان",
    "پوستتان",
    "پول‌پرستان",
    "پولتان",
    "پیش‌دبستان",
    "تابستان",
    "تاتارستان",
    "تاجیکستان",
    "تاسمان",
    "تاکستان",
    "تجربیاتتان",
    "تحتان",
    "تخم‌افشان",
    "ترجمان",
    "تردستان",
    "ترکستان",
    "ترکمان",
    "ترکمنستان",
    "تریستان",
    "تعریفتان",
    "تفتان",
    "تکلیفتان",
    "تلاشتان",
    "تماستان",
    "تنگدستان",
    "تنگستان",
    "تنوره‌کشان",
    "تهیدستان",
    "توتستان",
    "تیره‌بختان",
    "تیمارستان",
    "جان‌افشان",
    "جانبختان",
    "جان‌فشان",
    "جسمان",
    "جنت‌نشان",
    "جنّت‌نشان",
    "جواهرنشان",
    "جوهرافشان",
    "جیغ‌کشان",
    "چپ‌دستان",
    "چچستان",
    "چشمانتان",
    "چشمانشان",
    "چشمانمان",
    "چنارستان",
    "چیستان",
    "حاکمان",
    "حرفتان",
    "حسابتان",
    "حصیرستان",
    "خاطرنشان",
    "خانمان",
    "خداپرستان",
    "خصمان",
    "خلجستان",
    "خمیازه‌کشان",
    "خودپرستان",
    "خورشیدپرستان",
    "خوزستان",
    "خوشبختان",
    "خوشتان",
    "خوش‌گمان",
    "خون‌فشان",
    "خیزان‌-‌افتان",
    "دادستان",
    "داستان",
    "داغستان",
    "دامن‌افشان",
    "دامن‌کشان",
    "دانه‌افشان",
    "دبستان",
    "دبیرستان",
    "دپارتمان",
    "ددمنشان",
    "درافشان",
    "درختان",
    "درخشان",
    "درفشان",
    "دست‌افشان",
    "دستان",
    "دست‌نشان",
    "دشتستان",
    "دنیاپرستان",
    "دهستان",
    "دوزیستان",
    "دوستان",
    "دیلمان",
    "دیلمستان",
    "راجستان",
    "رحمان",
    "رخشان",
    "رفیع‌الشان",
    "رنگین‌پوستان",
    "رنگین‌کمان",
    "روبه‌صفتان",
    "روستان",
    "ریسمان",
    "ریگستان",
    "زابلستان",
    "زاولستان",
    "زبردستان",
    "زرافشان",
    "زرفشان",
    "زرنشان",
    "زمستان",
    "زوزه‌کشان",
    "ساختمان",
    "سجستان",
    "سخت‌پوستان",
    "سرانگشتان",
    "سرپرستان",
    "سرخ‌پوستان",
    "سرسختان",
    "سرگین‌غلتان",
    "سروستان",
    "سفیدپوستان",
    "سکستان",
    "سلمان",
    "سنبلستان",
    "سنگستان",
    "سیاهپوستان",
    "سیاه‌پوستان",
    "سیستان",
    "سینمادوستان",
    "شاعرصفتان",
    "شبستان",
    "شعردوستان",
    "شکرافشان",
    "شکرستان",
    "شکرفشان",
    "شهرستان",
    "شورستان",
    "صربستان",
    "صفیرکشان",
    "طاق‌بستان",
    "طاقستان",
    "طبرستان",
    "طخارستان",
    "ظالمان",
    "عالمان",
    "عثمان",
    "عربستان",
    "عطرافشان",
    "عطشان",
    "عظیم‌الشان",
    "عنبرافشان",
    "غرجستان",
    "غزلستان",
    "غلتان",
    "غیراستان",
    "فرنگستان",
    "فرهنگ‌دوستان",
    "فرهنگستان",
    "فرودستان",
    "فرونشان",
    "قبرستان",
    "قراقستان",
    "قرقیزستان",
    "قزاقستان",
    "قلم‌بدستان",
    "قلم‌به‌دستان",
    "قلیان‌کشان",
    "قهستان",
    "کارستان",
    "کاه‌منشان",
    "کتمان",
    "کردستان",
    "کشان‌کشان",
    "کهکشان",
    "کوته‌دستان",
    "کوچکتان",
    "کودکستان",
    "کوهستان",
    "گرجستان",
    "گردافشان",
    "گرده‌افشان",
    "گفتمان",
    "گل‌افشان",
    "گلستان",
    "گهرافشان",
    "گوانتان",
    "گورستان",
    "گوهرافشان",
    "لارستان",
    "ﻻرستان",
    "لرستان",
    "لقمان",
    "لهستان",
    "لیموعمان",
    "متکلمان",
    "مجارستان",
    "مرکاپتان",
    "مستان",
    "مسلمان",
    "مشتان",
    "مشک‌افشان",
    "معلمان",
    "مغولستان",
    "منجمان",
    "منشان",
    "مهاجمان",
    "مهستان",
    "می‌کشان",
    "نارنجستان",
    "نامسلمان",
    "نخلستان",
    "نژادپرستان",
    "نعره‌کشان",
    "نعمان",
    "نکشان",
    "نگارستان",
    "نهالستان",
    "نودولتان",
    "نورافشان",
    "نوع‌دوستان",
    "نیرنگستان",
    "نیستان",
    "هزاردستان",
    "هستان",
    "هفت‌آسمان",
    "هگمتان",
    "هم‌داستان",
    "همدستان",
    "هندوستان",
    "هنردوستان",
    "هنرستان",
    "هوجستان",
    "والامنشان",
    "وجه‌الضمان",
    "ورزش‌دوستان",
    "وطن‌پرستان",
    "ولی‌نعمتان",
    "یادداشتتان",
    "یاقوت‌نشان",
    "راستان",
    "همداستان",
    "پرستان",
    "موکشان",
)


class Test(unittest.TestCase):
    @staticmethod
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
        self.input_ = "کلماتی که با 'ی' پسوند همراه هستند مانند 'همه ی ' -- و البته امکان جایگزینی آن با حمزه 'ء' ( در صورت انتخاب کاربر )"  # noqa: E501
        self.output_ = "کلماتی که با «ی» پسوند همراه هستند مانند «همه‌ی» – و البته امکان جایگزینی آن با حمزه «ء» (در صورت انتخاب کاربر)"  # noqa: E501

    @_assertEqual("Fix Hamzeh -- word starting with a diacritized ی")
    def test_fix_hamzeh_diacritic(self):
        self.input_ = "کــه یَــزدان زِ نــاچــیــز چــیــز آفــریــد"
        self.output_ = "که یَزدان زِ ناچیز چیز آفرید"

    @_assertEqual("Suffix -- no های after ٔ or a repeated های")
    def test_suffix_after_hamzeh_and_repeated_hay(self):
        self.input_ = "گریهٔ های های"
        self.output_ = "گریهٔ های های"

    @_assertEqual("Suffix -- no lone letter left after a prefix ZWNJ")
    def test_suffix_no_lone_letter_after_prefix(self):
        self.input_ = "بینهایت بیندت"
        self.output_ = "بی‌نهایت بیندت"

    @_assertEqual("Suffix -- never joins a one-letter word")
    def test_suffix_not_after_one_letter_word(self):
        self.input_ = "سـبـو شـکـسـته و تر کرده جامه چندین بار"
        self.output_ = "سبو شکسته و تر کرده جامه چندین بار"

    @_assertEqual("Numbers as a Version -- Triple Dots")
    def test_versioning_numbers_triple(self):
        """There is no space between dots of version number!."""
        self.input_ = "نسخه 1.2.4"
        self.output_ = "نسخه ۱.۲.۴"

    @_assertEqual("Numbers as a Version -- Double Dots")
    def test_versioning_numbers_double(self):
        """There is no space between dots of version number!."""
        self.input_ = "نسخه 1.2"
        self.output_ = "نسخه ۱.۲"

    @_assertEqual("Consecutive Dashes")
    def test_consecutive_dashes(self):
        self.input_ = "خط تیره های پیاپی نظیر (--) و (---) با معادل های استاندارد شان"
        self.output_ = "خط تیره‌های پیاپی نظیر (–) و (—) با معادل‌های استانداردشان"

    @_assertEqual("Triple Dots I")
    def test_triple_dots_i(self):
        self.input_ = "سه نقطه ی پیاپی (...) با کاراکتر استانداردش در زبان فارسی"
        self.output_ = "سه نقطه‌ی پیاپی (…) با کاراکتر استانداردش در زبان فارسی"

    @_assertEqual("Triple Dots II")
    def test_triple_dots_ii(self):
        self.input_ = "پرتره ، طبیعت و غیره یا پرتره ، طبیعت و  .... ؟"
        self.output_ = "پرتره، طبیعت و غیره یا پرتره، طبیعت و… ؟"

    @_assertEqual("Persian Quotations I")
    def test_persian_quotations_i(self):
        self.input_ = "علایمی نظیر کتیشن فارسی با گیومه ؛  'نگار'"
        self.output_ = "علایمی نظیر کتیشن فارسی با گیومه؛ «نگار»"

    @_assertEqual("Persian Quotations II")
    def test_persian_quotations_ii(self):
        self.input_ = "«تاثیر نسبی داشته است. »"
        self.output_ = "«تاثیر نسبی داشته است.»"

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

    @_assertEqual("Fix Prefix ZWNJ")
    def test_fix_prefix_ZWNJ(self):
        self.input_ = r"در پیشوند کلمات با نیم‌فاصله نظیر ' می شود '، ' میشود '، ' بی شک '، ' بیشک ' , ' خانه اش '، ' وظیفه شناس ' ، ' کمک تان '  و یا ' نمیرود '"
        self.output_ = "در پیشوند کلمات با نیم‌فاصله نظیر «می‌شود»، «می‌شود»، «بی‌شک»، «بی‌شک»، «خانه‌اش»، «وظیفه‌شناس»، «کمک‌تان» و یا «نمی‌رود»"

    @_assertEqual("Fix Prefix ZWNJ II")
    def test_fix_prefix_ZWNJ_ii(self):
        self.input_ = r"می‌ شود"
        self.output_ = "می‌شود"

    @_assertEqual("Fix Prefix ZWNJ III")
    def test_fix_prefix_ZWNJ_iii(self):
        self.input_ = r"می ‌شود"
        self.output_ = "می‌شود"

    @_assertEqual("Fix Prefix ZWNJ -- می as wine stays a word")
    def test_fix_prefix_mi_wine(self):
        self.input_ = "ساقیا جام می\nبیار که جام می لعل و می ناب خوش است، می خور و می ده تا او می رود"
        self.output_ = "ساقیا جام می\nبیار که جام می لعل و می ناب خوش است، می خور و می ده تا او می‌رود"

    @_assertEqual("Fix Prefix ZWNJ -- می before a non-verb (پی)")
    def test_fix_prefix_mi_wine_pey(self):
        self.input_ = "چنانم ده می پی در پی عشق"
        self.output_ = "چنانم ده می پی در پی عشق"

    @_assertEqual("Fix Prefix ZWNJ -- no prefix after a diacritic inside a word")
    def test_fix_prefix_after_diacritic(self):
        self.input_ = "موسِمی عجب و موسِبیکار"
        self.output_ = "موسِمی عجب و موسِبیکار"

    @_assertEqual("Fix Prefix ZWNJ -- می as wine after a preposition or before an adjective+ی")
    def test_fix_prefix_mi_wine_prep(self):
        self.input_ = "به می عمارتِ دل کن، می لعلی که می خورم، زآن می سرمست، بهایِ می اکنون، این می رود"
        self.output_ = "به می عمارتِ دل کن، می لعلی که می‌خورم، زآن می سرمست، بهایِ می اکنون، این می‌رود"

    @_assertEqual("Immutable head keeps its attached tail")
    def test_immutable_head(self):
        self.input_ = "بیهُده‌گوست و بیداری‌ست و میان‌موی و میازار و بیارید"
        self.output_ = "بیهُده‌گوست و بیداری‌ست و میان‌موی و میازار و بیارید"

    @_assertEqual("Fix Suffix ZWNJ -- ور after ی is a word")
    def test_fix_suffix_var_after_yeh(self):
        self.input_ = "خوشدلی ور دانش ور، یارِ ما ور نی، جان ور نه"
        self.output_ = "خوشدلی ور دانش‌ور، یارِ ما ور نی، جان ور نه"

    @_assertEqual("Fix Suffix ZWNJ I")
    def test_fix_suffix_ZWNJ_I(self):
        self.input_ = r"در پسوند کلمات با نیم‌فاصله نظیر کتابها، خوشترین -- و البته امکان عدم تنظیم (در صورت انتخاب کاربر)"
        self.output_ = "در پسوند کلمات با نیم‌فاصله نظیر کتاب‌ها، خوش‌ترین – و البته امکان عدم تنظیم (در صورت انتخاب کاربر)"

    @_assertEqual("Fix Redundant Glyphs")
    def test_cleanup_redundant_glyphs(self):
        self.input_ = "استفاده ی بیش از یک علامت ؟؟؟؟ یا !!!"
        self.output_ = "استفاده‌ی بیش از یک علامت؟ یا!"

    @_assertEqual("Cleanup Kashidas")
    def test_cleanup_kashidas(self):
        self.input_ = "کشیـــــــــدگـــــــــــــــــی در کــــــــــــلمــــات"
        self.output_ = "کشیدگی در کلمات"

    @_assertEqual("Cleanup Extra Spaces")
    def test_cleanup_extra_spaces(self):
        self.input_ = "فضا های         خالی     بیش          از       حد"
        self.output_ = "فضاهای خالی بیش از حد"

    @_assertEqual("Immutable Words I")
    def test_immutable_words_i(self):
        self.input_ = "تنها ترین خدمتگزار (تنها ترین خدمتگزار)"
        self.output_ = "تنهاترین خدمتگزار (تنهاترین خدمتگزار)"

    @_assertEqual("Immutable Words II")
    def test_immutable_words_ii(self):
        self.input_ = "تنها ترین خدمتگزار (تنها ترین خدمتگزار)"
        self.output_ = "تنهاترین خدمتگزار (تنهاترین خدمتگزار)"

    @_assertEqual("Immutable Word Mirad")
    def test_immutable_word_mirad(self):
        self.input_ = "میرد\u200c میرداد میرد"
        self.output_ = "میرد میرداد میرد"

    @_assertEqual("Immutable Word Vanagozari")
    def test_immutable_word_vanagozari(self):
        # وا+نگذاری (negative of واگذاری), not وان+گذاری
        self.input_ = "کنون سزد که به خلقم ز خویش وانگذاری وانگذار"
        self.output_ = "کنون سزد که به خلقم ز خویش وانگذاری وانگذار"

    @_assertEqual("Immutable Word Biarayi")
    def test_immutable_word_biarayi(self):
        self.input_ = "بیارایی بیارای"
        self.output_ = "بیارایی بیارای"

    @_assertEqual("Immutable Word Farmayeshan")
    def test_immutable_word_farmayeshan(self):
        self.input_ = "فرمایشان"
        self.output_ = "فرمایشان"

    @_assertEqual("Suffix With Diacritics")
    def test_suffix_with_diacritics(self):
        self.input_ = "غم ایّام"
        self.output_ = "غم ایّام"

    @_assertEqual("Suffix With Diacritics")
    def test_suffix_with_diacritics_ii(self):
        self.input_ = "غمِ ایّام"
        self.output_ = "غمِ ایّام"

    @_assertEqual("Immutable Word With Diacritics")
    def test_immutable_word_with_diacritics(self):
        self.input_ = "بیمِ جان بُستان"
        self.output_ = "بیمِ جان بُستان"

    @_assertEqual("Arabic Word Before Plural Suffix")
    def test_arabic_word_before_plural_suffix(self):
        self.input_ = "ناوِلْها اَهْمِلْها بُستان"
        self.output_ = "ناوِلْها اَهْمِلْها بُستان"

    @_assertEqual("Immutable Boundary Words")
    def test_immutable_boundary_words(self):
        # words that look like prefix/suffix + stem (بی/می/ها/ستان ...) but must stay untouched
        self.input_ = "کمان بی‌اساید همدستان همداستان میارید بیضا بیهده گستری پرستان بینم بینی موکشان ببخشای میان میانت بیاساید بیضاء بیضایی بیضائی میاری بینند"
        self.output_ = self.input_

    @_assertEqual("Fix Suffix ZWNJ II")
    def test_fix_suffix_ZWNJ_II(self):
        self.input_ = "بیستم ماه میلادی"
        self.output_ = "بیستم ماه میلادی"

    @_assertEqual("Ignore Comment")
    def test_ignore_comment(self):
        self.input_ = "کشیـــــــــده  شده اند #> می نویسد  .... "
        self.output_ = "کشیده شده‌اند #> می نویسد  .... "

    @_assertEqual("mix_parentheses_suffix")
    def test_mix_parentheses_suffix(self):
        self.input_ = '"دختر تنهایی "   ( کهتر بمان )'
        self.output_ = "«دختر تنهایی» (کهتر بمان)"

    @_assertEqual("unchanged")
    def test_unchanged(self):
        self.input_ = "نشان‌دهنده همان‌طور"
        self.output_ = "نشان‌دهنده همان‌طور"

    @_assertEqual("single-letter stem is never split off")
    def test_no_lone_letter_before_suffix(self):
        self.input_ = "مگذار بتر کشان"
        self.output_ = "مگذار بتر کشان"

    @_assertEqual("single-letter remainder is never split after prefix")
    def test_no_lone_letter_after_prefix(self):
        self.input_ = "نمیر نمیرود"
        self.output_ = "نمیر نمی\u200cرود"

    def test_formerly_immutable_words_stay_unchanged(self):
        # an empty immutable list proves the rules, not the list, protect these words
        with mock.patch.object(ImmutableWords, "words", set()), mock.patch.object(ImmutableWords, "generate"):
            for args in ((), ("exaggerating-zwnj",)):
                for word in NO_LONGER_IMMUTABLE:
                    with self.subTest(word=word, args=args):
                        self.assertEqual(f"{PersianEditor(word, *args)}", word)

    @_assertEqual("pronoun endings stay attached after joining letters (ADR-0001)")
    def test_pronoun_endings_stay_attached(self):
        self.input_ = "بیخشان بخشان کشان کتابشان خانه‌شان خانهشان"
        self.output_ = "بیخشان بخشان کشان کتابشان خانه‌شان خانه‌شان"

    @_assertEqual("Nokare/copula ai after silent heh")
    def test_ai_nokare(self):
        self.input_ = "خانه ای دیدم و تو خسته ای. کتاب‌خانه ای دل‌انگیز و پرده ای گل‌دار"
        self.output_ = "خانه‌ای دیدم و تو خسته‌ای. کتاب‌خانه‌ای دل‌انگیز و پرده‌ای گل‌دار"

    @_assertEqual("Vocative ai stays separate")
    def test_ai_vocative(self):
        self.input_ = "بــگــو ایــنــجــایــگـه ای جـان ودلـدار\nگفتا که ای دوست\nدل ای یار، خانه، ای ماه\nبنده\nای خدا\n«که ای دوست» شاه ای پسر خانه ای جان!"
        self.output_ = "بگو اینجایگه ای جان ودلدار\nگفتا که ای دوست\nدل ای یار، خانه، ای ماه\nبنده\nای خدا\n«که ای دوست» شاه ای پسر خانه ای جان!"

    def test_ai_context_cues(self):
        # want: True = ای joins (indefinite/copula), False = stays separate (vocative / no cue in verse)
        cases = {
            # prose: a period marks the line as prose, so even cue-less cases join
            "دیروز نامه ای نوشتم و خانه ای بزرگ خریدم.": True,
            "این مقاله ای جامع است.": True,
            "او دیده ای مهربان دارد.": True,
            # cues that rule out a vocative (verse-like short lines)
            "یک خانه ای بزرگ": True,              # determiner before
            "تو خسته ای": True,                   # line end
            "کجا رفته ای؟": True,                 # punctuation
            "رفته ای  بیا که": True,              # hemistich gap
            "خانه ای که دیدم": True,              # function word
            "چه پروانه ای چون شمع": True,         # determiner / function word
            "نامه ای می‌نویسم": True,             # verb
            "خانه ای دارد": True,
            # vocative cues
            "دیده ای مهربان من": False,
            "خسته ای مهربان!": False,
            "اینجایگه ای جان": False,
            "گفتا که ای دوست": False,
            # no cue in a verse-like line: keep the user's spacing
            "دیده ای مهربان بگو": False,
            "رفته ای مهربان  دل ما را بردی": False,
        }
        for text, want in cases.items():
            with self.subTest(text=text):
                self.assertEqual("\u200cای" in f"{PersianEditor(text)}", want)

if __name__ == "__main__":
    unittest.main()
