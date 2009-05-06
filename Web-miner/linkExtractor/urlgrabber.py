# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

__author__ = " Biru C. Sainju"
__date__ = " Fri Sep 19 18:40:16 NPT 2008"
__version__ = "0.1"



from urlparse import urljoin
import urllib2
import re
from zip import decompress
from lxml.html import fromstring
from lxml.html.clean import Cleaner

class MyURLResolver:
    def __init__(self,url,filemode):
        if filemode:
		temp_dict=decompress(url)
	     	url_contents=temp_dict['contents']
	    	self.url=temp_dict['url']

        else:
		self.url=url
                url_contents=urllib2.urlopen(url).read()
        print self.url
        cleaner = Cleaner(style=True, links=True, add_nofollow=False,page_structure=False, safe_attrs_only=False)
        self.myhtml=cleaner.clean_html(fromstring(url_contents))

    #grabs the links in the page
    def getlinks(self):
        return self.myhtml.iterlinks()

    #removes the anchoring links
    def remove_anchors(self,links):
        good_list=[]
        for link in links:
            bad_pattern=re.compile('#')
            if not bad_pattern.match(link[2]):
                good_list.append(link)
        return good_list

    #processes the links in tuple
    def processurls(self,url,links):
        cleaned_list=filter(lambda list:list[1] =='href',links)
        more_cleaned_list= self.remove_anchors(cleaned_list)
        pattern=re.compile('/')
        abs_pattern=re.compile(r'(http:)|(ftp:)|(www)')
        skip_pattern=re.compile(r'(javascript:)|(mailto:)|(news:)|(\?m=a)|(\?n=d)|(\?s=a)|(\?d=a)')
        relative_urls=[]
        absolute_urls=[]
        for link in more_cleaned_list:
            if not skip_pattern.match(link[2]):
                if pattern.match(link[2]) or not (abs_pattern.match(link[2])):# and abs_pattern2.match(link[2])) :
                    if link[2] not in relative_urls:
                        relative_urls.append(link[2])
                else:
                    if link[2] not in absolute_urls:
                        absolute_urls.append(link[2])
        relative_urls=self.rewrite_url(url,relative_urls)
        final_urls=absolute_urls+relative_urls
        return final_urls,self.url

    #converts relative to abslute urls
    def rewrite_url(self,url,relative_urls):
        base_url=url
        final_url=[]
        for urls in relative_urls:
            final_url.append(urljoin(base_url,urls))
        
        return final_url

def crawl(url,filemode=None):
    URLResolver=MyURLResolver(url,filemode)
    raw_links=URLResolver.getlinks()
    final_urls,host=URLResolver.processurls(URLResolver.url,raw_links)
    return final_urls,host
if __name__=="__main__":
    #USAGE
    url='http://www.linuxjournal.com'
    final_urls=crawl(url)
    print len(final_urls)
    myfile = open("urls.txt","a+")
    for url in final_urls:

        try:
            print repr(url)
        except:
            print repr(url.encode('utf-16'))
        try:
            myfile.write(url)
            myfile.write('\n')
        except:
            myfile.write(unicode(url))
            myfile.write('\n')
