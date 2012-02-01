#!/usr/bin/env python

"""
Original author: Paul Boddie <paul@boddie.org.uk>

To the extent possible under law, the person who associated CC0 with this work
has waived all copyright and related or neighboring rights to this work.

See: http://creativecommons.org/publicdomain/zero/1.0/
"""

import sgmllib
import urllib, sgmllib
import string
from sets import Set

from urllib2 import Request, urlopen, URLError, HTTPError
from httplib import BadStatusLine


class MyParser(sgmllib.SGMLParser):
    "A simple parser class."

    def parse(self, s):
        "Parse the given string 's'."
        self.feed(s)
        self.close()

    def __init__(self, verbose=0):
        "Initialise an object, passing 'verbose' to the superclass."

        sgmllib.SGMLParser.__init__(self, verbose)
        self.hyperlinks = []

    def start_a(self, attributes):
        "Process a hyperlink and its 'attributes'."

        for name, value in attributes:
            if name == "href":
                self.hyperlinks.append(value)

    def get_hyperlinks(self):
        "Return the list of hyperlinks."

        return self.hyperlinks



# Get something to work with.
f = urlopen("http://www.naver.com")
s = f.read()

# Try and process the page.
# The class should have been defined first, remember.
myparser = MyParser()
myparser.parse(s)

lst = set()
# Get the hyperlinks.
for lnks in  myparser.get_hyperlinks():
    if string.find(lnks, 'http') == 0:
        lst.add(lnks)

for lnk in lst:
    print lnk
    try:
        response = urlopen(lnk)
        
    except HTTPError, e:
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
        
    except URLError, e:
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason

    except BadStatusLine, e:
        print 'a server responds with a HTTP status code that we don\'t understand'
        print 'Reason: ', e

    except IOError as (errno, strerror):
        print "I/O error({0}): {1}".format(errno, strerror)

    # print response.read()
    
