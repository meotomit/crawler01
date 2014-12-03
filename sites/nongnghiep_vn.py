# -*- coding: utf-8 -*-
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath('__file__')), os.pardir))
from bs4 import BeautifulSoup

from sites.ISite import ISite
#import requests
#import urllib2
import re

'''
Created on Oct 25, 2014

@author: phuckx
'''

class nongnghiep_vn(ISite):
    '''
    classdocs
    '''
    
    def filterUrl(self, url):
        
        # remove anchor
        tmp = url.split('#')
        res = tmp[0]
        
        # keep URL end with .html
        if not res.endswith(self.SUFFIX_URL):
            return None
        return res
    
    def getCategorySuffix(self, url):
        '''
            Lay ten chuyen muc
        '''
        tmp3 = re.findall(r'/\d+\-([a-z\-]+).html', url)
        if tmp3:
            return tmp3[0] + '/'
        else:
            return None
        
    def getLinks(self, url):
        '''
            Lay danh sach cac trang chi tiet trong 1 trang chuyen muc
        '''
        results = []
        categoryPrefix = 'http://nongnghiep.vn'
        #categorySuffix = self.getCategorySuffix(url)
        
        html = self.getHtml(url)
        soup = BeautifulSoup(html)
        content = soup.find('div', {'class' : 'p-news'})
        #print content
        if content:
            links = content.findAll('a')
            
            
            for link in links:
                if link.has_attr('href'):                
                    href = link['href']                           
                    #if categorySuffix != None:  
                    if href.startswith(categoryPrefix) : #and href.find(categorySuffix) != -1:
                        tmp = self.filterUrl(href)
                        if tmp and (tmp not in results):                                                        
                            results.append(tmp)
                    
        else :
            print 'Can NOT parse URL: ', url
        
        return results
    
    def getPageDetail(self, pageUrl):   
        result = ''
        
        html = self.getHtml(pageUrl)
        soup = BeautifulSoup(html, 'lxml')
        mainContent = soup.find('div', {'itemprop' : 'articleBody'})
        if mainContent:        
            tmp3 = mainContent.get_text().strip()            
            tmp3 = self.filterContent(tmp3)
            result = tmp3
        else :
            print 'can not parse'
        if len(result) < 1:
            return None
        return result

if __name__ == '__main__':
    
    obj = nongnghiep_vn()

    '''
    import urllib
    import urllib2
    url = 'http://nongnghiep.vn/Ajaxloads/ServiceData.asmx/GetNewsDataScrollNews'
    values = { 'catid': 29,'pageIndex': 1}
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    result = response.read()
    print result
    '''
    
    
    '''
    url = 'http://nongnghiep.vn/nongnghiepvn/vi-vn/15/28-giao-duc.html'
    listLinks = obj.getLinks(url)
    print 'Total links: ', len(listLinks)
    for link in listLinks:
        print link
    '''
    
    url = 'http://nongnghiep.vn/hai-xe-dau-dau-ca-vung-vai-khap-quoc-lo-post135325.html'
    url = 'http://nongnghiep.vn/ve-buc-thu-gui-bo-truong-cua-chau-gai-my-linh-post135342.html'
    url = 'http://nongnghiep.vn/cham-soc-cay-mau-den-cuoi-vu-post135450.html'
    url = 'http://nongnghiep.vn/ghep-cai-tao-dieu-o-dong-nai-post135463.html'
    mainContent = obj.getPageDetail(url)
    print mainContent
    
    
    print 'Done'