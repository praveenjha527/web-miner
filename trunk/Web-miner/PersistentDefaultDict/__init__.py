from sqlobject import *
connection_string='mysql://root@localhost/crawler'
connection = connectionForURI(connection_string)
sqlhub.processConnection = connection
from collections import defaultdict
class Crawled(SQLObject):
    host = StringCol()
    url = StringCol()
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
    url='biruthesupergreat'
    host='tupac'
    if url not in crawled_urls[host]:
        print "satisfied"
        crawled_urls['tupac'].append('biruthesupergreat',Crawled,'tupac')
    else:
	    print "url already exists"
"""
