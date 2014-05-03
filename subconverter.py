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
          
# TMP   
# SubRip
# Fab
# SubViewer
# WebVTT

class Subtitles:
    
    
    def __init__(self,fps=23.98):
        self.inSub = []
        self.subtitle = []
        self.sub = None
        self.subType = ''
        self.fps = fps
    
    def getFps(self):
        return self.fps
    
    def setFps(self,fps):
        self.fps = fps
        
    def writeToFile(self, out_file_name):
        with open(out_file_name, 'w') as outfile:
            if not self.subtitle == []:
                for l in self.subtitle:
                    outfile.write('\n'.join(self.subtitle))
    
    def frameToMs(self,frame):
        return int(frame / self.fps * 100)
    
    def msToFrame(self,ms):
        return int(ms * self.fps / 100)
    
    def parseMicroDvd(self):
        
        del self.subtitle[:]
        
        for l in self.inSub:
            if l.startswith('{'):
                start,stop,text = l.split('}',2)
                start = start.lstrip('{')
                stop = stop.lstrip('{')
                self.subtitle.append([self.frameToMs(int(start)),self.frameToMs(int(stop)),text])
    
    def parseMpl2(self):
        del self.subtitle[:]
        
        for l in self.inSub:
            if l.startswith('['):
                start,stop,text = l.split(']',2)
                start = start.lstrip('[')
                stop = stop.lstrip('[')
                self.subtitle.append([int(start) * 100, int(stop) * 100, text]) 
    
    def hhmmssToMs(self,h,m,s):
        return(int(h) * 3600 + int(m) * 60 + int(s))* 1000
    
    def msToHhmmss(self,ms):
        sec = ms/1000
        h = sec/3600
        m = (sec - h * 3600)/60
        s = (sec - h * 3600 - m * 60)
        return h,m,s 
       
    def parseTmp(self):
        del self.subtitle[:]
        for l in self.inSub:
            h,m,s,text = l.split(':',3)
            self.subtitle.append([self.hhmmssToMs(h,m,s), self.hhmmssToMs(h, m, int(s)+2),text])
            #sys.stdout.write("{0}:{1}:{2}={3}".format(h,m,s,text))
    def subRipFormatToMs(self,inTime):
        h,m,s = inTime.split(':')
        s,ms = s.split(',')
        return self.hhmmssToMs(h, m, s) + int(ms)
        
    def parseSubRip(self):
        inText = False
        del self.subtitle[:]
        for l in self.inSub:
            if re.search('\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d',l):
                start,stop = re.split(' --> ',l)
                start = start.strip()
                stop = stop.strip()
                print(self.subRipFormatToMs(start),self.subRipFormatToMs(stop))   
    
    def setSubsType(self,subType):
        """docstring for setSubs"""
        if subType == 'MicroDVD':
            self.subType = subType
            self.parseMicroDvd()
        elif subType == 'Mpl2':
            self.subType = subType
            self.parseMpl2()
        elif subType == 'TMP':
            self.subType = subType
            self.parseTmp()
        elif subType == 'SubRip':
            self.subType = subType
            self.parseSubRip()
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
        if sys.version_info[0] == 2:
            self.loadFromFileP2(inFileName)
        elif sys.version_info[0] == 3:
            self.loadFromFileP3(inFileName)
    
    def loadFromFileP2(self,inFileName):
        del self.inSub[:]
        with open(inFileName,'r') as inFile:
            for l in inFile:
                self.inSub.append(l)
        self._detectSubtitleFormat()
    
    def loadFromFileP3(self,inFileName):
        del self.inSub[:]
        with open(inFileName,'r', errors='ignore') as inFile:
            for l in inFile:
                self.inSub.append(l)
        self._detectSubtitleFormat()
        
    def loadFromBuffer(self,buffer):
        """docstring for loadFromBuffer"""
        del self.inSub[:]
        if type(buffer) == type([]):
            self.inSub = buffer[:]
        self._detectSubtitleFormat()
        
    
    def printSub(self ):
        for l in self.subtitle:
            #sys.stdout.write(l)
            print(l)            

        

        