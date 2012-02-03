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
from collections import deque
from time import gmtime, strftime

import sgmllib
import urllib, sgmllib
import string

from urllib2 import Request, urlopen, URLError, HTTPError
from httplib import BadStatusLine, IncompleteRead

lst = []                                # a list for visited
queue = deque()                         # a queue which will be visit.
                                        # queue (parent page, current page, error or message)

start_page = "http://www.tistory.com"   # start point

def main():
    global log_fd
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

    queue.append(('.',start_page,'start'))

    while( len(queue) > 0):
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
    log_fd = get_log_filename ( start_page )        
    # get an element to do
    parent_page, cur_page, err  = queue.popleft()
    error = 'ok'
    mesg = "{0} {1} {2} [{3}] {4}\n".format(len(lst), len(queue) , strftime("%d %H:%M:%S", gmtime()), parent_page, cur_page)
    print mesg
    
    log_fd.write(mesg)
    log_fd.close()

    ## get a content from that file.
    try:
        f = urlopen( cur_page )
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
        error = "I/O error({0}): {1}".format(errno, strerror)
        print error

    except IncompleteRead , e:
        error = 'IncompleteRead'
        print error

    # stop doing when cur_page is bad.
    if error != 'ok':
        lst.append( ( parent_page, cur_page, error) )
        return
    
    myparser = MyParser()

    try:
        myparser.parse(s)
    except sgmllib.SGMLParseError, e:
        print "sgmllib.SGMLParseError"
        return    

    # add all links in the currnt page into queue.
    cnt = 0
    for lnk in  myparser.get_hyperlinks():
        if string.find(lnk, 'http') == 0:
            if lnk in lst:
                pass
            else:
                queue.append((cur_page, lnk, 'ok'))
                cnt = cnt + 1

    #  put cur_page into lst list to mark it as visited.
    lst.append( ( parent_page, cur_page, cnt ) )

    if cnt != 0 :
        print "[", cur_page ,"] added " ,  cnt , "links"

def process_arg(lnk):
    if not 'http' in lnk:
        lnk = 'http://' + lnk

    return lnk

def get_log_filename(name):
    fr = open('text.txt','ab')    
    return fr

if __name__ == "__main__":
    main()
