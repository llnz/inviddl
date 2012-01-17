'''
Created on 12/01/2012

@author: lee
'''
#    Copyright (C) 2009 by Lee Begg                                      
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

from viddl.patterns import FileVarDownloadSite
from viddl.sites import register_site
from viddl.steps import download_step, extract_step

@register_site(r'http://(.*\.)?stuff\.co\.nz/')
class Stuff(FileVarDownloadSite):
    const_video_url_param_re = re.compile(r".*mediaXML:.*'http://([^']+)'.*")
    
    const_xml_url_real_fmt = "http://%s"
    const_video_real_url_param_re = re.compile(r'.*<media:content url="http://([^"]+)".*')
    const_video_url_real_fmt = "http://%s"
    
    def video_url_from_param(self, video_url_param):
        xml_url_real = self.const_xml_url_real_fmt % (video_url_param)

        xml_page = download_step(True, 'Retrieving XML page', 'unable to retrieve xml page', xml_url_real)

        video_url_param = extract_step('Extract video url parameter', 'unable to extract video url parameter', self.const_video_real_url_param_re, xml_page)

        video_url_real = self.const_video_url_real_fmt % (video_url_param)
        
        return video_url_real
