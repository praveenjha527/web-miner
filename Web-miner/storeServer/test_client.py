# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

__author__ = " Biru C. Sainju"

__version__ = "0.1"
# Echo client program
import my_gzip
import zlib

def decompress(fname):
    zfile = my_gzip.GzipFile(filename=fname,mode = 'rb',   compresslevel = 2)
    url=zfile.readline().rstrip('\n')
    contents=zfile.read()
    #print len(contents)
    contents=zlib.compress(contents,6)
    print len(contents)
    data={'url':url,'contents':contents}
    return data

fname='index.html.gz'
sss=decompress(fname)
import socket
import cPickle
HOST = '127.0.0.1'    # The remote host
PORT = 2021             # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

test=cPickle.dumps(sss)
#print len(test)
test=zlib.compress(test,6)
print len(test)
s.send(test+"\r\n")
s.close()

