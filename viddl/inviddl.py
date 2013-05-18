'''The main inviddl code'''
#    Copyright (C) 2012, 2013 by Lee Begg                                      
#    <llnz@paradise.net.nz>                                                             
#
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without modification, 
#are permitted provided that the following conditions are met:
#
# - Redistributions of source code must retain the above copyright notice, this list 
# of conditions and the following disclaimer.
#
# - Redistributions in binary form must reproduce the above copyright notice, this 
# list of conditions and the following disclaimer in the documentation and/or other 
# materials provided with the distribution.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
#ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. 
#IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, 
#INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
#BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
#DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
#LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE 
#OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED 
#OF THE POSSIBILITY OF SUCH DAMAGE.
import sys


from viddl.sites import get_site

#load site modules
from viddl.sites import nz3news, stuff, ch9nz, nzfilmarchive, tvnznews, nzonscreen

def main():
    
    #parse args
    if len(sys.argv) != 2:
        sys.exit('Usage: %s url [url ...]' % sys.argv[0])
    urls = sys.argv[1:]
    
    
    for url in urls:
        #check url to find site
        site = get_site(url)
        #if found
        if site is not None:
            print 'Found site %s' % site.__class__.__name__
            #site.download_from_url
            site.download_from_url(url)
        #else
        else:
            print "fail"
            #download page
            #check resulting url to find site
            #if found
                #site.download_from_page
            #else
                #try default downloaders
    
    pass