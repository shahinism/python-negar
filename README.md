Negar
=====

Negar trying to be a spell corrector for Persian language. I'm working on new algorithm that I found from here:

https://github.com/aziz/virastar/blob/master/lib/virastar.rb

Thank you Aziz.

It doesn't work completely now. 

How to use
=====

you can use me with a command like this:

    ./Virastar.py [FILE-NAME]/[Argumant]

My arguments are:

    --help : show this message

you can use me more effectively with a command like this:

    ./Virastar.py [FILE-NAME] > output

BUGS
=====

*Line 89-90:
            for i in range(len(bad_chars)):
                text = re.sub(bad_chars[i], good_chars[i], text)

Changed to:
            for i in bad_chars:
                text = re.sub(i, good_chars[bad_chars.index(i)], text)

then "self.fix_misc_non_persian_chars = True" now WORKS :D*

*Line 59:
	Changed! Convert هٔ To ه‌ی
23-09-1391  04:13  Ramin Najjarbashi*
