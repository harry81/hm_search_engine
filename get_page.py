#!/usr/bin/env python

"""
master
Original author: Paul Boddie <paul@boddie.org.uk>

To the extent possible under law, the person who associated CC0 with this work
has waived all copyright and related or neighboring rights to this work.

See: http://creativecommons.org/publicdomain/zero/1.0/
"""
import sys
import getopt
from types import *

import sgmllib
import urllib, sgmllib
import string

from urllib2 import Request, urlopen, URLError, HTTPError
from httplib import BadStatusLine

lst = []
stack = []

start_page = "http://www.tistory.com"

def main():
    # options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:g", ["help","go"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)

    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)

        elif o in ("-g", "--go"):
            start_page = args[0]

    # verify the start page
    start_page = process_arg(start_page)
    print 'start_page : ' , start_page

    stack.append(start_page)

    while( len(stack) > 0):
        parse_doc()

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


def parse_doc():
    page = stack.pop()
    error = 'ok'
    print   len(lst), len(stack) , ' : parse' ,  page
    
    lst.append(page)

    ## check url errors
    try:
        f = urlopen( page )
        s = f.read()
        
    except HTTPError, e:
        error = 'The server couldn\'t fulfill the request.'
        print error
        print 'Error code: ', e.code
        
    except URLError, e:
        error = 'We failed to reach a server.'
        print error        
        print 'Reason: ', e.reason
        return

    except BadStatusLine, e:
        error = 'a server responds with a HTTP status code that we don\'t understand'
        print error  
        print 'Reason: ', e
        return
    
    except IOError as (errno, strerror):
        print 
        error = "I/O error({0}): {1}".format(errno, strerror)
        print error          

    if error != 'ok':
        return
    
    myparser = MyParser()

    try:
        myparser.parse(s)
    except sgmllib.SGMLParseError, e:
        print "sgmllib.SGMLParseError"
        return    
        
    for lnk in  myparser.get_hyperlinks():
        if string.find(lnk, 'http') == 0:
            if lnk in lst:
#                print 'already exists'
                pass
            else:
                stack.append(lnk)

def process_arg(lnk):
    if not 'http' in lnk:
        lnk = 'http://' + lnk

    return lnk

if __name__ == "__main__":
    main()
