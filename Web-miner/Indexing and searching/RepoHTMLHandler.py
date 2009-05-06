import os, popen2

from lucene import Document, Field, StringReader
from Streams import RepoReader, InputStreamReader
import mod_gzip

class RepoHTMLHandler(object):

    def indexFile(self, writer, path):

        try:
            file = mod_gzip.GzipFile(filename = path,mode = 'rb', compresslevel = 2)
            url, HTMLcontents = RepoReader(InputStreamReader(file, 'utf-8')).read()
            file.close()
        except:
            raise
        else:
            doc = Document()
            doc.add(Field("contents", HTMLcontents, 
                          Field.Store.NO, Field.Index.TOKENIZED))
            doc.add(Field("url", url, 
                           Field.Store.YES, Field.Index.NO))
            writer.addDocument(doc)

            return doc