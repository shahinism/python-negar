#!/usr/bin/python

import os
import sys
import getopt
import gui
import Virastar
import codecs

__author__ 	= "Shahin Azad 'Shahinism' (http://Shahinism.com)"
__version__     = "0.6"
__date__	= "Fri Aug 17 18:40:48 IRDT 2012"


def helpMessage():
    print """
Welcome to Negar Persian editor program
Usage: Negar [OPTIONS] -f [INPUT_FILE] -o [OUTPUT-FILE]

Options:
   -h, --help                       Display this help and exit
   -V, --Version                    Print version number and exit
   -f, --file[=INPUT_FILE_NAME]     Specify [INPUT_FILE]. The file who you want to edit
   -o, --output[=OUTPUT_FILE_NAME]  Specify [OUT_PUT_FILE]. The file who you want the programs
                                    output writes into it. If you don't specify this option
                                    Negar will generate an auto file to save the result.
       --gui                        Run negars graphical user interface (GUI)
       --fix-dashes                 Disable fix dashes feature
       --fix-three-dots             Disable fix three dots feature
       --fix-english-quotes         Disable fix english quotes feature
       --fix-hamzeh                 Disable fix hamzeh feature
       --hamzeh-with-yeh            Use 'Hamzeh' instead of 'yeh' for fix hamzeh feature
       --fix-spacing-bq             Disable fix spacing braces and qoutes feature
       --fix-arabic-num             Disable fix arabic num feature
       --fix-english-num            Disable fix english num feature
       --fix-non-persian-chars      Disable fix misc non persian chars feature
       --fix-p-spacing              Disable fix perfix spacing feature
       --fix-p-separate             Disable fix perfix separating feature
       --fix-s-spacing              Disable fix suffix spacing feature
       --fix-s-separate             Disable fix suffix separating feature
       --aggresive                  Disable aggresive feature
       --cleanup-kashidas           Disable cleanup kashidas feature
       --cleanup-ex-marks           Disable cleanup extra marks feature
       --cleanup-spacing            Disable cleanup spacing feature
       --add-untouch-list[=FILE]    Add a list of words from 'FILE' to untouchable list.
                                    The list 'fix-s-separate'& 'fix-p-separate' use to add
                                    true spacing
Exit status:
0   if OK,
1   if unknown argumant passed to the Negar.

To get more information visit the website: http://shahinism.github.com/Negar
"""

def main():
    output_file = "Negar_Output"
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hVgf:o:", ["help", "file=", "output=", "Version", "gui", "fix-dashes",
                                                             "fix-three-dots", "fix-english-quotes", "fix-hamzeh",
                                                             "hamzeh-with-yeh", "fix-spacing-bq", "fix-arabic-num",
                                                             "fix-english-num", "fix-non-persian-chars", "fix-p-spacing",
                                                             "fix-p-separate", "fix-s-spacing", "fix-s-separate", "aggresive",
                                                             "cleanup-kashidas", "cleanup-ex-marks", "cleanup-spacing",
                                                             "add-untouch-list="])
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
                sys.exit(0)
            elif opt in ('-V', '--Version'):
                print "You are using Negar version: "+__version__
                sys.exit(0)
            elif opt in ('-f', '--file'):
                fileName = arg
            elif opt in ('-o', '--output'):
                output_file = arg
            elif opt in ('--add-untouch-list'):
                word = []
                if os.path.isfile(arg):
                    try:
                        with codecs.open(arg, encoding="utf-8") as f:
                            while True:
                                line = f.readline()
                                if len(line) == 0:
                                    break
                                word = line.split()
                                Virastar.add_to_untouchable(word)
                    except IOError:
                        print "I can't open the file!"
                else:
                    print "The file you passed to me, isn't actually a file :-("
                exit(0)
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
            run_PE = Virastar.PersianEditor(line, *args)
            output_file.write(run_PE.cleanup().encode('utf-8'))
    finally:
        input_file.close()
    
if __name__ == "__main__":
    main()
