import os, sys, lucene
from time import time
from datetime import timedelta
from lucene import Document, IndexSearcher, FSDirectory, QueryParser, StandardAnalyzer, Hit

sys.path.append("/home/suvash/workspace/python/web-miner/Web-miner")

#from configuration.crawlerConfig import *
from crawlerConfig import *
def initLucene():
    lucene.initVM(lucene.CLASSPATH)
    
def search(q):
    
    initLucene()
    fsDir = FSDirectory.getDirectory(INDEX_PATH, False)
    searcher = IndexSearcher(fsDir)
    query = QueryParser("contents", StandardAnalyzer()).parse(q)
    start = time()
    hits = searcher.search(query)
    duration = timedelta(seconds=time() - start)
    matchpages = []
    for hit in hits:
            doc = Hit.cast_(hit).getDocument()
            temp = ({"title":doc["title"],"url":doc["url"]})
            matchpages.append(temp)
    result = {"no_of_hits":hits.length(),"duration":duration, "query":q,"result":matchpages}
    return result