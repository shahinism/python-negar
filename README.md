Negar
==========
[![PyPI](https://img.shields.io/pypi/v/python-negar)](https://pypi.org/project/python-negar/)
[![repo size](https://img.shields.io/github/repo-size/shahinism/python-negar.svg)](https://github.com/shahinism/python-negar/archive/master.zip)
[![GitHub forks](https://img.shields.io/github/forks/shahinism/python-negar)](https://github.com/shahinism/python-negar/network)
[![GitHub issues](https://img.shields.io/github/issues/shahinism/python-negar)](https://github.com/shahinism/python-negar/issues)
[![GitHub license](https://img.shields.io/github/license/shahinism/python-negar)](https://github.com/shahinism/python-negar/blob/main/LICENSE)
[![Downloads](https://pepy.tech/badge/python-negar)](https://pepy.tech/project/python-negar)
[![Downloads](https://pepy.tech/badge/python-negar/month)](https://pepy.tech/project/python-negar)

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

    test = r"""قابلیت های ویراستار ' نگار  ':
    * جایگزینی
    + خط تیره های پیاپی نظیر (--) و (---) با معادل های استاندارد شان
    + سه نقطه ی پیاپی (...) با کاراکتر استانداردش در زبان فارسی
        + علایمی نظیر کتیشن فارسی با گیومه ؛  'نگار'
        + اعداد عربی '١٢٣٤٥٦٧٨٩٠' و انگلیسی '1234567890'  با معادل فارسی
        + کاراکتر های غیر فارسی نظیر ',;%يةك' با معادل های فارسی

    * تنظیم فاصله
        + کلماتی که با 'ی' پسوند همراه هستند مانند 'همه ی ' -- و البته امکان جایگزینی آن با حمزه 'ء' ( در صورت انتخاب کاربر )
        + پرانتز ها  یا دیگر علایم ؛ ( نگار )
        + علائم نقطه‌گذاری ؛ بدون فاصله از قبل و با یک فاصله از بعد به استثنای اعداد اعشاری مانند 12.4
        + در پیشوند کلمات با نیم‌فاصله نظیر ' می شود '، ' میشود '، ' بی شک '، ' بیشک ' , ' خانه اش '، ' وظیفه شناس ' ، ' کمک تان '  و یا ' نمیرود '
        + در پسوند کلمات با نیم‌فاصله نظیر کتابها، خوشترین -- و البته امکان عدم تنظیم (در صورت انتخاب کاربر)

    * جلوگیری از
        + استفاده ی بیش از یک علامت ؟؟؟؟ یا !!!
        + کشیـــــــــدگـــــــــــــــــی در کــــــــــــلمــــات
        + فضا های         خالی     بیش          از       حد"""

    print(PersianEditor(text))

result:

    قابلیت‌های ویراستار «نگار»:
    * جایگزینی
    + خط تیره‌های پیاپی نظیر (–) و (—) با معادل‌های استانداردشان
    + سه نقطه‌ی پیاپی (…) با کاراکتر استانداردش در زبان فارسی
        + علایمی نظیر کتیشن فارسی با گیومه؛ «نگار»
        + اعداد عربی «۱۲۳۴۵۶۷۸۹۰» و انگلیسی «۱۲۳۴۵۶۷۸۹۰» با معادل فارسی
        + کاراکترهای غیر فارسی نظیر «، ؛ ٪یهک» با معادل‌های فارسی

    * تنظیم فاصله
        + کلماتی که با «ی» پسوند همراه هستند مانند «همه‌ی» – و البته امکان جایگزینی آن با حمزه «ء» (در صورت انتخاب کاربر)
        + پرانتزها یا دیگر علایم؛ (نگار)
        + علائم نقطه‌گذاری؛ بدون فاصله از قبل و با یک فاصله از بعد به استثنای اعداد اعشاری مانند ۱۲.۴
        + در پیشوند کلمات با نیم‌فاصله نظیر «می‌شود»، «می‌شود»، «بی‌شک»، «بی‌شک»، «خانه‌اش»، «وظیفه‌شناس»، «کمک‌تان» و یا «نمی‌رود»
        + در پسوند کلمات با نیم‌فاصله نظیر کتاب‌ها، خوش‌ترین – و البته امکان عدم تنظیم (در صورت انتخاب کاربر)

    * جلوگیری از
        + استفاده‌ی بیش از یک علامت؟ یا!
        + کشیدگی در کلمات
        + فضاهای خالی بیش از حد

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
    --exaggerating_zwnj          Disable suffix separation as much as possible

GUI & CLI
======
There are two companions with this repository to support GUI and CLI, named `negar-gui` and `negar-cli`, respectively.

Both of them are available on PyPI.

* https://pypi.org/project/negar-gui/

* https://pypi.org/project/negar-cli/


## Contributors

<a href="https://github.com/shahinism/python-negar/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=shahinism/python-negar" />
</a>
