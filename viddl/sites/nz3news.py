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

import re

from viddl.patterns import M3uPlaylistVarDownloadSite
from viddl.sites import register_site

@register_site(r'http://(www\.)?3news\.co\.nz/', 
               r'http://feedproxy\.google\.com/~r/Tv3LatestNewsVideo/')
class Nz3News(M3uPlaylistVarDownloadSite):
    const_playlist_url_param_re = re.compile(r'var video ="([^"]+)"')
    const_playlist_url_real_fmt = "http://strm.3news.co.nz/vod/_definst_/mp4:3news%s_%s.mp4/playlist.m3u8"
    const_video_filename_real_fmt = "%s_%s.mp4"
    video_speed = "700K"
    
    def playlist_url_from_param(self, playlist_url_param):
        if playlist_url_param[0] != '/':
            playlist_url_param = playlist_url_param.replace(playlist_url_param[0], '/')
        else:
            playlist_url_param = playlist_url_param.replace('*', '/')
        
        if playlist_url_param[:2] == '//':
            playlist_url_param = playlist_url_param[1:]
        
        playlist_url_real = self.const_playlist_url_real_fmt % (playlist_url_param, self.video_speed)
        return playlist_url_real

    def filename_from_param(self, playlist_url_param):
        '''Return the video filename for the given param.'''
        return (self.const_video_filename_real_fmt % (playlist_url_param, self.video_speed)).split('/')[-1]
    
#Nz3News = register_site(Nz3News, r'http://(www\.)?3news\.co\.nz/', 
#               r'http://feedproxy\.google\.com/~r/Tv3LatestNewsVideo/')