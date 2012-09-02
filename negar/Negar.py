#!/usr/bin/python
import sys
import getopt
import gui
from   Virastar import PersianEditor

__author__ 	= "Shahin Azad 'Shahinism' (http://Shahinism.com)"
__version__     = "0.6"
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

def main():
    output_file = "Negar_Output"
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hVgf:o:", ["help", "file", "output", "Version", "gui", "fix-dashes",
                                                             "fix-three-dots", "fix-english-quotes", "fix-hamzeh",
                                                             "hamzeh-with-yeh", "fix-spacing-bq", "fix-arabic-num",
                                                             "fix-english-num", "fix-non-persian-chars", "fix-p-spacing",
                                                             "fix-p-separate", "fix-s-spacing", "fix-s-separate", "aggresive",
                                                             "cleanup-kashidas", "cleanup-ex-marks", "cleanup-spacing"])
    except getopt.GetoptError, err:
        print str(err)
        helpMessage()
        sys.exit(1)

    for opt, arg in opts:
        if opt in ('-g', '--gui'):
            print "Gui is running ..."
            gui.main()
            exit(0)
        else:
            if opt in ('-h', '--help'):
                helpMessage()
                sys.exit()
            elif opt in ('-V', '--Version'):
                print "You are using Negar version: "+__version__
                sys.exit()
            elif opt in ('-f', '--file'):
                fileName = arg
            elif opt in ('-o', '--output'):
                output_file = arg
            elif opt in ('--fix-dashes'):
                args.append('fix-dashes')
            elif opt in ('--fix-three-dots'):
                args.append('fix-three-dots')
            elif opt in ('--fix-english-quotes'):
                args.append('fix-english-quotes')
            elif opt in ('--fix-hamzeh'):
                args.append('fix-hamzeh')
            elif opt in ('--hamzeh-with-yeh'):
                args.append('hamzeh-with-yeh')
            elif opt in ('--fix-spacing-bq'):
                args.append('fix-spacing-bq')
            elif opt in ('--fix-arabic-num'):
                args.append('fix-arabic-num')
            elif opt in ('--fix-english-num'):
                args.append('fix-english-num')
            elif opt in ('--fix-non-persian-chars'):
                args.append('fix-non-persian-chars')
            elif opt in ('--fix-p-spacing'):
                args.append('fix-p-spacing')
            elif opt in ('--fix-p-separate'):
                args.append('fix-p-separate')
            elif opt in ('--fix-s-separate'):
                args.append('fix-s-separate')
            elif opt in ('--aggresive'):
                args.append('aggresive')
            elif opt in ('--cleanup-kashidas'):
                args.append('cleanup-kashidas')
            elif opt in ('--cleanup-ex-marks'):
                args.append('cleanup-ex-marks')
            elif opt in ('--cleanup-spacing'):
                args.append('cleanup-spacing')
    
    try:
        input_file  = open(fileName)
        output_file = open(output_file, 'w') 
        while True:
            line = unicode(input_file.readline(), encoding='utf-8')
            if len(line) == 0:
                break
            run_PE = PersianEditor(line, *args)
            output_file.write(run_PE.cleanup().encode('utf-8'))
    finally:
        input_file.close()
    
if __name__ == "__main__":
    main()
