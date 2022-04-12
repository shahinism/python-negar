Negar
======

Negar is an editor(=virastar in Persian) for Persian text. The project is initially inspired by [virastar](https://github.com/aziz/virastar/blob/master/lib/virastar.rb). Thank you [Aziz](https://github.com/aziz) for your great job.

Installation
==============

## PyPi

**python-negar** is available on [PyPi](http://pypi.python.org/pypi/python-negar):

    $ pip install python-negar

## Git

You can get latest stable changes from github server:

    $ git clone https://github.com/shahinism/python-negar.git
    $ cd python-negar
    $ python setup.py install

## Zip, Tarball

You can download the latest tarball.

### *nix

Get the latest tarball & install:

    $ wget -O python-negar-master.tar.gz https://github.com/shahinism/python-negar/archive/master.tar.gz
    $ tar xvzf python-negar-master.tar.gz && cd python-negar-master
    $ python setup.py install

### Windows

Download latest zip archive.

https://github.com/shahinism/python-negar/archive/master.zip

Decompress it, and run the following command in root directory of `python-negar`

    $ python setup.py install

#### Requirements

    $ pip install regex

Usage
======

Calling by default options:

    from negar.virastar import PersianEditor

    test = r"""نگار قابلیت های زیر را داراست:
    * خط تیره های پیاپی نظیر (--) و (---) را به معادل های استاندارد شان تبدیل می کند.
    * سه نقطه ی پیاپی را (...) به کاراکتر استانداردش در زبان فارسی تبدیل می کند.
    * علایمی نظیر کتیشن فارسی را 'نگار' به گیومه تبدیل می کند.
    * کلماتی مانند 'همه ی ' که با 'ی' پسوند همراه هستند را به صورت درست می‌نویسد و در صورت انتخاب کاربر می‌تواند آن را با حمزه 'ء' جایگزین کند.
    * فاصله گذاری نادرست پرانتز ها نظیر ( نگار ) یا دیگر علایم را به صورت صحیح تنظیم می کند.
    * اعداد عربی مانند '١٢٣٤٥٦٧٨٩٠' و انگلیسی مانند '1234567890' را به معادل فارسی شان تبدیل می کند.
    * کاراکتر های غیر فارسی را شامل ',;%يةك' به معادل های فارسی شان تبدیل می کند.
    * کلماتی که با فاصله ی اشتباه به صورت ' می شود '، ' بی شک '، ' خانه اش '، ' وظیفه شناس ' و یا ' کمک تان ' نوشته شده‌، به صورت درست فاصله گذاری میشوند.
    * کلماتی که به اشتباه بدون فاصله به صورت ' میشود '، ' بیشک ' , یا ' نمیرود ' نوشته شده‌، به صورت درست فاصله گذاری میشوند.
    * از استفاده ی بیش از یک علامت ؟؟؟؟ یا !!! جلوگیری می کند.
    * کلماتی که به صورت کشیـــــــــده نوشته شده اند را به صورت درست می نویسد.
    * از فاصله گذاری     بیش از حد    جلوگیری می کند.
    * علائم نقطه‌گذاری به درستی تنظیم میشوند . بدون فاصله از قبل و با یک فاصله از بعد . استثناء اعداد اعشاری هستند مانند 12.4 که نباید فاصله بگیرد ."""

    print(PersianEditor(text))

result:

    نگار قابلیت‌های زیر را داراست:
    * خط تیره‌های پیاپی نظیر (–) و (—) را به معادل‌های استانداردشان تبدیل می‌کند.
    * سه نقطه‌ی پیاپی را (…) به کاراکتر استانداردش در زبان فارسی تبدیل می‌کند.
    * علایمی نظیر کتیشن فارسی را «نگار» به گیومه تبدیل می‌کند.
    * کلماتی مانند «همه‌ی» که با «ی» پسوند همراه هستند را به صورت درست می‌نویسد و در صورت انتخاب کاربر می‌تواند آن را با حمزه «ء» جایگزین کند.
    * فاصله‌گذاری نادرست پرانتزها نظیر (نگار) یا دیگر علایم را به صورت صحیح تنظیم می‌کند.
    * اعداد عربی مانند «۱۲۳۴۵۶۷۸۹۰» و انگلیسی مانند «۱۲۳۴۵۶۷۸۹۰» را به معادل فارسی‌شان تبدیل می‌کند.
    * کاراکترهای غیر فارسی را شامل «، ؛ ٪یهک» به معادل‌های فارسی‌شان تبدیل می‌کند.
    * کلماتی که با فاصله‌ی اشتباه به صورت «می‌شود»، «بی‌شک»، «خانه‌اش»، «وظیفه‌شناس» و یا «کمک‌تان» نوشته شده، به صورت درست فاصله‌گذاری می‌شوند.
    * کلماتی که به اشتباه بدون فاصله به صورت «می‌شود»، «بی‌شک»، یا «نمی‌رود» نوشته شده، به صورت درست فاصله‌گذاری می‌شوند.
    * از استفاده‌ی بیش از یک علامت؟ یا! جلوگیری می‌کند.
    * کلماتی که به صورت کشیده نوشته شده‌اند را به صورت درست می‌نویسد.
    * از فاصله‌گذاری بیش از حد جلوگیری می‌کند.
    * علائم نقطه‌گذاری به درستی تنظیم می‌شوند. بدون فاصله از قبل و با یک فاصله از بعد. استثناء اعداد اعشاری هستند مانند ۱۲.۴ که نباید فاصله بگیرد.

Enabling extra features/args:

    ##
    args = []
    args.append('fix-english-quotes')
    args.append('cleanup-spacing')
    print(PersianEditor(text, *args))


Full list of args with description:

    --fix-dashes                 Disable fix dashes feature
    --fix-three-dots             Disable fix three dots feature
    --fix-english-quotes         Disable fix english quotes feature
    --fix-hamzeh                 Disable fix hamzeh feature
    --hamzeh-with-yeh            Use 'Hamzeh' instead of 'yeh' for fix hamzeh feature
    --fix-spacing-bq             Disable fix spacing braces and qoutes feature
    --fix-arabic-num             Disable fix arabic num feature
    --fix-english-num            Disable fix english num feature
    --fix-non-persian-chars      Disable fix misc non persian chars feature
    --fix-p-spacing              Disable fix prefix spacing feature
    --fix-p-separate             Disable fix prefix separating feature
    --fix-s-spacing              Disable fix suffix spacing feature
    --fix-s-separate             Disable fix suffix separating feature
    --aggresive                  Disable aggresive feature
    --cleanup-kashidas           Disable cleanup kashidas feature
    --cleanup-ex-marks           Disable cleanup extra marks feature
    --cleanup-spacing            Disable cleanup spacing feature
    --trim-lt-whitespaces        Disable Trim leading trailing whitespaces

GUI & CLI
======
There are two companions with this repository to support GUI and CLI, named `negar-gui` and `negar-cli`, respectively.

Both of them are available on PyPI. 

* https://pypi.org/project/negar-gui/

* https://pypi.org/project/negar-cli/
