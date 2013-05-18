#    Copyright (C) 2009, 2013 by Lee Begg                                      
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

import re
from xml.etree import ElementTree as ET
from viddl.patterns import VideoSite
from viddl.steps import download_step, extract_step, download_video_step
from viddl.sites import register_site

@register_site(r'http://(www\.)?nzonscreen\.com/')
class NzOnScreen(VideoSite):
    
    const_xmlfile_re = re.compile(r"flashVars.*=.*'.*&amp;xmlURL=([^'&]+)(?:&.*)*';")
    const_xmlfile_url_fmt = "http://www.nzonscreen.com%s"
    
    def download_from_page(self, url, page):
        xmlfilestr = extract_step('Extracting XML playlist url', 'unabled to extract XML playlist url', self.const_xmlfile_re, page)

        xmlfileurl = self.const_xmlfile_url_fmt % xmlfilestr
        
        xml_file = download_step(True, 'Retrieving XML playlist', 'unable to retrieve XML playlist', xmlfileurl)
        
        print('Parsing XML')
        
        xmldoc = ET.fromstring(xml_file)
        
        print('Extracting video urls')
        
        videoprefix = xmldoc.get('videoPrefix')
        
        
        listofvideotags = xmldoc.findall('.//imageBox')
        videos = []
        
        for videotag in listofvideotags:
            vid_url = videotag.get('videoHiRes')
            if vid_url is not None:
                videos.append(vid_url)
        
        for video_url in videos:
            
            video_url_real = "%s%s" % (videoprefix, video_url)
            
            print video_url_real
        
            video_filename = video_url_real.split('/')[-1]
            
            download_video_step(video_filename, video_url_real)
