from PersistentDefaultDict import Crawled
from PersistentDefaultDict import crawled_urls
print crawled_urls
host='simpsons'
url='homer.html'
if url not in crawled_urls[host]:
    crawled_urls[host].append(url,Crawled,host)
else:
    print "already exists"