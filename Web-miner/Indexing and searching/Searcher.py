import os

from time import time
from datetime import timedelta

from lucene import \
     Document, IndexSearcher, FSDirectory, QueryParser, StandardAnalyzer, Hit


class Searcher(object):

    @classmethod
    def main(cls, argv):

        if len(argv) != 3:
            print "Usage: python Searcher.py <index dir> <query>"

        else:
            indexDir = argv[1]
            q = argv[2]

            if not (os.path.exists(indexDir) and os.path.isdir(indexDir)):
                raise IOError, "%s does not exist or is not a directory" %(indexDir)

            cls.search(indexDir, q)

    @classmethod
    def search(cls, indexDir, q):

        fsDir = FSDirectory.getDirectory(indexDir, False)
        searcher = IndexSearcher(fsDir)

        query = QueryParser("contents", StandardAnalyzer()).parse(q)
        start = time()
        hits = searcher.search(query)
        duration = timedelta(seconds=time() - start)
        
        #result = {"no_of_hits":hits.length(),"duration":duration, "query":q,}
        #return 
        print "Found %d document(s) (in %s) that matched query '%s':" %(hits.length(), duration, q)

        for hit in hits:
            doc = Hit.cast_(hit).getDocument()
            print doc
            #print doc["url"]
#    main = classmethod(main)
#   search = classmethod(search)


if __name__ == "__main__":     
      
    import os, sys, lucene
    lucene.initVM(lucene.CLASSPATH)
    sys.path.append(os.path.dirname(os.path.abspath(sys.argv[0])))
    Searcher.main(sys.argv)
  