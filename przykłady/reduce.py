#!/usr/bin/env python
#coding=utf-8

from operator import itemgetter
import sys

#mapa slow
word2count = {}

for line in sys.stdin:

    line = line.strip()

    word, count = line.split('\t', 1)
   
    #konwersja licznika ze stringa na int
    try:
        count = int(count)
        #licznik nie koniecznie musi byc 1
        word2count[word] = word2count.get(word, 0) + count
    except ValueError:
        pass

sorted_word2count = sorted(word2count.items(), key=itemgetter(0))

for word, count in sorted_word2count:
    print '%s\t%s'% (word, count)
