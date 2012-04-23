#!/usr/bin/env python
#coding=utf-8

import string
import sys
a = string.letters
# dane przychodzą z standardowego wejścia
for line in sys.stdin:
    
    # usuniecie z poczatku i konca bialych znaków
    line = line.strip()
    
    # podzielenie linii na słowa
    words = line.split()
    # emity
    for word in words:
        # i wypuszczamy przez stdout
        
	#liczy slowa
	# print '%s\t%s' % (word, 1)
	#liczy slowa zaczynajace sie na kolejne znaki
	# print '%s\t%s' % (word[0], 1)
	#liczy dlugosc konkretnych slow lacznie
	#liczy slowa bez znakow nie bedacych literami
	newword = ""
	for l in word: 
	        for x in a: 
        	        if l == x : newword = newword + l
	
	if len(newword) != 0: print '%s\t%s' % (newword, 1)
