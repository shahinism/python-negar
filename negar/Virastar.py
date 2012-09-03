#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import codecs

class PersianEditor():
    """
    This class includes some functions to standard edit a Persian text
    """    
    def __init__(self, text, *args):
        """
        This is the base part of the class
        """
        self.text = text
        self.fix_dashes = False if 'fix-dashes' in args else True
        self.fix_three_dots = False if 'fix-three-dots' in args else True
        self.fix_english_quotes = False if 'fix-english-quotes' in args else True
        self.fix_hamzeh = False if 'fix-hamzeh' in args else True
        self.hamzeh_with_yeh = False if 'hamzeh-with-yeh' in args else True
        self.cleanup_zwnj = False
        self.fix_spacing_for_braces_and_quotes = False if 'fix-spacing-bq' in args else True
        self.fix_arabic_numbers = False if 'fix-arabic-num' in args else True
        self.fix_english_numbers = False if 'fix-english-num' in args else True
        self.fix_misc_non_persian_chars = False if 'fix-non-persian-chars' in args else True
        self.fix_perfix_spacing = False if 'fix-p-spacing' in args else True
        self.fix_perfix_separate = False if 'fix-p-separate' in args else True
        self.fix_suffix_spacing = False if 'fix-s-spacing' in args else True
        self.fix_suffix_separate = False if 'fix-s-separate' in args else True
        self.aggresive = False if 'aggresive' in args else True
        self.cleanup_kashidas = False if 'cleanup-kashidas' in args else True
        self.cleanup_extra_marks = False if 'cleanup-ex-marks' in args else True
        self.cleanup_spacing = False if 'cleanup-spacing' in args else True
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

        if self.fix_perfix_separate:
            self.fix_perfix_separate_func()
            
        if self.fix_suffix_spacing:
            self.fix_suffix_spacing_func()

        if self.fix_suffix_separate:
            self.fix_suffix_separate_func()
            
        if self.aggresive:
            self.aggresive_func()

        if self.fix_spacing_for_braces_and_quotes:
            self.fix_spacing_for_braces_and_quotes_func()
            
        if self.cleanup_spacing:
            self.cleanup_spacing_func()

        return self.text
        
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

        #Followilng commands will help Negar to avoid change english numbers in strings
        #like 'Text12', 'Text_12' & other string like this
        self.text = re.sub(ur'[a-z\-_]{2,}[۰-۹]+|[۰-۹]+[a-z\-_]{2,}',
                           lambda m:
                           self.char_translator(persian_numbers, english_numbers,  m.group()),
                           self.text)
            
            
    def fix_perfix_spacing_func(self):
        """
        Put zwnj between word and prefix (mi* nemi*)

        there's a possible bug here: می and نمی could separate nouns and not prefix
        """
        # I added some persian punctioation characters to prevent a bug: «می شود» 
        self.text = re.sub(ur"([\s«\(\{])(ن?می)\s+",ur'\1\2‌', self.text)

    def fix_perfix_separate_func(self):
        # I removed punctioations here but I dont know why its work :D
        regex = re.compile(ur"(ن?می)(\S+)")
        
        # This is a little parser that split whole string from spaces and put it to list
        # all lists words will be test one by one and space if need
        list = self.text.split(" ")
        for word in list:
            p = regex.search(word)
            if p:
                # Here I'll check the word wasn't something like میلاد
                if not p.group() in self.dont_touch_list_gen():
                    # This little one was really tricky! regex grouping is really awesome ;-)
                    self.text = re.sub(p.group(), p.group(1) + ur"‌" + p.group(2) , self.text)

    def fix_suffix_spacing_func(self):
        """
        put zwnj between word and suffix (*ha[ye] *tar[in])
        """
        regex = re.compile(ur"""
                           \s+(تر(ی(ن)?)?       # To find matches with 'Tar', 'Tari', 'Tarin'
                           |ها(ی(ی)?)?          # To find matches with 'Ha', 'Haye', 'Hayie'
                           |[تمش]ان             # To find matches with 'man', 'shan', 'tan'
                       )\s+    
                           """, re.VERBOSE)
        
        self.text = re.sub(regex, ur'‌\1 ', self.text)
        
    def fix_suffix_separate_func(self):
        """
        to add virtual space in words with suffix (haye, ...)

        that are not spaced correctly ;-)
        """
        regex = re.compile(ur"""
                           (\S+)
                           (تر(ی(ن)?)?       # *To find matches with 'Tar', 'Tari', 'Tarin'
                           |ها(ی(ی)?)?       # *To find matches with 'Ha', 'Haye', 'Hayie'
                           |[تمش]ان          # *To find matches with 'man', 'shan', 'tan'
                        )                    # *I remove \s+ here because I will split the string
                                             # from spaces
                           """, re.VERBOSE)

        # This is a little parser that split whole string from spaces and put it to list
        # all lists words will be test one by one and space if need
        list = self.text.split(" ")
        for word in list:
            p = regex.search(word)
            if p:
                # Here I'll check the word wasn't something like بهتر
                if not p.group() in self.dont_touch_list_gen():
                    self.text = re.sub(p.group(), p.group(1) + ur"‌" + p.group(2) , self.text)
        
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

    def dont_touch_list_gen(self):
        """
        This function will generate a unicode list from 'data/uniq.txt'

        the file with words like 'بهتر' or 'میلاد' that suffix/perfix function
        dont have to touch theme
        """
#        f = pkgutil.get_data('negar', 'data/untouchable.dat')
        this_dir, this_filename = os.path.split(__file__)
        DATA_PATH = os.path.join(this_dir, "data", "untouchable.dat")
#        print open(DATA_PATH).read()

        f = codecs.open(DATA_PATH, encoding="utf-8")
        self.dont_touch = [] # This is that empty list I used to append words :D
        while True:
            # I had to strip the f.readline() to prevent white spaces
            line = f.readline().strip()
            if len(line) == 0:
                break
            self.dont_touch.append(line)
        return self.dont_touch
        
    def char_translator(self, fromchar, tochar, whichstring):
        """
        This function will translate the 'whichstring' character by character from

        'fromchar' to 'tochar'. in this new function I can return the newstring,
        but I can't check the length of fromchar and tochar! Why? I don't know!
        """
        newstring = whichstring
        for i in range(len(fromchar)):
            newstring = re.sub(fromchar[i], tochar[i], newstring)
        return newstring
        

def add_to_untouchable(word_list):
    this_dir, this_file = os.path.split(__file__)
    DATA_PATH = os.path.join(this_dir, "data", "untouchable.dat")
    f = codecs.open(DATA_PATH, "a", encoding="utf-8")
    for word in word_list:
        f.write(word+"\n")
       # self.dont_touch.append(word)
            
if __name__ == "__main__":
    print "I'm a module. You can't use me directly!\nfor that you can call negar;-)"