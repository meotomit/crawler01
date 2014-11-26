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
        categoryPrefix = 'http://nongnghiep.vn/nongnghiepvn/vi-vn/'
        categorySuffix = self.getCategorySuffix(url)
        
        html = self.getHtml(url)
        soup = BeautifulSoup(html)
        content = soup.find('div', {'class' : 'p-news'})
        #print content
        if content:
            links = content.findAll('a')
            for link in links:
                if link.has_attr('href'):                
                    href = link['href']                    
                    if categorySuffix != None:  
                        if href.startswith(categoryPrefix) and href.find(categorySuffix) != -1:
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
        mainContent = soup.find('div', {'class' : 'p-news-detail'})
        titleSoup = mainContent.find('div', {'class' : 'title'})
        sapoSoup = mainContent.find('div', {'class' : 'sapo'})
        contentSoup = mainContent.find('div', {'class' : 'content'})
        
        if (titleSoup):
            tmp1 = titleSoup.get_text().strip()
            result += tmp1 + '\r\n'
            
        if (sapoSoup):
            tmp2 = sapoSoup.get_text().strip()
            result += tmp2 + '\r\n'
            
        if mainContent:
            contentSoup = self.filterTags(contentSoup)                        
            tmp3 = contentSoup.get_text().strip()            
            tmp3 = self.filterContent(tmp3)
            result += tmp3
        else :
            print 'can not parse'
        if len(result) < 1:
            return None
        return result

if __name__ == '__main__':
    
    obj = nongnghiep_vn()

    url = 'http://nongnghiep.vn/nongnghiepvn/vi-vn/15/20-ky-thuat-nghe-nong.html'
    listLinks = obj.getLinks(url)
    for link in listLinks:
        print link
         
    '''
    url = 'http://nongnghiep.vn/nongnghiepvn/vi-vn/25/133577/khuyen-nong/bo-ha-noi-lot-xac.html'
    mainContent = obj.getPageDetail(url)
    print mainContent
    '''
    
    print 'Done'