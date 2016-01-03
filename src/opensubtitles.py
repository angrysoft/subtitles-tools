#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# opensubtitle.py
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


# http://trac.opensubtitles.org/projects/opensubtitles/wiki/XMLRPC
# https://docs.python.org/3/library/xmlrpc.client.html#module-xmlrpc.client
#

import struct
import os
import xmlrpc.client

# 200 OK
# 206 Partial content; message
# 401 Unauthorized
# 402 Subtitles has invalid format
# 403 SubHashes (content and sent subhash) are not same!
# 404 Subtitles has invalid language!
# 405 Not all mandatory parameters was specified
# 406 No session
# 407 Download limit reached
# 408 Invalid parameters
# 409 Method not found
# 410 Other or unknown error
# 411 Empty or invalid useragent
# 412 %s has invalid format (reason)
# 501 Temporary down
# 503 Service Unavailable
# 301 Moved (to ​http://api.opensubtitles.org/xml-rpc)

class OpenSubtitles():
    """Class OpenSubtitle"""

    def __init__(self):
        """Constructor for OpenSubtitle"""
        #self.filePath = ""
        #self.movieName = os.path.basename(filePath)
        #self.dirPath = os.path.dirname(filePath)
        self.token = None
        self.userAgent = "SolEol 0.0.8"
        self.lang = 'en'
        self.url = 'http://api.opensubtitles.org:80/xml-rpc'
        self.proxy = None


    def _isConnected(f):
        def decorated_function(self):
            if not self.proxy:
                self.connection()
            return f(self)
        return decorated_function

    def _isLogged(f):
        def decorated_function(self):
            if not self.token:
                self.logIn()
            return f(self)
        return decorated_function

    def connection(self):
        """connection"""
        try:
            self.proxy = xmlrpc.client.ServerProxy(self.url)
        except xmlrpc.client.Fault as err:
            print("A fault occurred")
            print("Fault code: %d" % err.faultCode)
            print("Fault string: %s" % err.faultString)

    def hashFile(self, name):
        try:
            filesize = os.path.getsize(name)
            if filesize < 65536 * 2:
                return "SizeError"
            longlongformat = '<q'  # little-endian long long
            bytesize = struct.calcsize(longlongformat)

            with open(name, "rb") as f:
                hashCode = filesize
                r = int(65536/bytesize)
                for x in range(r):
                    (l_value,) = struct.unpack(longlongformat, f.read(bytesize))
                    hashCode += l_value

                f.seek(max(0,filesize-65536), 0)
                for x in range(r):
                    (l_value,) = struct.unpack(longlongformat, f.read(bytesize))
                    hashCode += l_value

                hashCode &= 0xFFFFFFFFFFFFFFFF

            return '{0:016x}'.format(hashCode)

        except(IOError):
            return "IOError"

    def setLang(self, lang):
        """setLang: For languages codes, check ​ISO639 https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes"""
        self.lang = lang

    def getLang(self):
        return self.lang

    def setToken(self, token):
        """setToken"""
        self.token = token

    def getToken(self):
        """getToken"""
        return self.token
    def getUserAgent(self):
        """getUserAgent"""
        return self.userAgent

    def setUserAgent(self, userAgent):
        """setUserAgent"""
        self.userAgent = userAgent

    @_isConnected
    def logIn(self, username="", password=""):
        """logIn
        :param username: (optional) user login name
        :param password: (otpional) user password
        This will login user. This function should be called always when starting talking with server.
        It returns token, which must be used in later communication. If user has no account,
        blank username and password should be OK. As language - use ​ISO639 2 letter code and later
        communication will be done in this language if applicable. You can also pass language
        in HTTP ACCEPT-LANGUAGE header. Note: when username and password is blank,
        status is 200 OK, because we want allow anonymous users too.
        Useragent cannot be empty string.
        For $useragent use your registered useragent, also provide version number -
        we need tracking version numbers of your program. If your UA is not registered,
        you will get error 414 Unknown User Agent."""
        retVal = self.proxy.LogIn(username, password, self.getLang(), self.getUserAgent())
        if 'token' in retVal:
            self.setToken(retVal['token'])
        return retVal['status']

    def logOut(self):
        """logOut
        This will logout user (ends session id). Good call this function is before ending (closing) clients program."""
        if self.token:
            return self.proxy.LogOut(self.token)['status']

    def _search(self, query='', season='', episode='', imbdId='', movieHash='', movieByteSize='', tag='', limit=50):
        """_search"""
        # self.getLang()
        pass

    def searchByMovieHash(self):
        """searchByFileHash"""
        pass

    def searchByImdbId(self):
        """searchByImdbId"""
        pass

    def searchByQuery(self):
        """searchByQuery"""
        pass

    def searchByTag(self):
        pass

    def test(self, name):
        """test"""
        print(self.hashFile(name))
