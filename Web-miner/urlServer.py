# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

__author__ = ' suvash '
__lastModified__ = ' Oct 23, 2008 '

from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory
from twisted.internet import reactor
from persistent import PersistentQueue
from random import randint, choice
from twisted.internet import threads
from URLInfo import get_baseUrl
from time import time
from twisted.web import xmlrpc
from twisted.web import server
from priorityQueue import PriorityQueue

#keeps the track of the client connected to the server
connected_clients = []

#send message tp clent informing the queue is available
def wake_clients():
    i = choice(connected_clients)
    i.transport.write("Null"+" QUEUE_PARTIALLY_FULL\r\n")

#returns the priority of the url        
def getPriority(url):
    return randint(0,9)

class getUrlQueues:
    def __init__(self, n, type, cache_size , marshal):
        self.no_of_queues = n
        self.queues = []
        for i in range(0,self.no_of_queues):
            self.queues.append(PersistentQueue((type+"_"+str(i)), cache_size, marshal)
        

class UrlFrontQueue(getUrlQueues):
    
    def __init__(self,n,cache_size = 512, marshal = "marshal" ):
        getUrlQueues.__init__(self, n , "FrontQueue",cache_size, marshal)
        
class UrlBackQueue(getUrlQueues):
    
    def __init__(self, n ,cache_size = 512, marshal = "marshal" ):
        self.empty_queues =[]
        
        for i in range(0,n):
            self.empty_queues.append(i)
            
        self.host_to_queue_maptable = {}
        getUrlQueues.__init__(self,n,"BackQueue", cache_size, marshal)
        self.host_timestamp_pQueue = PriorityQueue(n)
    
    #returns the list containing the empty backQueue index
    def emptyBackQueue(self):
        emptyBackQueues = []
        for key, data in self.empty_queues:
            if data == True:
                emptyBackQueues.append(key)
        return emptyBackQueues
            
    
#Protocol for the URLfrontier    
class UrlFrontierProtocol(LineReceiver):
    
    def connectionMade(self):
        connected_clients.append(self)
        
    #Callback called when a line is received
    def lineReceived(self, Url):
        queue_index = getPriority(Url) 
        self.factory.front_queues.queues[queue_index].put(Url)
   
            
    def connectionLost(self,reason):
        print reason
        
         
class UrlFrontierServer(Factory):
    
    protocol = UrlFrontierProtocol
    def startFactory(self):
        self.front_queues = UrlFrontQueue(10)
        self.back_queues = UrlBackQueue(50)
    
        

def backQueueManager(front_queues,back_queues,frontier_server):
    while True:
        if back_queues.empty_queues:
            #return the front_queue_index biased to the higher priority ones
            front_queue_index = int(randint(0,9))  
            if len(front_queues.queues[front_queue_index]):
                url=front_queues.queues[front_queue_index].pop()
                #get the host of the url
                url_host = get_baseUrl(url)
                host_keys = back_queues.host_to_queue_maptable.keys()
                #print host_keys
                if(url_host in host_keys):
                   
                    try:
                        back_queues.queues[back_queues.host_to_queue_maptable.get(url_host)].put(url)
                    except:
                        print "thread cannot enqueue the ",url," to back url"     

                else:
                        back_queue_index = choice(back_queues.empty_queues)
                        back_queues.queues[back_queue_index].put(url)
                        back_queues.host_to_queue_maptable[url_host] = back_queue_index
                        back_queues.host_timestamp_pQueue.put(url_host, priority = (time()+30),timeout = 0 )
                        back_queues.empty_queues.remove(back_queue_index)
                         

class UrlServer(xmlrpc.XMLRPC):
    
    def __init__(self, back_queues):
       self.back_queues = back_queues
       xmlrpc.XMLRPC.__init__(self)
    
    def xmlrpc_getUrl(self):
        if self.back_queues.host_timestamp_pQueue.qsize():            
            host, priority = self.back_queues.host_timestamp_pQueue.get_with_priority(timeout = 0) 
            try:
                queue_index = self.back_queues.host_to_queue_maptable[host]
            except:
                print host
                print "the given host is not available"
            else:
                url = self.back_queues.queues[queue_index].pop()
                if(not len(self.back_queues.queues[queue_index])):
                    self.back_queues.host_to_queue_maptable.pop(host)
                    self.back_queues.empty_queues.append(queue_index)
                return (url, priority)
            return 0
        else:
            return 0
    
    def xmlrpc_update(self,*args):
        for i in args:
            url_host , pageretrievaltime = i
        if url_host in self.back_queues.host_to_queue_maptable.keys():
            self.back_queues.host_timestamp_pQueue.qsize()
            self.back_queues.host_timestamp_pQueue.put(url_host, priority = (time()+10*pageretrievaltime),timeout = 0)
            return 0
        else:
            return 1
    
    
if __name__ == '__main__': 
    frontier_server = UrlFrontierServer()
    reactor.listenTCP(1125,frontier_server)
    urlserver = UrlServer(frontier_server.back_queues)
    reactor.listenTCP(1126, server.Site(urlserver))
    reactor.callInThread(backQueueManager,frontier_server.front_queues,frontier_server.back_queues,frontier_server)
    reactor.run()

