#    Copyright (C) 2012 by Lee Begg                                      
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

@register_site(r'http://(www\.)?3news\.co\.nz/', 
               r'http://feedproxy\.google\.com/~r/Tv3LatestNewsVideo/')
class Nz3News(FileVarDownloadSite):
    const_video_url_param_re = re.compile(r'var video ="([^"]+)"')
    const_video_url_real_fmt = "http://flash.mediaworks.co.nz/tv3/streams/_definst_%s_%s.mp4"
    video_speed = "700K"
    
    def video_url_from_param(self, video_url_param):
        if video_url_param[0] != '/':
            video_url_param = video_url_param.replace(video_url_param[0], '/')
        else:
            video_url_param = video_url_param.replace('*', '/')
        
        if video_url_param[:2] == '//':
            video_url_param = video_url_param[1:]
        
        video_url_real = self.const_video_url_real_fmt % (video_url_param, self.video_speed)
        return video_url_real

#Nz3News = register_site(Nz3News, r'http://(www\.)?3news\.co\.nz/', 
#               r'http://feedproxy\.google\.com/~r/Tv3LatestNewsVideo/')