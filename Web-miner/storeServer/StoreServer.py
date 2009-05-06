# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

__author__ = " Biru C. Sainju "
__version__ = "0.1"
import logging
import asyncore
import socket
import cPickle
import os
import zlib
from zip import compressBuf
import urlparse
import md5

#BACKLOG                 = 11
SIZE                    = 1024*64
REPO_PATH        ='/home/suvash/workspace/python/WebCrawler/Testtrunk/Repo/'
def delete_anchors(url):
        return url.rstrip('#'+urlparse.urlparse(url).fragment)

class storeHandler(asyncore.dispatcher):


    def __init__(self, conn_sock, client_address, server):
        self.server             = server
        self.client_address     = client_address
        self.buffer             = ""

        # We dont have anything to write, to start with
        self.is_writable        = False

        # Create ourselves, but with an already provided socket
        asyncore.dispatcher.__init__(self, conn_sock)
        #log.debug("created handler; waiting for loop")

    def readable(self):
        return True     # We are always happy to read


    def writable(self):
        return self.is_writable # But we might not have
                                # anything to send all the time

    def deserialize(self,buf):

        da=cPickle.loads(zlib.decompress(buf))
        content=zlib.decompress(da['contents'])
        return da['url'],content

    def handle_read(self):

        data = self.recv(SIZE)

        if data:

            self.buffer += data
            data=""
            self.is_writable = True  # sth to send back now
        else:
            pass

    def handle_write(self):
        if self.buffer:
            pass

        else:
            pass
        if len(self.buffer) == 0:
            self.is_writable = False


    # Will this ever get called?  Does loop() call
    # handle_close() if we called close, to start with?
    def handle_close(self):
        url,cont=self.deserialize(self.buffer)
        host,fname=self.getUrlParams(url)
        self.pageCallback(cont,url,host,fname)
        self.buffer = ""
        self.close()
        #pass
    def getUrlParams(self,url):

        url_split=urlparse.urlparse(url)
        """hash=md5.new('IOEcrawler')
        hash.update(url)
        return url_split.hostname,str(hash.hexdigest())"""
        if url_split.path:
            fname=url_split.path.split('/')
            #fname=fname[-1]
        else:
            fname='index.html'
        return url_split.hostname,str(fname)
        """import urlparse
        url_split=urlparse.urlparse(url)
        if not url_split.fragment:
            if url_split.path:
                fname=url_split.path.split('/')
                fname=fname[-1]
            else:
                fname='index.html'
        return url_split.hostname,fname"""
    def pageCallback(self,result,url,host,fname):
        print "URL", url,"\nhost",host,"\nFname",fname
        if os.path.isdir(host):
            os.chdir(REPO_PATH+host)
            compressBuf(result,url,fname)
        else:
            os.chdir(REPO_PATH)
            os.mkdir(host)
            os.chdir(REPO_PATH+host)
            compressBuf(result,url,fname)
        os.chdir(REPO_PATH)

class storeServer(asyncore.dispatcher):

    allow_reuse_address         = False
    request_queue_size          = 11
    address_family              = socket.AF_INET
    socket_type                 = socket.SOCK_STREAM


    def __init__(self, address, handlerClass=storeHandler):
        self.address            = address
        self.handlerClass       = handlerClass

        asyncore.dispatcher.__init__(self)
        self.create_socket(self.address_family,
                               self.socket_type)

        if self.allow_reuse_address:
            self.set_reuse_addr()

        self.server_bind()
        self.server_activate()


    def server_bind(self):
        self.bind(self.address)

    def server_activate(self):
        self.listen(self.request_queue_size)


    def fileno(self):
        return self.socket.fileno()


    def serve_forever(self):
        asyncore.loop()


    # TODO: try to implement handle_request()

    # Internal use
    def handle_accept(self):
        (conn_sock, client_address) = self.accept()
        if self.verify_request(conn_sock, client_address):
            self.process_request(conn_sock, client_address)


    def verify_request(self, conn_sock, client_address):
        return True


    def process_request(self, conn_sock, client_address):

        self.handlerClass(conn_sock, client_address, self)


    def handle_close(self):
        self.close()
if __name__=="__main__":
    os.chdir(REPO_PATH)
    port = 2021
    interface='127.0.0.1'
    server = storeServer((interface, port))
    server.serve_forever()