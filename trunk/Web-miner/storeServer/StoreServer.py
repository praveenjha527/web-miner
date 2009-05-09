import cPickle
import os
import zlib
from zip import compressBuf
import urlparse
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory
from twisted.internet import reactor
from twisted.internet.protocol import Protocol,ServerFactory
from crawlerConfig import *


def delete_anchors(url):
        return url.rstrip('#'+urlparse.urlparse(url).fragment)

class storeServerProtocol(LineReceiver):

    MAX_LENGTH = 64*1024
    
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
    os.chdir("."+REPO_PATH)
    reactor.listenTCP(STORE_SERVER_PORT, storeServer())
    reactor.run()