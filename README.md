Negar
======

Negar is a spell corrector for Persian language. I'm working on new algorithm that I found from here:

https://github.com/aziz/virastar/blob/master/lib/virastar.rb

Thank you Aziz.

Screenshot & Features
=====================
You can run gui version like this:

    negar

![Negar's Main Tab](https://github.com/shahinism/python-negar/raw/master/docs/screenshot/maintab.png)
![Negar's Config Tab](https://github.com/shahinism/python-negar/raw/master/docs/screenshot/configtab.png)


Installation
==============

## PyPi

**python-negar** is available on PyPi:

http://pypi.python.org/pypi/python-negar
::

    $ pip install python-negar

## Git

You can get latest stable changes from github server:
::

    $ git clone https://github.com/shahinism/python-negar.git
    $ cd python-negar
    $ python setup.py install

## Zip, Tarball

You can grab the latest tarball.

### *unix

Get the latest tarball & install
::

    $ wget https://github.com/shahinism/python-negar/archive/master.tar.gz
    $ tar xvzf python-negar-master.tar.gz && cd python-negar-master
    $ python setup.py install

### Windows

Download latest zip archive.

https://github.com/shahinism/python-negar/archive/master.zip

Decompress it, and run the following command in root directory of python-negar
::

    $ python setup.py install


#### Requirements 
The main class for text editing just relies on Python's standard library but the GUI part needs `PyICU`, `pyperclip`, and `pyqt6`.
::

    $ pip install PyICu pyperclip pyqt6

Usage
======

Usage without extra args:
::

    from negar.virastar import PersianEditor

    text = "مانند 'همه ی ' که با 'ی' پسوند همراه هستند"
    print(PersianEditor(text)) # Done ;)

Enabling extra features/args:
::

    ##
    args = []
    args.append('fix-english-quotes')
    args.append('cleanup-spacing')
    print(PersianEditor(text, *args))


Full list of args with description:
::

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

