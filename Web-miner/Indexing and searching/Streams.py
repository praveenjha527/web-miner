from StringIO import StringIO
from HTMLParser import HTMLParser
import zlib

class InputStreamReader(object):

    def __init__(self, inputStream, encoding):

        super(InputStreamReader, self).__init__()
        self.inputStream = inputStream
        self.encoding = encoding or 'utf-8'
  
    def _read(self,length):      
        contents = self.inputStream.read(length)
        return contents

    def read(self,length = -1):
        contents = self._read(length)
        contents = unicode(contents, self.encoding)
        return contents

    def getUrl(self):
         url = self.inputStream.readline().rstrip('\n')
         return url
     
    def close(self):

        self.inputStream.close()


class RepoReader(object):

    def __init__(self, reader):

        self.reader = reader

        class htmlParser(HTMLParser):

            def __init__(self):

                HTMLParser.__init__(self)

                self.buffer = StringIO()
                self.position = 0

            def handle_data(self, data):

                self.buffer.write(data)

            def _read(self, length):

                buffer = self.buffer
                size = buffer.tell() - self.position

                if length > 0 and size > length:
                    buffer.seek(self.position)
                    data = buffer.read(length)
                    self.position += len(data)
                    buffer.seek(0, 2)

                elif size > 0:
                    buffer.seek(self.position)
                    data = buffer.read(size)
                    self.position = 0
                    buffer.seek(0)

                else:
                    data = ''

                return data
                
        self.parser = htmlParser()

    def read(self, length=-1):
        url = self.reader.getUrl()
        while True:
            data = self.reader.read(length)
            if len(data) > 0:
                self.parser.feed(data)
                data = self.parser._read(length)
                if len(data) == 0:
                    continue
            return url,data

    def close(self):

        self.reader.close()