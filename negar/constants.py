from pathlib import Path

__version__ = "0.9.0"

LOGO = (Path(__file__).parent.absolute()/"logo.png").as_posix()
DATAFILE = Path(__file__).parent.absolute()/"data/untouchable.dat"
USERFILE = Path.home()/".python-negar"

INFO="""نگار قابلیت های زیر را داراست:
* خط تیره های پیاپی نظیر (--) و (---) را به معادل های استاندارد شان تبدیل می کند.
* سه نقطه ی پیاپی را (...) به کاراکتر استانداردش در زبان فارسی تبدیل می کند.
* علایمی نظیر کتیشن فارسی را 'نگار' به گیومه تبدیل می کند.
* کلماتی مانند 'همه ی ' که با 'ی' پسوند همراه هستند را به صورت درست می‌نویسد و در صورت انتخاب کاربر می‌تواند آن را با حمزه 'ء' جایگزین کند.
* فاصله گذاری نادرست پرانتز ها نظیر ( نگار ) یا دیگر علایم را به صورت صحیح تنظیم می کند.
* اعداد عربی مانند '١٢٣٤٥٦٧٨٩٠' و انگلیسی مانند '1234567890' را به معادل فارسی شان تبدیل می کند.
* کاراکتر های غیر فارسی را شامل ',;%يةك' به معادل های فارسی شان تبدیل می کند.
* کلماتی که با فاصله ی اشتباه به صورت ' می شود ' و یا ' کمک تان ' نوشته شده‌، به صورت درست فاصله گذاری میشوند.
* کلماتی که به اشتباه بدون فاصله به صورت ' میشود ' , یا ' کمکتان ' نوشته شده‌، به صورت درست فاصله گذاری میشوند.
* از استفاده ی بیش از یک علامت ؟؟؟؟ یا !!! جلوگیری می کند.
* کلماتی که به صورت کشیـــــــــده نوشته شده اند را به صورت درست می نویسد.
* از فاصله گذاری     بیش از حد    جلوگیری می کند.
"""