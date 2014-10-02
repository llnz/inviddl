#    Copyright (C) 2014 by Lee Begg                                      
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
from viddl.patterns import Brightcove
from viddl.sites import register_site
from viddl.steps import download_step

@register_site(r'http://([a-z0-9]+\.)?nzherald\.co\.nz')
class NzHerald(Brightcove):
    const_playerid_param_re = re.compile(r"<param name='playerID' value='([^']+)' />")
    const_experience_param_re = re.compile(r"<object class='BrightcoveExperience' .*id='([^']+)'>")
    const_videoplayer_param_re = re.compile(r"<param name='@videoPlayer' value='([^']+)' />")

    def download_from_url(self, url):
        '''Rewrite urls to m.nzherald.co.nz'''
        matches = re.match(r'(http://)([a-z0-9]+\.)?(nzherald\.co\.nz/.*)', url)
        new_url = ''.join([matches.group(1), 'm.', matches.group(3)])
        video_webpage = download_step(True, 'Retrieving video webpage', 'unable to retrieve video webpage', new_url)
        
        self.download_from_page(url, video_webpage)

