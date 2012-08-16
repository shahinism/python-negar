#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys

class PersianEditor():
    """
    This class includes some functions to standard edit a Persian text
    """
    
    def __init__(self, text):
        """
        This is the base part of the class
        """
        self.text = text
        self.fix_dashes = True
        self.fix_three_dots = True
        self.fix_english_quotes = True
        self.fix_hamzeh = True
        self.hamzeh_with_yeh = True
        self.cleanup_zwnj = False
        self.fix_spacing_for_braces_and_quotes = True
        self.fix_arabic_numbers = True
        self.fix_english_numbers = True
        self.fix_misc_non_persian_chars = True
        self.fix_perfix_spacing = True
        self.fix_suffix_spacing = True
        self.aggresive = True
        self.cleanup_kashidas = True
        self.cleanup_extra_marks = True
        self.cleanup_spacing = True
        self.cleanup()

    def cleanup(self):
        """
        This is the main function who call other functions if need!
        """
        if self.fix_dashes:
            self.fix_dashes_func()

        if self.fix_three_dots:
            self.fix_three_dots_func()

        if self.fix_english_quotes:
            self.fix_english_quotes_func()

        if self.fix_hamzeh:
            self.fix_hamzeh_func()

        if self.cleanup_zwnj:
            self.cleanup_zwnj_func()

        if self.fix_misc_non_persian_chars:
            self.char_validator()

        if self.fix_arabic_numbers:
            self.fix_arabic_numbers_func()

        if self.fix_english_numbers:
            self.fix_english_numbers_func()

        if self.fix_perfix_spacing:
            self.fix_perfix_spacing_func()
            
        if self.fix_suffix_spacing:
            self.fix_suffix_spacing_func()

        if self.aggresive:
            self.aggresive_func()

        if self.fix_spacing_for_braces_and_quotes:
            self.fix_spacing_for_braces_and_quotes_func()

        if self.cleanup_spacing:
            self.cleanup_spacing_func()

        print self.text.encode('utf-8'),
        
    def fix_dashes_func(self):
        """
        This function will replace double dash to ndash and triple dash to mdash
        """
        self.text = re.sub(ur'-{3}', ur'—', self.text)
        self.text = re.sub(ur'-{2}', ur'–', self.text)

    def fix_three_dots_func(self):
        """
        This function will replace three dots with ellipsis
        """
        self.text = re.sub(ur'\s*\.{3,}', ur'…', self.text)

    def fix_english_quotes_func(self):
        """
        This function will replace English quotes with their persian equivalent
        """
        self.text = re.sub(ur"([\"'`]+)(.+?)(\1)", ur'«\2»', self.text)

    def fix_hamzeh_func(self):
        """
        This function will replace end of any word which finished with 'ه ی' with
        'هٔ' or 'ه‌ی'(if self.hamzeh_with_yeh == True)
        """
        if self.hamzeh_with_yeh:
            self.text = re.sub(ur'(\S)(ه[\s]+[یي])(\s)',ur'\1ه‌ی\3', self.text)
        else:
            self.text = re.sub(ur'(\S)(ه[\s]+[یي])(\s)',ur'\1هٔ\3', self.text)

    def cleanup_zwnj_func(self):
        '''
        This function will remove unnecessary zwnj that are succeeded/preceded by a space
        '''
        self.text = re.sub(ur'\s+|\s+', ur' ', self.text)

    def char_validator(self):
        """
        This function will change invalid characters to validate ones.

        it uses char_translator function to do it.
        """
        bad_chars  = u",;%يةك"
        good_chars = u"،؛٪یهک"
        self.text = self.char_translator(bad_chars, good_chars, self.text)

    def fix_arabic_numbers_func(self):
        """
        This function will translate Arabic numbers to their Persian equivalants.

        it uses char_translator function to do it.
        """
        persian_numbers = u"۱۲۳۴۵۶۷۸۹۰"
        arabic_numbers = u"١٢٣٤٥٦٧٨٩٠"
        self.text = self.char_translator(arabic_numbers, persian_numbers, self.text)

    def fix_english_numbers_func(self):
        """
        This function will translate English numbers to their Persian equivalants.

        it will avoid to do this translation at a English string!
        it uses char_translator function to do it.
        """
        persian_numbers = u"۱۲۳۴۵۶۷۸۹۰"
        english_numbers = u"1234567890"
        self.text = self.char_translator(english_numbers, persian_numbers, self.text)

