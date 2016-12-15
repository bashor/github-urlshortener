#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  short_url.py
#  
#  Copyright 2016 Felipe Borges <felipe10borges@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import git
import os

BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

FILE_CONTENT = """---
permalink: /%s
---
<html><head><meta http-equiv="refresh" content="0; url="%s" /></head><script>window.location.href = "%s"</script><body style="margin:0;overflow:hidden"><iframe src="%s" width="100&#37;" height="100&#37;" frameborder="0"/></body></html>
"""
repo_url = os.path.dirname(os.path.realpath(__file__))

BASE_URL = "http://feborg.es/"

LAST_ID_FILE = "config.txt"

class Base62:
    def encode (self, num):
        if num == 0:
            return BASE62[0]
        arr = []
        base = len(BASE62)
        while num:
            num, rem = divmod (num, base)
            arr.append (BASE62[rem])
        arr.reverse ()

        return ''.join (arr)

class URLShortner:
    def __init__ (self):
        self.base62 = Base62 ()
        self.repo = git.Repo (repo_url)

    def short (self, url):
        with open (LAST_ID_FILE, 'r') as f:
            self.last_id = int (f.read ())
            uid = self.base62.encode (self.last_id)

            self._create_file (uid, url)

        with open (LAST_ID_FILE, 'w') as f:
            f.write (str (self.last_id + 1))

        self.push (uid, url)

        return uid

    def _create_file (self, uid, url):
        f = open (uid + ".html", 'w')
        f.write (FILE_CONTENT % (uid, url, url, url))
        f.close ()

    def push (self, uid, url):
        self.repo.git.add (uid + ".html")
        self.repo.git.commit(m = "urlshortner: (%s, %s, %s)" % (self.last_id, uid, url))

        self.repo.git.push()
        
def main(args):
    url = args[1]
    if not url:
        print ("USAGE: short_url.py <url>")
        return 0
    
    shortner = URLShortner ()
    uid = shortner.short (url)
    
    print (BASE_URL + uid)
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
