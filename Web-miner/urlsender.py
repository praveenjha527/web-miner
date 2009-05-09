# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.


from __future__ import with_statement

__author__ = ' suvash '
__lastModified__ = ' Oct 9, 2008 '


from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import ClientFactory
from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from crawlerConfig import *

class UrlSendProtocol(LineReceiver):
    
    def lineReceived(self, info):
        print repr(info)
        if (len(self.factory.data)):
            if(info == "OK"):
                self.factory.sendStatus = "OK"
                url = self.factory.data.pop()
                self.transport.write(url+"\r\n")
        else:
            self.loseConnection()
            
    def loseConnection(self):
        """Close the connection, and ignore any further lines and raw data."""
        self.transport.loseConnection()
        self.__ignoreBuffer = True

    def connectionMade(self):
        print "connection made"
        data = self.factory.data.pop()
        self.transport.write(data+"\r\n")
        print "data sent"
        
class UrlSendClientFactory(ClientFactory):
    
    protocol = UrlSendProtocol
   
    def startedConnecting(self, connector):
        self.senStatus ="OK"
        self.data =[]
        with open("urls.txt","rb") as f:
            for line in f:
                self.data.append(line)
        print len(self.data)
        print 'Started to connect.'
        
    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason
    
    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason


if __name__ == '__main__':
    reactor.connectTCP(HOST,URL_FRONTIER_SERVER_PORT, UrlSendClientFactory())
    reactor.run()

            