###########################################################################
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
###########################################################################

import urllib2
import httplib
import socket
import sys
import time

const_initial_block_size = 10 * 1024
const_epsilon = 0.0001

class InviddlError(Exception):
    '''Retryable error for Inviddl'''
    pass

def retry(func):
    
    def retry_wrapper(*args, **kwargs):
        for _loop in (0, 1, 2):
            try:
                return func(*args, **kwargs)
            except InviddlError:
                pass
        
    return retry_wrapper

# Calculate new block size based on previous block size
def new_block_size(before, after, bytes):
        new_min = max(bytes / 2.0, 1.0)
        new_max = max(bytes * 2.0, 1.0)
        dif = after - before
        if dif < const_epsilon:
                return int(new_max)
        rate = bytes / dif
        if rate > new_max:
                return int(new_max)
        if rate < new_min:
                return int(new_min)
        return int(rate)



# Wrapper to create custom requests with typical headers
def request_create(url, extra_headers, post_data):
        retval = urllib2.Request(url)
        if post_data is not None:
                retval.add_data(post_data)
        # Try to mimic Firefox, at least a little bit
        retval.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11')
        retval.add_header('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')
        retval.add_header('Accept', 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5')
        retval.add_header('Accept-Language', 'en-us,en;q=0.5')
        if extra_headers is not None:
                for header in extra_headers:
                        retval.add_header(header[0], header[1])
        return retval

# Perform a request, process headers and return response
def perform_request(url, headers=None, data=None):
        request = request_create(url, headers, data)
        response = urllib2.urlopen(request)
        return response

#generic download step
@retry
def download_step(return_data_flag, step_title, step_error, url, post_data=None):
        try:
                print('%s... ' % step_title)
                data = perform_request(url, data=post_data).read()
                print('done.\n')
                if return_data_flag:
                        return data
                return None

        except (urllib2.URLError, ValueError, httplib.HTTPException, TypeError, socket.error):
                print('failed.\n')
                raise InviddlError(step_error)

        except KeyboardInterrupt:
                sys.exit('\n')

# Generic extract step
def extract_step(step_title, step_error, regexp, data):
        try:
                print('%s... ' % step_title)
                match = regexp.search(data)

                if match is None:
                        print('failed.\n')
                        sys.exit(step_error)

                extracted_data = match.group(1)
                print('done.\n')
                return extracted_data

        except KeyboardInterrupt:
                sys.exit('\n')

def download_video_step(video_filename, video_url):
    if(video_url.startswith('http://')):
        http_download_video_step(video_filename, video_url)
    else:
        print("Unable to download video, not http. Actual url is: %s" % video_url)

@retry
def http_download_video_step(video_filename, video_url):
    try:
        video_file = open(video_filename, 'wb')
    except (IOError, OSError):
        sys.exit('Error: unable to open "%s" for writing.' % video_filename)
                
    http_download_video_to_file_step(video_file, video_url)
    
    video_file.close()
    print('Video data saved to %s\n' % video_filename)


def http_download_video_to_file_step(video_file, video_url):
    try:
        print('Requesting video file... ')
        video_data = perform_request(video_url)
        print('done.\n')
    
        try:
                video_len = long(video_data.info()['Content-length'])
                #video_len_str = format_bytes(video_len)
        except KeyError:
                video_len = None
                video_len_str = 'N/A'
    
        byte_counter = 0
        block_size = const_initial_block_size
        start_time = time.time()
        while True:
            #if video_len is not None:
            #        percent = float(byte_counter) / float(video_len) * 100.0
            #        percent_str = '%.1f' % percent
            #        eta_str = calc_eta(start_time, time.time(), video_len, byte_counter)
            #else:
            #        percent_str = '---.-'
            #        eta_str = '--:--'
            #counter = format_bytes(byte_counter)
            #speed_str = calc_speed(start_time, time.time(), byte_counter)
            #cond_print('\rRetrieving video data: %5s%% (%8s of %s) at %8s/s ETA %s ' % (percent_str, counter, video_len_str, speed_str, eta_str))
    
            before = time.time()
            video_block = video_data.read(block_size)
            after = time.time()
            dl_bytes = len(video_block)
            if dl_bytes == 0:
                    break
            byte_counter += dl_bytes
            video_file.write(video_block)
            
            block_size = new_block_size(before, after, dl_bytes)
    
        if video_len is not None and byte_counter != video_len:
                raise InviddlError('server did not send the expected amount of data')
    
        print('done.\n')
        
    except (urllib2.URLError, ValueError, httplib.HTTPException, TypeError, socket.error):
            print('failed.\n')
            raise InviddlError('unable to download video data')
    
    except KeyboardInterrupt:
            sys.exit('\n')
