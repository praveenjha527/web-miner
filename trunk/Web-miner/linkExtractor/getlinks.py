# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

__author__ = " Biru C. Sainju "
__version__ = "0.1"


import glob
import socket
from configuration.crawlerConfig import *

from urlgrabber import crawl

class DataSource(object):
    def __init__(self):
        
        self.text_files = glob.glob("."+REPO_PATH+"*/*.gz")

    def __len__(self):
        return len(self.text_files)

    def __iter__(self):
        return iter(self.text_files)

    def __getitem__(self, key):
       
        return key
source = DataSource()

def mapfn(key, value):
    final_urls,host=crawl(value,filemode=True)
    for url in final_urls:
        yield host, url


def reducefn(key, value):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, URL_FRONTIER_SERVER_PORT))
    for i in value:
        s.send(i+"\r\n")
        data = s.recv(4096)
    


