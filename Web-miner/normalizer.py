# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

__author__ = " Biru C. Sainju"

__version__ = "0.1"
import string
import urlparse

def spliturl(url):
    return urlparse.urlparse(url)

def Urlnormalise(url):
    url=string.lower(url)
    url_parts=spliturl(url)
    base=url_parts[1].split(':')
    normalised=base[0]
    for i in xrange(2,4):
        normalised+=url_parts[i]
    if(url_parts[4]):
        normalised+='?'
    normalised+=url_parts[4]
    if(url_parts[5]):
        normalised+='#'
    normalised+=url_parts[5]
    if normalised.endswith('/'):
        normalised=normalised.rstrip('/')
    return normalised

if __name__=='__main__':
    url='http://mail.google.com/mail/?shva=1#inbox/11ed5'
    norm=Urlnormalise(url)
    print norm
