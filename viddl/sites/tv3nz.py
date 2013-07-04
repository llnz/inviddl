#    Copyright (C) 2013 by Lee Begg                                      
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
from viddl import steps

@register_site(r'http://(www\.)?tv3\.co\.nz/')
class Tv3nz(M3uPlaylistVarDownloadSite):
    const_playlist_url_param_re = re.compile(r'var video ="([^"]+)"')
    const_geo_param_re = re.compile(r'var geo\s*=\s*"([^"]+)"')
    const_playlist_url_geo_fmt = "https://50a3bc1624217.streamlock.net/vod_https/_definst_/mp4:tv3%s_%s.mp4/playlist.m3u8"
    const_playlist_url_geomob_fmt = 'https://50a3bc1624217.streamlock.net/hls-vod/_definst_/mp4:tv3%s_%s.mp4/playlist.m3u8'
    const_playlist_url_nongeo_fmt = "http://vod-non-geo.mediaworks.co.nz/hls-vod/_definst_/mp4:tv3%s_%s.mp4/playlist.m3u8"
    const_video_filename_real_fmt = "%s_%s.mp4"
    video_speed = "700K"
    
    def download_from_page(self, url, page):
        
        self.geo_param = steps.extract_step('Extract geo param', "Couldn't extract geo param", self.const_geo_param_re, page)
        
        M3uPlaylistVarDownloadSite.download_from_page(self, url, page)
    
    def playlist_url_from_param(self, playlist_url_param):
        if playlist_url_param[0] != '/':
            playlist_url_param = playlist_url_param.replace(playlist_url_param[0], '/')
        else:
            playlist_url_param = playlist_url_param.replace('*', '/')
        
        if playlist_url_param[:2] == '//':
            playlist_url_param = playlist_url_param[1:]
        if self.geo_param == 'geo':
            playlist_url_real = self.const_playlist_url_geo_fmt % (playlist_url_param, self.video_speed)
        elif self.geo_param == 'geomob':
            playlist_url_real = self.const_playlist_url_geomob_fmt % (playlist_url_param, self.video_speed)
        else:
            playlist_url_real = self.const_playlist_url_nongeo_fmt % (playlist_url_param, self.video_speed)
        return playlist_url_real

    def filename_from_param(self, playlist_url_param):
        '''Return the video filename for the given param.'''
        if playlist_url_param[0] != '/':
            playlist_url_param = playlist_url_param.replace(playlist_url_param[0], '/')
        else:
            playlist_url_param = playlist_url_param.replace('*', '/')
        return (self.const_video_filename_real_fmt % (playlist_url_param, self.video_speed)).split('/')[-1]
    
#Nz3News = register_site(Nz3News, r'http://(www\.)?3news\.co\.nz/', 
#               r'http://feedproxy\.google\.com/~r/Tv3LatestNewsVideo/')