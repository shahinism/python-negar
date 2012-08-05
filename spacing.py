#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

class SpaceCurrector():

    defaultString = unicode('سلام من می خواهم بدانم شما با من دوست می شوید؟ تنها تن‌ها  همه ی ما کنجکاویمها بدانیم!', encoding='utf-8')
    def __init__(self, myString = defaultString):
        self.string = myString
        # This dictionary has wrong spacing as keys and right ones as values.
        self.rightDict = { ' می ':' می‌',
                           ' ها ':'‌ها ',
                           ' ی ':'‌ی '}
        self.makeUnicode()
        self.makeRightSpace()
        self.printCurrectString()



    def makeUnicode(self):
        for find, replace in self.rightDict.items():
            # These lines will make a new key and value in 'UTF-8' encoding
            # to replace with old key and values.
            newFind    = unicode(find, encoding='utf-8')
            newReplace = unicode(replace, encoding='utf-8')
            # In the next two lines I will insert the new key and value to
            # rightDict Dictionary and delete the old key.
            self.rightDict[newFind] = newReplace
            del self.rightDict[find]


    def makeRightSpace(self):
        self.original = self.string
        # This loop will replace all items in the sentence with rightDict dictionaries
        # items. if it find a match, it will replace!
        for find, replace in self.rightDict.items():
            self.string = re.sub(find, replace, self.string)

    def printCurrectString(self):
        print ' ورودی-> ' + self.original.encode('utf-8')
        print ' خروجی-> ' + self.string.encode('utf-8')

        self.splitter()

    def splitter(self):
        wronglist = unicode('تنها', encoding='utf-8')
        string = self.string+' \n'
        while string != '\n':
            endPos = string.find(' ')
            word   = string[:endPos]
            if word != wronglist:
                find = re.compile(unicode('ها$', encoding='utf-8'), re.U)
                replace = u'‌ها '
                word = re.sub(find, replace, word)
            print word.encode('utf-8')
            string = string[endPos+1:]


if __name__ == '__main__':
    print '\n\nI\'m just a leonly class!if you want \nto use me, you have to try my parend :D\nin the next two line, you can see a sample of what I can do:\n\n'
    Class = SpaceCurrector()
