#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# napi-cli.py
# Copyright (C) 2012-2015  Sebastian Zwierzchowski <sebastian.zwierzchowski@gmail.com>
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

import sys
import os
from threading import Thread
from subtitlestools import napi

def get_subtitle(filePath):
    """ Function doc """
    n = napi.Napi(filePath,debug=True)
    n.getSubtitles()
    del n

def get_form_dir(dirPath):
    movie = ('asf', 'avi', 'flv', 'mkv' , 'mov', 'mp4', 'mpe', 'mpg', 'mpeg', 'rmvb', 'wmv', '3pg', '3gp')
    dirPath = os.path.normpath(dirPath)
    for f in os.listdir(dirPath):
        if f[0] == '.':
            continue
        if os.path.isdir(os.path.join(dirPath, f)):
            continue
        if f.find('.') > 0:
            suffix = f.rsplit('.', 1)[1].lower()
            if suffix in movie:
                try:
                    Thread(target=get_subtitle, args=(os.path.join(dirPath, f),)).start()
                except Exception as errtxt:
                    print(errtxt)

if __name__ == '__main__':
    if(len(sys.argv) == 1) or not os.path.exists(sys.argv[1]):
        sys.exit(1)
    for f in sys.argv[1:]:
        if os.path.isdir(f):
            get_form_dir(f)
        else:
            try:
                Thread(target=get_subtitle, args=(f,)).start()
            except Exception as errtxt:
                print(errtxt)
