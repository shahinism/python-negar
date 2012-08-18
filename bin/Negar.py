#!/usr/bin/python
import sys
import getopt
from   lib.Virastar import PersianEditor

# app data
__author__ 	= "Shahin Azad 'Shahinism' (http://Shahinism.com)"
__version__	= "0.2"
__date__	= "Fri Aug 17 18:40:48 IRDT 2012"

def helpMessage():
    print """
Welcome to Negar Persian editor program
Usage: Negar [OPTIONS] -f [INPUT_FILE] -o [OUTPUT-FILE]

Options:
\t-h, --help                       Display this help and exit
\t-V, --Version                    Print version number and exit
\t-f, --file[=INPUT_FILE_NAME]     Specify [INPUT_FILE]. The file who you want to edit
\t-o, --output[=OUTPUT_FILE_NAME]  Specify [OUT_PUT_FILE]. The file who you want the programs
\t                                 output writes into it. If you don't specify this option
\t                                 Negar will generate an auto file to save the result.
Exit status:
0   if OK,
1   if unknown argumant passed to the Negar.

To get more information visit the website: http://shahinism.github.com/Negar
"""

def main(argv):
    output_file = "Negar_Output"
    try:
        opts, args = getopt.getopt(argv, "hVf:o:", ["help", "file", "output", "Version"])
    except getopt.GetoptError:
        helpMessage()
        sys.exit(1)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            helpMessage()
            sys.exit()
        elif opt in ('-V', '--Version'):
            print "You are using Negar version:"+__version__
            sys.exit()
        elif opt in ('-f', '--file'):
            fileName = arg
        elif opt in ('-o', '--output'):
                output_file = arg
    
    try:
        input_file  = open(fileName)
        output_file = open(output_file, 'w') 
        while True:
            line = unicode(input_file.readline(), encoding='utf-8')
            if len(line) == 0:
                break
            run_PE = PersianEditor(line)
            output_file.write(run_PE.cleanup().encode('utf-8'))
    finally:
        input_file.close()
    
if __name__ == "__main__":
    main(sys.argv[1:])
