# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

__author__ = " Biru C. Sainju"

__version__ = "0.1"
from PersistentDefaultDict import Crawled
from PersistentDefaultDict import crawled_urls
print crawled_urls
host='simpsonss'
url='homer.html'
if url not in crawled_urls[host]:
    crawled_urls[host].append(url,Crawled,host)
else:
    print "already exists"