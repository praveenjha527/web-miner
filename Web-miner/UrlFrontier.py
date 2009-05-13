#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = ' suvash '
__lastModified__ = ' Oct 23, 2008 '


from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory
from twisted.internet import reactor
from twisted.internet import threads
from twisted.web import xmlrpc
from twisted.web import server
from persistentQueue import PersistentQueue
import marshal
from priorityQueue import PriorityQueue
from random import randint
from random import choice
from URLInfo import get_baseUrl
from time import time
from time import sleep
import os
from crawlerConfig import *

#keeps the track of the client connected to the server
connected_clients = []

#returns the priority of the url        
def getPriority(url):
    return randint(0,9)

class getUrlQueues():
    def __init__(self, n, type, cache_size , marshal):
        self.no_of_queues = n
        self.queues = []
        for i in range(0,self.no_of_queues):
            self.queues.append(PersistentQueue((type+"_"+str(i)), cache_size, marshal))
        

class UrlFrontQueue(getUrlQueues):
    def __init__(self,n,cache_size = 512, marshal = marshal ):
        getUrlQueues.__init__(self, n , "FrontQueue",cache_size, marshal)
    
    def isEmpty(self):
        for i in range(0,self.no_of_queues ):
            if(len(self.queues[i])):
               return False
        return True
            
        
class UrlBackQueue(getUrlQueues):
    
    def __init__(self, n ,cache_size = 512, marshal = marshal ):
        self.empty_queues =[]    
        for i in range(0,n):
            self.empty_queues.append(i)
        self.host_to_queue_maptable = {}
        getUrlQueues.__init__(self,n,"BackQueue", cache_size, marshal)
        self.host_timestamp_pQueue = PriorityQueue(n)
    
            
    
#Protocol for the URLfrontier    
class UrlFrontierProtocol(LineReceiver):
    
    def connectionMade(self):
        connected_clients.append(self)
        
    #Callback called when a line is received
    def lineReceived(self, Url):
        #print Url
        queue_index = getPriority(Url) 
        self.factory.front_queues.queues[queue_index].put(Url)
        self.transport.write("OK\r\n")
            
    def connectionLost(self,reason):
        print reason
        
         
class UrlFrontierServer(Factory):
    
    protocol = UrlFrontierProtocol
    
    def startFactory(self):
        if not (os.path.exists(QUEUE_PATH)):
            os.mkdir(QUEUE_PATH)
        os.chdir(QUEUE_PATH)
        self.front_queues = UrlFrontQueue(10)
        self.back_queues = UrlBackQueue(50)
    
def updateBackQueue(front_queues,back_queues):
    
    isUrlHostUnique = False
    
    while(front_queues.isEmpty()):
        sleep(2)
    
    while not isUrlHostUnique:
        front_queue_index = int(randint(0,9))
        while(not len(front_queues.queues[front_queue_index])):
            sleep(1)
            front_queue_index = int(randint(0,9))
            
        url=front_queues.queues[front_queue_index].get()
        #get the host of the url
        url_host = get_baseUrl(url)
        host_keys = back_queues.host_to_queue_maptable.keys()
        if(url_host in host_keys):
            try:
                back_queues.queues[back_queues.host_to_queue_maptable.get(url_host)].put(url)
            except:
                print "Cannot enqueue the ",url," to back url"     
        else:
            back_queue_index = choice(back_queues.empty_queues)
            try:
                back_queues.queues[back_queue_index].put(url)
            except:
                print "Cannot enqueue the ",url," to back url"
            back_queues.host_to_queue_maptable[url_host] = back_queue_index
            try:
                back_queues.host_timestamp_pQueue.put(url_host, priority = (time()+30),timeout = 0 )
            except:
                print "Cannot cannot enqueue ",url_host," to host_timestamp_pQueue"
            back_queues.empty_queues.remove(back_queue_index)
            isUrlHostUnique = True
            

class UrlServer(xmlrpc.XMLRPC):
    
    def __init__(self,front_queues, back_queues):
        self.front_queues = front_queues
        self.back_queues = back_queues 
        xmlrpc.XMLRPC.__init__(self)
    
    def xmlrpc_getUrl(self):
        
        if not self.back_queues.host_timestamp_pQueue.qsize():  
            updateBackQueue(self.front_queues, self.back_queues)          
        host, priority = self.back_queues.host_timestamp_pQueue.get_with_priority(timeout = 0) 
        try:
            queue_index = self.back_queues.host_to_queue_maptable[host]
        except:
            print host
            print "the given host is not available"
        else:
            url = self.back_queues.queues[queue_index].get()
            if(not len(self.back_queues.queues[queue_index])):
                self.back_queues.host_to_queue_maptable.pop(host)
                self.back_queues.empty_queues.append(queue_index)
            return (url, priority)
        return None

    
    def xmlrpc_update(self,*args):
        pageretrievaltime, url_host  = args
        print url_host, pageretrievaltime
        if url_host in self.back_queues.host_to_queue_maptable.keys():
            #self.back_queues.host_timestamp_pQueue.qsize()
            self.back_queues.host_timestamp_pQueue.put(url_host, priority = (time()+10*pageretrievaltime),timeout = 0)
      
          
if __name__ == '__main__': 
    frontier_server = UrlFrontierServer()
    reactor.listenTCP(URL_FRONTIER_SERVER_PORT,frontier_server)
    urlserver = UrlServer(frontier_server.front_queues,frontier_server.back_queues)
    reactor.listenTCP(URL_SERVER_PORT, server.Site(urlserver))
    reactor.run()

