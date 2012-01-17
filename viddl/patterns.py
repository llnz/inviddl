'''Some base classes to make writing sites easier

Find the pattern that fits the best, then subclass to add the specific 
behavour as needed
'''
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

from xml.etree import ElementTree as ET

from viddl.steps import download_step, download_video_step, extract_step


class VideoSite(object):
    '''A basic video site.
    
    This class shows off the basic API the rest of the library expects. 
    You don't need to subclass this, but it does show the API and connect
    the download_from_url to download_from_page by downloading the page.
    '''
    
    def download_from_url(self, url):
        video_webpage = download_step(True, 'Retrieving video webpage', 'unable to retrieve video webpage', url)
        
        self.download_from_page(url, video_webpage)
        
    
    def download_from_page(self, url, page):
        raise NotImplementedError()

class ExtSMILVideoSite(object):
    '''A site using an external SMIL file to define the videos to play.
    
    Downloads the SMIL file, reads it and then downloads the videos which
    have the highest system bandwidth.
    '''
    
    def download_smil_and_videos(self, smil_url):
        smil_file = download_step(True, 'Retrieving SMIL playlist', 'unable to retrieve SMIL playlist', smil_url)

        print('Parsing SMIL')
        
        smildoc = ET.fromstring(smil_file)
        
        print('Extracting video urls')
        
        listofvideotags = smildoc.findall('.//{http://www.w3.org/ns/SMIL}video')
        videosbybitrate = {}
        
        for videotag in listofvideotags:
            bitrate = int(videotag.get('systemBitrate'))
            brvideos = videosbybitrate.get(bitrate)
            if brvideos is None:
                brvideos = []
                videosbybitrate[bitrate] = brvideos
            brvideos.append(videotag.get('src'))
        
        videos = videosbybitrate[max(videosbybitrate.keys())]
        
        for video_url_real in videos:
            
            
            print video_url_real
        
            video_filename = video_url_real.split('/')[-1]
            
            download_video_step(video_filename, video_url_real)
            

class FileVarDownloadSite(VideoSite):
    '''Page contains a variable which with a url formater can be turned into 
    the url to download'''
    
    const_video_url_param_re = None
    
    def video_url_from_param(self, param):
        '''Return the video url for the given param.'''
        raise NotImplementedError()

    
    def download_from_page(self, url, page):
        video_url_param = extract_step('Extracting video URL parameter', 'unable to extract video URL parameter', self.const_video_url_param_re, page)
        
        print "raw video_url_param: ", video_url_param
        
        video_url_real = self.video_url_from_param(video_url_param)
        
        video_filename = video_url_real.split('/')[-1]
        
        print video_url_real
        
        download_video_step(video_filename, video_url_real)


