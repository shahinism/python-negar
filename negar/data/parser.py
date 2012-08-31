#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

f = open('persian.dic', 'r')
p = open('parse.txt', 'w')

regex = re.compile(ur"""
                   (\s+ن?می[^‌]\S+) # To find [n]?mi perfix
                   |(\S+[^‌][متش]ان) # To find [mtsh]an suffix
                   |(\S+[^‌]تر(ی(ن)?)?) # To find tar(i(n?))? suffix
                   |(\S+[^‌]ها)
                   """, re.VERBOSE)
while True:
    line = unicode(f.readline(), encoding="utf-8")
    if len(line) == 0:
        break
    find = regex.search(line)
    if find:
        p.write(find.group().encode('utf-8')+'\n')
        