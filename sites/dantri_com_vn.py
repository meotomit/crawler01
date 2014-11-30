# -*- coding: utf-8 -*-
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath('__file__')), os.pardir))
from bs4 import BeautifulSoup

from sites.ISite import ISite
#import requests
#import urllib2
import re

class dantri_com_vn(ISite):
        
    SUFFIX_URL = '.htm'

    def filterUrl(self, url):        
        url = ISite.filterUrl(self, url)
        url = 'http://dantri.com.vn' + str(url)
        return url
    
    def getLinks(self, url):
        '''
            Lay danh sach cac trang chi tiet trong 1 trang chuyen muc
        '''
        results = []
        categoryPrefix = url[20:-4] + '/' # http://dantri.com.vn/the-gioi.htm --> http://dantri.com.vn/the-gioi/
        
        html = self.getHtml(url)
        soup = BeautifulSoup(html)
        content = soup.find('div', {'class' : 'container'})
        if content:
            links = content.findAll('a')
            for link in links:
                if link.has_attr('href'):                
                    href = link['href']
                    #print href
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
        mainContent = soup.find('div', {'id' : 'ctl00_IDContent_ctl00_divContent'})       
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
            print 'Can NOT parse URL: ' + pageUrl 
            return None

if __name__ == '__main__':
        obj = dantri_com_vn()
        
        '''
        # test get urls
        url = 'http://dantri.com.vn/the-gioi.htm'
        url = 'http://dantri.com.vn/kinh-doanh.htm'
        url = 'http://dantri.com.vn/van-hoa.htm'     
        listLinks = obj.getLinks(url)
        for link in listLinks:
            print link        
        '''
    
        # Test get page detail
#         url = 'http://kinhdoanh.vnexpress.net/tin-tuc/doanh-nghiep/khu-vui-choi-tre-em-thi-truong-3-ty-dola-3091745.html'
        url = 'http://dantri.com.vn/van-hoa/tuoi-tho-hong-nhung-day-ap-ky-niem-qua-cay-bang-cua-cha-955650.htm'
        url = 'http://dantri.com.vn/kinh-doanh/he-lo-noi-that-xa-hoa-trong-lau-dai-ga-vang-cua-dai-gia-ha-noi-956146.htm'
        url = 'http://dantri.com.vn/giao-duc-khuyen-hoc/tuyen-sinh-2015-dh-ngoai-thuong-xet-tuyen-theo-tung-khoi-thi-955972.htm'
        url = 'http://dantri.com.vn/giai-tri/ve-hoang-da-va-cuon-hut-cua-nguoi-phu-nu-goi-tinh-nhat-the-gioi-955837.htm'
        url = 'http://dantri.com.vn/phap-luat/nhom-cau-tac-7-thang-an-hon-200-con-cho-956142.htm'
        mainContent = obj.getPageDetail(url)
        print mainContent
        
        print 'DONE'

