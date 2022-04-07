﻿Negar
======

Negar is an editor(=virastar in Persian) for Persian text. The project is initially inspired by [virastar](https://github.com/aziz/virastar/blob/master/lib/virastar.rb). Thank you [Aziz](https://github.com/aziz) for your great job.

Screenshot & Features
=====================
You can run gui version like this:

    negar

![Negar's Main Tab](https://github.com/shahinism/python-negar/raw/master/docs/screenshot/maintab.png)
![Negar's Config Tab](https://github.com/shahinism/python-negar/raw/master/docs/screenshot/configtab.png)


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

You can grab the latest tarball.

### *nix

Get the latest tarball & install:

    $ wget https://github.com/shahinism/python-negar/archive/master.tar.gz
    $ tar xvzf python-negar-master.tar.gz && cd python-negar-master
    $ python setup.py install

### Windows

Download latest zip archive.

https://github.com/shahinism/python-negar/archive/master.zip

Decompress it, and run the following command in root directory of `python-negar`

    $ python setup.py install

If you coulddn't able to install PyICU, you can download a corresponding whl file from [Unofficial Windows Binaries for Python Extension Packages](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyicu).
For example, the latest version (as of Apr 2022) for your `32-bit` Windows and `Python3.8` version is `PyICU‑2.8.1‑cp38‑cp38‑win32.whl`.

    pip install .\PyICU‑2.8.1‑cp38‑cp38‑win32.whl

#### Requirements
The main class for text editing just relies on Python's standard library but the GUI part needs `PyQt5`, `pyperclip`, and `PyICU`.

    $ pip install PyQt5 PyICU pyperclip

Usage
======

Usage without extra args:

    from negar.virastar import PersianEditor

    text = "مانند 'همه ی ' که با 'ی' پسوند همراه هستند"
    print(PersianEditor(text)) # Done ;)

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

