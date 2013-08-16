#!/usr/bin/python
# -*- coding: utf-8 -*-
# subconverter.py
# Copyright (C) 2013  Sebastian Zwierzchowski <sebastian.zwierzchowski@gmail.com>
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
__copyright__='Copyright 20012 Sebastian Zwierzchowski'
__license__='GPL2'
__version__='0.1'

import os.path
import getopt
import sys

class Subtitle:
    
    def __init__(self, ):
        self.subtitle = []
    
    def write_to_file(self, out_file_name):
        outfile = open(out_file_name, 'w')
        if not self.subtitle == []:
            for l in self.subtitle:
                outfile.write('\n'.join(self.subtitle))
    
    def print_sub(self ):
        for l in self.subtitle:
            for ll in l:
                if type(ll) == str:
                    sys.stdout.write('{0}'.format(ll))
                else:
                    sys.stdout.write('{0} : '.format(ll))
     
            


class MicroDvd:
    """MicroDVD subtile format"""
    
    def __init__(self):
        self.subtitle = []
        
        
    def write_to_file(self,out_file):
        outfile = open(self.out_file,'w')
        if not self.subtitle == []:
            for l in self.subtitle:
                outfile.writelines('{{{0}}}{{{1}}}{2}'.format(l))
        outfile.close()
        
                
    def load_from_file(self,in_file):
        del self.subtitle[:]
        infile = open(self.in_file,'r')
        for l in infile.readlines():
            if l.startswith('{'):
                start,stop,text = l.split('}',2)
                start = start.lstrip('{')
                stop = stop.lstrip('{')
                self.subtitle.append(int(start),int(stop),text)
    
    
class Mpl2(Subtitle):
    
    def __parse_time(self):
        
    
    def load_from_file(self, in_file_name):
        del self.subtitle[:]
        infile = open(in_file_name,'r')
        for l in infile.readlines():
            if l.startswith('['):
                start,stop,text = l.split(']',2)
                start = start.lstrip('[')
                stop = stop.lstrip('[')
                self.subtitle.append([int(start), int(stop), text])        
    
    
    

    
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
        #c = Subconverter(f,fps)
        #c.convert()
        #del(c)
        
        s = Mpl2()
        s.load_from_file(f)
        #s.write_to_file('test.txt')
        s.print_sub()
        
        