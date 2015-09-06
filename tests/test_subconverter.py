#!/usr/bin/env python

import sys
sys.path.append('../src/')
import subconverter

s = subconverter.Subtitles()


def testFile(f):
    """docstring for tesFile"""
    s.loadFromFile(f)
    #s.printSub()
    print('{0} : {1}'.format(f, s.getSubsType()))

testFile('sub.txt')
testFile('mpl2.txt')
testFile('tmp.txt')
testFile('srt.txt')
testFile('unknown.txt')