#        self.text = re.sub(ur'[a-z\-_]{2,}[۰-۹]+|[۰-۹]+[a-z\-_]{2,}',
#                           lambda m:
#                           self.char_translator(persian_numbers, english_numbers,  m.group()),
#                           self.text)
            
            
    def fix_perfix_spacing_func(self):
        """
        Put zwnj between word and prefix (mi* nemi*)

        there's a possible bug here: می and نمی could separate nouns and not prefix
        """
        self.text = re.sub(ur"\s+(ن?می)\s+",ur' \1‌', self.text)

    def fix_suffix_spacing_func(self):
        self.text = re.sub(ur'\s+(تر(ی(ن)?)?|ها(ی)?)\s+', ur'‌\1 ', self.text)

    def aggresive_func(self):
        """
        Aggressive Editing
        """
        # replace more than one ! or ? mark with just one
        if self.cleanup_extra_marks:
            self.text = re.sub(ur'(!){2,}', ur'\1', self.text)
            self.text = re.sub(ur'(؟){2,}', ur'\1', self.text)
            
        # should remove all kashida
        if self.cleanup_kashidas:
            self.text = re.sub(ur'ـ+', "", self.text)
        
    def fix_spacing_for_braces_and_quotes_func(self):
        """
        This function will fix the braces and quotes spacing problems.
        """
        # ()[]{}""«» should have one space before and one virtual space after (inside)
        self.text = re.sub(ur'[ ‌]*(\()\s*([^)]+?)\s*?(\))[ ‌]*', ur' \1‌\2‌\3 ', self.text)
        self.text = re.sub(ur'[ ‌]*(\[)\s*([^)]+?)\s*?(\])[ ‌]*', ur' \1‌\2‌\3 ', self.text)
        self.text = re.sub(ur'[ ‌]*(\{)\s*([^)]+?)\s*?(\})[ ‌]*', ur' \1‌\2‌\3 ', self.text)
        self.text = re.sub(ur'[ ‌]*(“)\s*([^)]+?)\s*?(”)[ ‌]*', ur' \1‌\2‌\3 ', self.text)
        self.text = re.sub(ur'[ ‌]*(«)\s*([^)]+?)\s*?(»)[ ‌]*', ur' \1‌\2‌\3 ', self.text)
        # : ; , ! ? and their persian equivalents should have one space after and no space before
        self.text = re.sub(ur'[ ‌ ]*([:;,؛،.؟!]{1})[ ‌ ]*',ur'‌\1 ', self.text)
        self.text = re.sub(ur'([۰-۹]+):\s+([۰-۹]+)', ur'\1:\2', self.text)
        # should fix inside spacing for () [] {} "" «»
        self.text = re.sub(ur'(\()\s*([^)]+?)\s*?(\))', ur'\1\2\3', self.text)
        self.text = re.sub(ur'(\[)\s*([^)]+?)\s*?(\])', ur'\1\2\3', self.text)
        self.text = re.sub(ur'(\{)\s*([^)]+?)\s*?(\})', ur'\1\2\3', self.text)
        self.text = re.sub(ur'(“)\s*([^)]+?)\s*?(”)', ur'\1\2\3', self.text)
        self.text = re.sub(ur'(«)\s*([^)]+?)\s*?(»)', ur'\1\2\3', self.text)
            
    def cleanup_spacing_func(self):
        self.text = re.sub(ur'[ ]+', ur' ', self.text)
        self.text = re.sub(ur'([\n]+)[ ‌]', ur'\1', self.text)


    def char_translator(self, fromchar, tochar, whichstring):
        """
        This function will translate the 'whichstring' character by character from

        'fromchar' to 'tochar'. My old function is writed after this. in this new
        function I can return the newstring, but I can't check the length of fromchar
        and tochar! Why? I don't know!
        """
        newstring = self.text
        for i in range(len(fromchar)):
            newstring = re.sub(fromchar[i], tochar[i], newstring)
        return newstring
#    def char_translator(self, fromchar, tochar):
#        if len(fromchar) == len(tochar):
#            for i in range(len(fromchar)):
#                self.text = re.sub(fromchar[i], tochar[i], self.text)
#        else:
#            raise "in function char_translator fromchar and to char doesn't have same length'"
        
        
def helpMessage():
    print """Hi, I'm negars virastar!
you can use me with a command like this:
./Virastar.py [FILE-NAME]/[Argumant]
My Argumants are:
\t\t--help : show this message
\n\n\n
you can use me more effectively with a command like this:
\t\t$./Virastar.py FILE-NAME > OutPut\n"""
        
if __name__ == "__main__":
    if len(sys.argv) < 2:
        helpMessage()
        sys.exit()
    if sys.argv[1].startswith('--'):
        option = sys.argv[1][2:]
        if option == 'help':
            helpMessage()
    else:
        try:
            fileName = sys.argv[1]
            file = open(fileName)
            while True:
                line = unicode( file.readline(), encoding='utf-8')
                if len(line) == 0:
                    break
                    #print line
                run2 = PersianEditor(line)
        finally:
            file.close()