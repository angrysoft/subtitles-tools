#!/usr/bin/python
# -*- coding: utf-8 -*-
# subconverter.py
# Copyright (C) 2012-2014  Sebastian Zwierzchowski <sebastian.zwierzchowski@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

__author__='Sebastian Zwierzchowski'
__copyright__='Copyright 20012-2014 Sebastian Zwierzchowski'
__license__='GPL2'
__version__='0.2'

import os.path
import getopt
import sys
import re

class DefaultSubsCls:
    """docstring for DefaultSubClass"""
    
    def __init__(self, subs,fps=23.98):
    
        self.subtitle = []
        self.subsInMs =[]
        self.inSubs = []
        self.fps = fps
        
    def setSubsInMs(self,subs):
        """docstring for subsInMs"""
        self.subsInMs = subs[:]
        
    def getSubsInMS(self):
        """docstring for getSubsInMS"""
        return self.subsInMs
    
    def fwdSubs(self,ms):
        """docstring for fwdSubs"""
        pass
        
    def rwdSubs(self,ms):
        """docstring for rwdSubs"""
        pass

# MicroDvd

class MicroDvd(DefaultSubsCls):
    """MicroDVD subtile format"""

    #outfile.writelines('{{{0}}}{{{1}}}{2}'.format(l))

    
    def parseSubtitle(self,subs):
        """docstring for parseSubtitle"""
        del self.subtitle[:]

        for l in subs:
            if l.startswith('{'):
                start,stop,text = l.split('}',2)
                start = start.lstrip('{')
                stop = stop.lstrip('{')
                self.subtitle.append([int(start),int(stop),text])

# Mpl2    

class Mpl2(DefaultSubsCls):
    """Mpl2 subtile format"""
        
    def _timeToMs(self,inTime):
        """docstring for __caclTime"""
        pass
    
    def _timeFromMs(self,inTime):
        """docstring for __timeFromMs"""
        pass
    
    def parseSubtitle(self,subs):
        del self.subtitle[:]
        
        for l in subs:
            if l.startswith('['):
                start,stop,text = l.split(']',2)
                start = start.lstrip('[')
                stop = stop.lstrip('[')
                self.subtitle.append([int(start), int(stop), text])        
                
# TMP   
# SubRip
# Fab
# SubViewer
# WebVTT

class Subtitles:
    
    
    def __init__(self,fps=23.98):
        self.inSub = []
        self.sub = None
        self.subType = ''
    
    def writeToFile(self, out_file_name):
        with open(out_file_name, 'w') as outfile:
            if not self.subtitle == []:
                for l in self.subtitle:
                    outfile.write('\n'.join(self.subtitle))
    
    
    def setSubsType(self,subType):
        """docstring for setSubs"""
        if subType == 'MicroDVD':
            self.subType = subType
            self.sub = MicroDvd(self.inSub).parseSubtitle()
        elif subType == 'Mpl2':
            self.subType = subType
        elif subType == 'TMP':
            self.subType = subType
        elif subType == 'SubRip':
            self.subType = subType
        elif subType == 'Fab':
            self.subType = subType
        elif subType == 'SubViewer':
            self.subType = subType
        elif subType == 'WebVTT':
            self.subType = subType
        elif subType == 'unknown':
            self.subType = subType
            
    def getSubsType(self):
        """docstring for getSubsType"""
        return self.subType
               
    def _detectSubtitleFormat(self):
        """detect subtitle format if 80% of file is a matching"""
        # Mpl2          : txt
        # SubRip        : srt
        # MicoroDVD     : sub
        # Fab           : txt
        # SubViewier    : txt
        # TMP           : txt
        # 
        microDvd = 0
        mpl2 = 0
        tmp = 0
        subRip = 0
        fab = 0
        subViewer = 0
        vtt = 0
        fileLines = len(self.inSub)
        for s in self.inSub:
            if re.search('^\{\d+\}\{\d+\}',s) : microDvd+=1
            elif re.search('^\[\d+\]\[\d+\]',s) : mpl2+=1
            elif re.search('^\d\d:\d\d:\d\d:',s) : tmp+=1
            elif re.search('\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d',s) : subRip+=1
            elif re.search('^\d\d\d\d : \d\d:\d\d:\d\d:\d\d\s+\d\d:\d\d:\d\d:\d\d',s) : fab+=1
            elif re.search('^\d\d:\d\d:\d\d:\d\d,\d\d:\d\d:\d\d:\d\d',s) : subViewer+=1
            elif re.search('\d\d:\d\d.\d\d\d --> \d\d:\d\d.\d\d\d',s) : vtt+=1
        if microDvd >= (fileLines*0.8) : self.setSubsType('MicroDVD')
        elif mpl2 >= (fileLines*0.8) : self.setSubsType('Mpl2')
        elif tmp >= (fileLines*0.8) : self.setSubsType('TMP')
        elif subRip >= (fileLines*0.2) : self.setSubsType('SubRip')
        elif fab >= (fileLines*0.8) : self.setSubsType('Fab')
        elif subViewer >= (fileLines*0.8) : self.setSubsType('SubViewer')
        elif vtt >= (fileLines*0.2) : self.setSubsType('WebVTT')
        else : self.setSubsType('unknown')
    
    def loadFromFile(self,inFileName):
        self.inSub = []
        with open(inFileName,'r') as inFile:
            for l in inFile:
                self.inSub.append(l)
        self._detectSubtitleFormat()
    
    
    def loadFromBuffer(self,buffer):
        """docstring for loadFromBuffer"""
        self.inSub = []
        if type(buffer) == type([]):
            self.inSub = buffer[:]
        self._detectSubtitleFormat()
        
    
    def printSub(self ):
        for l in self.inSub:
            print(l)
            



class Subconverter:
    
    
    def __init__(self,in_file,fps=23.98):
        self.in_file = in_file
        self.out_file = in_file.rsplit('.',1)[0]
        self.out_file +=".sub"
        self.fps = fps
    def convert(self):
        infile = open(self.in_file,'r')
        outfile = open(self.out_file,'w')
        for l in infile.readlines():
            if l.startswith('['):
                #print('debug',l.split(']',2))
                #l = l.strip()
                start,stop,text = l.split(']',2)
                start = start.lstrip('[')
                stop = stop.lstrip('[')
                start = int(int(start)*self.fps/10)
                stop = int(int(stop)*self.fps/10)
                outfile.writelines('{{{0}}}{{{1}}}{2}'.format(start,stop,text))
                #print('{{{0}}}{{{1}}}{2}'.format(start,stop,text))
    

        
def usage():
    print('{0} version : {1}'.format(os.path.basename(sys.argv[0]),__version__))
    print('usage : {0} /path/to/subtitle.txt [-f FPS]'.format(os.path.basename(sys.argv[0])))
    
if __name__ == '__main__':
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "f:", ["fps="])
    except getopt.GetoptError as error:
        print(str(error))
        usage()
        sys.exit(1)
    fps = 23.98
    for o,a in opts:
        if o in ("-f","--fps") :
            fps = float(a)
    for f in args:
        if not os.path.exists(f):
            print("File {0} : not exists".format(f))
            continue
        c = Subconverter(f,fps)
        c.convert()
        del(c)
        
        #s = Mpl2()
        #s.load_from_file(f)
        #s.write_to_file('test.txt')
        #s.print_sub()
        
        