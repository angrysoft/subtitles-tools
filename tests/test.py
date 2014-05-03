#!/usr/bin/env python

import sys
sys.path.append('../')
import subconverter

s = subconverter.Subtitles()

def testFile(f):
    """docstring for tesFile"""
    s.loadFromFile(f)
    print('{0} : {1}'.format(f,s.getSubsType()))


testFile('sub.txt')
s.printSub()
testFile('mpl2.txt')
testFile('tmp.txt')
#s.printSub()
#testFile('napisy.srt.txt')
testFile('unknown.txt')

