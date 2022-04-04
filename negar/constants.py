from pathlib import Path

__version__ = "1.0.0"

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
* کلماتی که با فاصله ی اشتباه به صورت ' می شود '، ' بی شک '، ' خانه اش ' و یا ' کمک تان ' نوشته شده‌، به صورت درست فاصله گذاری میشوند.
* کلماتی که به اشتباه بدون فاصله به صورت ' میشود '، ' بیشک ' , یا ' نمیرود ' نوشته شده‌، به صورت درست فاصله گذاری میشوند.
* از استفاده ی بیش از یک علامت ؟؟؟؟ یا !!! جلوگیری می کند.
* کلماتی که به صورت کشیـــــــــده نوشته شده اند را به صورت درست می نویسد.
* از فاصله گذاری     بیش از حد    جلوگیری می کند."""

URLREGX = r""" 	#https://gist.github.com/gruber/8891611
(?xi)
\b
(							# Capture 1: entire matched URL
  (?:
    https?|ftp:				# URL protocol and colon
    (?:
      /{1,3}						# 1-3 slashes
      |								#   or
      [a-z0-9%]						# Single letter or digit or '%'
      								# (Trying not to match e.g. "URI::Escape")
    )
    |							#   or
    							# looks like domain name followed by a slash:
    [a-z0-9.\-]+[.]
    (?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj| Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)
    [/?]
  )
  (?:							# One or more:
    [^\s()<>{}\[\]]+						# Run of non-space, non-()<>{}[]
    |								#   or
    \([^\s()]*?\([^\s()]+\)[^\s()]*?\)  # balanced parens, one level deep: (…(…)…)
    |
    \([^\s]+?\)							# balanced parens, non-recursive: (…)
  )+
  (?:							# End with:
    \([^\s()]*?\([^\s()]+\)[^\s()]*?\)  # balanced parens, one level deep: (…(…)…)
    |
    \([^\s]+?\)							# balanced parens, non-recursive: (…)
    |									#   or
    [^\s`!()\[\]{};:'".,<>?«»“”‘’]		# not a space or one of these punct chars
  )
  |					# OR, the following to match naked domains:
  (?:
  	(?<!@)			# not preceded by a @, avoid matching foo@_gmail.com_
    [a-z0-9]+
    (?:[.\-][a-z0-9]+)*
    [.]
    (?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj| Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)
    \b
    /?
    (?!@)			# not succeeded by a @, avoid matching "foo.na" in "foo.na@example.com"
  )
)
"""
