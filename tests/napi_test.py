#!/usr/bin/env python

import sys
import os
from threading import Thread
sys.path.append('../src/')
import napi
#from subtitlestools import napi

def get_subtitle (filePath):
    """ Function doc """
    n = napi.Napi(filePath)
    n.setDebug(True)
    #n.test()
    n.getSubtitles()
    del n

def get_form_dir(dirPath):
    movie = ('asf', 'avi', 'flv', 'mkv' , 'mov', 'mp4', 'mpe', 'mpg', 'mpeg','rmvb', 'wmv', '3pg', '3gp')
    dirPath = dirPath.rstrip('/')
    for f in os.listdir(dirPath):
        if f[0] =='.': continue
        if os.path.isdir("{0}/{1}".format(dirPath,f)): continue
        #file_list.append("{0}/{1}".format(dirPath,f))
        suffix = ''
        if f.find('.') > 0:
            suffix = f.rsplit('.',1)[1].lower()
            if (suffix in movie):
                try:
                    Thread(target=get_subtitle, args=("{0}/{1}".format(dirPath,f),)).start()
                except Exception as errtxt:
                    print(errtxt)


if __name__ == '__main__':
    if(len(sys.argv)==1) or not os.path.exists(sys.argv[1]):
        sys.exit(1)
    for f in sys.argv[1:]:
        if os.path.isdir(f):
            get_form_dir(f)
        else:
            try:
                Thread(target=get_subtitle, args=(f,)).start()
            except Exception as errtxt:
                print(errtxt)
