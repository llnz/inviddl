'''Some base classes to make writing sites easier

Find the pattern that fits the best, then subclass to add the specific 
behavour as needed
'''
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

from xml.etree import ElementTree as ET
import sys, os
import shutil
import json
import re
import operator

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


class M3uPlaylistVarDownloadSite(VideoSite):
    '''Page contains a variable which with a url formater can be turned into 
    the M3u Playlist url to download from'''
    
    const_playerlist_url_param_re = None
    
    def playlist_url_from_param(self, param):
        '''Return the playlist url for the given param.'''
        raise NotImplementedError()

    def filename_from_param(self, param):
        '''Return the video filename for the given param.'''
        raise NotImplementedError()
    
    def download_from_page(self, url, page):
        playlist_url_param = extract_step('Extracting video URL parameter', 'unable to extract video URL parameter', self.const_playlist_url_param_re, page)
        
        print "raw playlist_url_param:", playlist_url_param
        
        playlist_url_real = self.playlist_url_from_param(playlist_url_param)
        
        video_filename = self.filename_from_param(playlist_url_param)
        print "Final filename:", video_filename
        
        print playlist_url_real
        
        playlist_webpage = download_step(True, 'Retrieving playlist', 'unable to retrieve playlist', playlist_url_real)
        
        chunklist_file = [line for line in playlist_webpage.splitlines() if line[0] != '#'][0]
        
        print chunklist_file
        
        chunklist_url = playlist_url_real.rsplit('/', 1)[0] + '/' + chunklist_file
        
        print chunklist_url
        
        chunklist_webpage = download_step(True, 'Retrieving chunklist', 'unable to retrieve chunklist', chunklist_url)
        
        video_items = [line for line in chunklist_webpage.splitlines() if line[0] != '#']
        
        print video_items
        
        tmp_dir = video_filename + '_tmp'
        
        if not os.path.exists(tmp_dir):
            os.mkdir(tmp_dir)
        
        real_video_items = []
        for video_item in video_items:
            real_item = video_item.split('?', 1)[0]
            real_video_items.append(real_item)
            if not os.path.exists(os.path.join(tmp_dir, real_item)):
                download_video_step(os.path.join(tmp_dir, real_item + "_tmp"),  chunklist_url.rsplit('/', 1)[0] + '/' + video_item)
                shutil.move(os.path.join(tmp_dir, real_item + "_tmp"), os.path.join(tmp_dir, real_item))
        
        try:
            video_file = open(video_filename, 'wb')
        except (IOError, OSError):
            sys.exit('Error: unable to open "%s" for writing.' % video_filename)
        
        for video_item in real_video_items:
            with open(os.path.join(tmp_dir, video_item), 'rb') as in_file:
                video_file.write(in_file.read())
        
        video_file.close()
        print('Video data saved to %s\n' % video_filename)
        
        shutil.rmtree(tmp_dir)
        
class Brightcove(VideoSite):
    '''Brightcove is a common Video streaming service.
    '''
    const_playerid_param_re = None
    const_experience_param_re = None
    const_videoplayer_param_re = None
    const_experiencejson_param_re = re.compile(r'var experienceJSON = (\{.*\});')
       
    const_inner_url_format = 'http://c.brightcove.com/services/viewer/htmlFederated?&width=640&height=360&flashID=%s&wmode=opaque&playerID=%s&isVid=true&isUI=true&dynamicStreaming=true&autoStart=true&@videoPlayer=%s'
    
    def download_from_page(self, url, page):
        playerid_param = extract_step('Extracting playerid parameter', 'unable to extract playerid parameter', self.const_playerid_param_re, page)
        experience_param = extract_step('Extracting experience parameter', 'unable to extract experience parameter', self.const_experience_param_re, page)
        videoplayer_param = extract_step('Extracting videoplayer parameter', 'unable to extract videoplayer parameter', self.const_videoplayer_param_re, page)
        
        inner_url_real = self.const_inner_url_format % (experience_param, playerid_param, videoplayer_param)
        
        print "raw inner_url_real: ", inner_url_real
        
        inner_page = download_step(True, 'Retrieving video info webpage', 'unable to retrieve video info webpage', inner_url_real, 
                                   headers=[('User-Agent', 'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3')])
        
        
        experience_json_str = extract_step('Extracting experience json parameter', 'unable to extract experience json parameter', self.const_experiencejson_param_re, inner_page)
        
        experience_json = json.loads(experience_json_str)
        
        speed_url = []
        for rendition in experience_json['data']['programmedContent']['videoPlayer']['mediaDTO']['renditions']:
            speed_url.append((rendition['encodingRate'], rendition['defaultURL']))
        
        video_url_real = sorted(speed_url, key=operator.itemgetter(0), reverse=True)[0][1]
        
        video_filename = self.get_filename(url, page, video_url_real)
        
        print video_url_real
        
        download_video_step(video_filename, video_url_real)
        
    def get_filename(self, url, page, video_url):
        return video_url.split('/')[-1]
