Negar
=====

Negar trying to be a spell corrector for Persian language. I'm working on new algorithm that I found from here:

https://github.com/aziz/virastar/blob/master/lib/virastar.rb

Thank you Aziz.

It doesn't work completely now. 

How to install
=====

First of all depend on you Distribution/Operation System install Pythons ‘setuptools’. 
In some Linux distribution its name is something like ‘pysetuptools’. 

After that execute commands:

    $ git clone https://github.com/shahinism/Negar.git
    $ cd Negar
    $ sudo python setup.py install

For now there is no requirements except Pythons standard library.

How to use
=====

you can use me with a command like this:

    $ Negar.py [ARGUMENTS] -f [INPUT_FILENAME] -o [OUTPUT_FILENAME]

My arguments are:

    -h, --help                       Display this help and exit
    -V, --Version                    Print version number and exit
    -f, --file[=INPUT_FILE_NAME]     Specify [INPUT_FILE]. The file who you want to edit
    -o, --output[=OUTPUT_FILE_NAME]  Specify [OUT_PUT_FILE]. The file who you want the programs
                                     output writes into it. If you don't specify this option
                                     Negar will generate an auto file to save the result.

