# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

__author__ = " Biru C. Sainju "
__version__ = "0.1"


import mod_gzip
def compressBuf(buf,url,fname):
    #zbuf = cStringIO.StringIO()
    ##biru = gzip.open('fname', 'wb',compresslevel = 6)
    zfile = my_gzip.GzipFile(filename=fname+'.gz',mode = 'wb',   compresslevel = 2)
    ##biru.write(buf)
    zfile.write(buf,url)

    zfile.close()
def decompress(fname):
    zfile = mod_gzip.GzipFile(filename=fname,mode = 'rb',   compresslevel = 2)
    url=zfile.readline().rstrip('\n')
    contents=zfile.read()
    zfile.close()
    data={'url':url,'contents':contents}
    return data

    ##biru.close()
if __name__=="__main__":
    import urllib2
    myHtml=urllib2.urlopen('http://www.google.com').read()
    #myHtml = """<html><body><h1>hello compressed world!</h1>"""
    url='http://www.google.com/images/today/vies?id=125'
    myHtml=open('sqlexpression.html','rb').read()
    compressBuf(myHtml,url,'biru')
    #data=decompress('biru.gz')
    #print data['url']
    #print data['contents']

