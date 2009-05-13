# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

__author__ = " Biru C. Sainju"
__version__ = "0.1"

import cPickle
import os
import zlib
from zip import compressBuf
import urlparse
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory
from twisted.internet import reactor
from twisted.internet.protocol import Protocol,ServerFactory
import sys

sys.path.append("/home/suvash/workspace/python/web-miner/Web-miner")

from configuration.crawlerConfig import *


def delete_anchors(url):
        return url.rstrip('#'+urlparse.urlparse(url).fragment)

class storeServerProtocol(LineReceiver):

    MAX_LENGTH = 1024*1024
    
    def pageCallback(self,result,url,host,fname):
        if os.path.isdir(host):
            os.chdir(REPO_PATH+host)
            compressBuf(result,url,fname)
        else:
            os.chdir(REPO_PATH)
            os.mkdir(host)
            os.chdir(REPO_PATH+host)
            compressBuf(result,url,fname)
        os.chdir(REPO_PATH)
        
    def getUrlParams(self,url):
        url_split=urlparse.urlparse(url)
        if url_split.path:
            fname=url_split.path.split('/')
            fname=fname[-1]
        else:
            fname='index.html'
        return url_split.hostname,str(fname)
        
    def deserialize(self,buf):
        da=cPickle.loads(zlib.decompress(buf))
        content=zlib.decompress(da['contents'])
        return da['url'],content
    
    def connectionMade(self):
        print "Connected from", self.transport.client
    
    #Callback called when a line is received
    def lineReceived(self, Url):
    	#print Url
        url,cont=self.deserialize(Url)
        host,fname=self.getUrlParams(url)
        self.pageCallback(cont,url,host,fname)
        print "called"
                    
    def connectionLost(self,reason):
        print reason
         
class storeServer(ServerFactory):
    protocol = storeServerProtocol
    def __init__(self):
	    print "Server Started"

if __name__=='__main__':
    os.chdir(REPO_PATH)
    reactor.listenTCP(STORE_SERVER_PORT, storeServer())
    reactor.run()