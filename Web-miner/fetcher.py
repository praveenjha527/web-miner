# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

__author__ = ' suvash '
__lastModified__ = ' Nov 22, 2008 '

from twisted.internet import defer
from twisted.internet import reactor
from twisted.web.client import getPage
from twisted.internet import threads
from URLInfo import get_baseUrl
from robotParser import is_crawlable
import xmlrpclib
import time
import cPickle
import zlib
import socket
from crawlerConfig import *


#fetch the webpage from the internet
@defer.deferredGenerator
def fetch(n):
    global url_server_cnxn
    global store_server_cnxn
    while True:
        print " i am crawler no ", n
        deltatime = 0
        wfd = defer.waitForDeferred(threads.deferToThread(url_server_cnxn.getUrl))
        yield wfd
        #print wfd.result
        
        if wfd.result != None:
            url , time_to_wait = wfd.result
            #print urls
            if (is_crawlable(url) == True):
                #if time tow wait has not expired wait for the time
                if((time.time()-time_to_wait) > 0):
                    time.sleep(time.time()-time_to_wait)
                start_time = time.time()
                wfd = defer.waitForDeferred(getPage(url))
                yield wfd
                if( wfd.result and len(wfd.result) < 65536 ):
                    store_server_cnxn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    store_server_cnxn.connect((HOST, STORE_SERVER_PORT))
                    data_info = {'url':url,'contents': zlib.compress(wfd.result)}
                    data = cPickle.dumps(data_info)
                    compressed_data = zlib.compress(data,6)
                    store_server_cnxn.send(compressed_data + "\r\n")
                    store_server_cnxn.close()
                #sh wfd.result
                deltatime = time.time() - start_time   
        wfd = defer.waitForDeferred(threads.deferToThread(url_server_cnxn.update,deltatime,get_baseUrl(url)))
        yield wfd
        
#start the n concurrent connection
def initFetcher(n):
    for i in range(0,n):
        fetch(i)
        
#run the crawler   
def run():
    
    global url_server_cnxn
    url_server_cnxn = xmlrpclib.Server("http://"+HOST+":"+`URL_SERVER_PORT`)
    #
    initFetcher(NO_OF_CONCURRENT_CONNECTION)
    

        
if __name__ == "__main__":
    run()
    reactor.run()