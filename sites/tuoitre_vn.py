# -*- coding: utf-8 -*-
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath('__file__')), os.pardir))
from bs4 import BeautifulSoup

from sites.ISite import ISite
#import requests
#import urllib2
import re

class tuoitre_vn(ISite):
        
    SUFFIX_URL = '.html'
    
    def getLinks(self, url):
        '''
            Lay danh sach cac trang chi tiet trong 1 trang chuyen muc
        '''
        results = []
        categoryPrefix = url
        
        html = self.getHtml(url)
        soup = BeautifulSoup(html)
        content = soup.find('section', {'class' : 'content'})
        print content
        if content:
            links = content.findAll('a')
            for link in links:
                if link.has_attr('href'):                
                    href = link['href']
                    print href
                    
                    if href.startswith(categoryPrefix):
                        tmp = self.filterUrl(href)
                        if tmp and (tmp not in results):                       
                            results.append(tmp)
                    
        else :
            print 'Can NOT parse URL: ', url
        
        return results


    def getPageDetail(self, pageUrl):   
        html = self.getHtml(pageUrl)
        soup = BeautifulSoup(html, 'lxml')
        mainContent = soup.find('div', {'class' : 'fck'})    
        if mainContent:
            mainContent = self.filterTags(mainContent)
            
            # remove breadcrumbs
            for elem in mainContent.findAll('div', {'class' : 'box26'}):
                elem.extract()
                    
            text = mainContent.get_text().strip()
            
            text = self.filterContent(text)
            text = re.sub(u' \(Dân trí\) \- ', '', text)
            return text
        else :
            print 'can not parse'
            return None

if __name__ == '__main__':
        obj = tuoitre_vn()
        
        '''
        # test get urls
        url = 'http://tuoitre.vn/tin/phap-luat'  
        url = 'http://tuoitre.vn/tin/nhip-song-tre'
        url = 'http://tuoitre.vn/tin/giao-duc'
        listLinks = obj.getLinks(url)
        for link in listLinks:
            print link  
                  
        '''
    
        # Test get page detail
#         url = 'http://kinhdoanh.vnexpress.net/tin-tuc/doanh-nghiep/khu-vui-choi-tre-em-thi-truong-3-ty-dola-3091745.html'
        url = 'http://tuoitre.vn/tin/giao-duc/20141015/dhqg-tphcm-cong-bo-phuong-an-tuyen-sinh-chinh-thuc/658660.html'
        url = 'http://tuoitre.vn/tin/van-hoa-giai-tri/20141015/dung-khan-pieu-lam-kho-su-co-ngoai-y-muon/658645.html'
        url = 'http://tuoitre.vn/tin/phap-luat/20141014/bong-dung-bi-to-dua-thieu-100-trieu-dong/658111.html'
        mainContent = obj.getPageDetail(url)
        print mainContent
        
        print 'DONE'

