#!/usr/bin/env python3
# reversed napi 0.16.3.1
#
# by gim,krzynio,dosiu,hash 2oo8.
#
#
#
# last modified: 6-I-2oo8
#
# 4pc0h f0rc3

#
# POZDRAWIAMY NASZYCH FANOW!
# poprawki + dodatki,2to3  generic


import hashlib
import sys
import urllib.request
import os

class Napi:
    """ Class doc """
    def __init__ (self, file_path, debug=False):
        """ Function doc """
        self.movie_name = os.path.basename(file_path)
        d = hashlib.md5()
        d.update(open(file_path, mode='rb').read(10485760))
        self.file_hash = d.hexdigest()
        self.file_path = file_path
        self.debug = debug
        self.lang = 'PL'
        # version : other  - 7zip,
        # version : pynapi - txt
        self.version = "pynapi"
        self.url = ""
        
    def printDebug(self, msg):
        if self.debug:
            print("debug : {}".format(msg))
        
    def setLang(self, lang):
        self.lang = lang
    
    def getLang(self):
        return self.lang
        
    def setVersion(self, v):
        self.version = v
        
    def getVersion(self):
        return self.version
    
    def _f(self, z):
        idx = [0xe, 0x3,  0x6, 0x8, 0x2]
        mul = [2,   2,    5,   4,   3]
        add = [0, 0xd, 0x10, 0xb, 0x5]

        b = []
        for i in range(len(idx)):
            a = add[i]
            m = mul[i]
            i = idx[i]

            t = a + int(z[i], 16)
            v = int(z[t:t+2], 16)
            
            b.append(("%x" % (v*m))[-1])
        return ''.join(b)

    def getSubtitles (self):
        """ Download subtitles from www.napiproject.pl """
        self.url = "http://napiprojekt.pl/unit_napisy/dl.php?l={lang}&f={fhash}&t={f_fhash}&v={ver}&kolejka=false&nick=&pass=&napios={system}".format(
            lang=self.lang,
            fhash=self.file_hash,
            f_fhash=self._f(self.file_hash),
            ver=self.version,
            system=os.name)

        text_file = (self.file_path).rsplit('.', 1)[0]+'.txt'
        if self.version == 'pynapi':
            with open(text_file, "wb") as f:
                f.write(urllib.request.urlopen(self.url).read())

            if os.path.getsize(text_file) <= 4:
                os.unlink(text_file)
                self.printDebug("Subtitles not found")
            else:
                self.printDebug("Downloaded subtitles : {0}".format(self.movie_name))
        elif self.version == 'other':
                zip_file = text_file + '.7z'
                with open(zip_file, "wb") as f:
                    f.write(urllib.request.urlopen(self.url).read())

                if (os.system('7z x -y -so -piBlm8NTigvru0Jr0 "{0}" 2>/dev/null > "{1}"'.format(zip_file, text_file))):
                    self.printDebug("Subtitles not found : {0}".format(self.movie_name))
                    if os.path.exists(text_file):
                        os.unlink(text_file)
                else:
                    self.printDebug("Dwonloaded Subtitles : {0}".format(self.movie_name))
                    os.unlink(zip_file)

    def test (self):
        """ Function doc """
        print("Basename : {0}\nHash : {1}\nfhash : {2}\n".format(self.movie_name, self.file_hash, self._f(self.file_hash)))
        print("url : {0}".format(self.url))

