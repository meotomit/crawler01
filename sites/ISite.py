'''
Created on May 28, 2014

@author: kimphuc
'''
from abc import ABCMeta, abstractmethod
import re
#import requests
import urllib2

class ISite(object):
    __metaclass__ = ABCMeta
    
    QUEUE_DOWNLOADED_URL = 'QUEUE_DOWNLOADED_URL'
    
    # default header
    HEADERS = {
            'Accept':'    text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            #'Origin': 'http://www.indiapost.gov.in',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:28.0) Gecko/20100101 Firefox/28.0',
            #'Content-Type': 'application/x-www-form-urlencoded',
            #'Referer': 'http://www.indiapost.gov.in/pin/',
            #'Accept-Encoding': 'gzip,deflate,sdch',
            #'Accept-Language': 'en-US,en;q=0.8',
            #'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'
        }
    
    SUFFIX_URL = '.html'        
    
    @abstractmethod
    def getLinks(self, cateUrl):        
        pass
    
    @abstractmethod
    def getPageDetail(self, pageUrl):
        pass
    
    def getHtml(self, url):
        #client = requests.Session()
        #r = client.get(url, headers = self.HEADERS)
        #html = r.text
        #html = urllib2.urlopen(url).read()
        req = urllib2.Request(url, None, {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'})
        response = urllib2.urlopen(req).read()
        return response
    
    def filterUrl(self, url):
        # remove anchor
        tmp = url.split('#')
        res = tmp[0]
        
        # keep URL end with .html
        if not res.endswith(self.SUFFIX_URL):
            return None
        return res
    
    def filterTags(self, soupContent):
        for elem in soupContent.findAll(['script', 'style']):
            elem.extract()
        return soupContent
        
    def filterContent(self, content):
        # remove multi space
        content = re.sub('[ \t]+',' ', content)
        content = re.sub('[\r\n]+','\n', content)
        return content
    
    def insertPost(self, conn, cateId, url, content):
        query = "INSERT INTO post(cate_id, site, url, content) values (?, ?, ?, ?)"
        
    
