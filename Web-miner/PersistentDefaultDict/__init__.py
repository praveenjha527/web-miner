
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.



__author__ = " Biru C. Sainju "
__version__ = "0.1"
import sys
import os
from sqlobject import *
from collections import defaultdict
if sys.platform[:3] == "win":
    def getcwd():
        return os.getcwd().replace(':', '|')
else:
    getcwd = os.getcwd
db=os.path.join(getcwd(), 'crawler.db')
connection_string='sqlite:///'+db #for sqlite
#connection_string='mysql://root@localhost/crawler' for mysql
connection = connectionForURI(connection_string)
sqlhub.processConnection = connection

class Crawled(SQLObject):
    host = StringCol()
    url = StringCol()
try:
    Crawled.createTable()
except  dberrors.OperationalError:
    pass # table already exists
	
class sublist(list):
    def append(self,url,model,host,dbreadmode=False):
        super(sublist,self).append(url)
        if not dbreadmode:
            #print "called"
            try:
                r = model(host=host, url=url)
            except:
                print "error"

class PersistentDict(defaultdict):
    def __init__(self, model):
        super(PersistentDict, self).__init__(sublist)
        self.model = model
        for row in model.select():
            self[row.host].append(row.url,model,row.host,True)

crawled_urls = PersistentDict(Crawled)
"""if __name__=="__main__":
    crawled_urls = PersistentDict(Crawled)
    url='images'
    host='www.google.com'
    if url not in crawled_urls[host]:
        print "satisfied"
        crawled_urls['tupac'].append('biruthesupergreat',Crawled,'tupac')
    else:
	    print "url already exists"
"""
