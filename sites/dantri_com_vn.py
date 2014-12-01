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
        if url:
            search = re.search("/trang-\d+\.htm", url)
            if search: # neu la trang paging
                return None
            if url.find('dantri.com.vn') > 0:
                return url
            else:
                url = 'http://dantri.com.vn' + str(url)
                return url
        else:
            return None
    
    def getLinks(self, url):
        '''
            Lay danh sach cac trang chi tiet trong 1 trang chuyen muc
        '''
        results = []
        #import pdb
        #pdb.set_trace()
        match = re.search('/trang\-\d+\.htm', url)
        categoryPrefix = url
        if match:
            categoryPrefix = re.sub('/trang\-\d+.htm', '/', url)
            #categoryPrefix = url[:pos+1] #
        else:
            categoryPrefix = url[:-4] + '/' # http://dantri.com.vn/the-gioi.htm --> http://dantri.com.vn/the-gioi/
        
        html = self.getHtml(url)
        soup = BeautifulSoup(html)
        content = soup.find('div', {'class' : 'container'})
        if content:
            links = content.findAll('a')
            for link in links:
                if link.has_attr('href'):                
                    href = link['href']
                    if href:
                        #import pdb
                        #pdb.set_trace()
                        if href.find('dantri.com.vn') < 0:
                            href = 'http://dantri.com.vn' + href
                    #print href
                    if href.startswith(categoryPrefix):
                        tmp = self.filterUrl(href)
                        if tmp and (tmp not in results):
                            if tmp.find('xem-nhieu-nhat.htm') < 0:                        
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
            if text:
                text = re.sub(u' \(Dân trí\) \- ', '', text)
                return text
            else :
                print 'Content size < 400 chars or can NOT filter content, URL : ' + pageUrl
                return None
        else :
            print 'Can NOT parse URL: ' + pageUrl 
            return None

if __name__ == '__main__':
        obj = dantri_com_vn()
        
        
        # test get urls
        url = 'http://dantri.com.vn/the-gioi.htm'
        url = 'http://dantri.com.vn/kinh-doanh.htm'
        #url = 'http://dantri.com.vn/van-hoa.htm'  
        url = 'http://dantri.com.vn/giao-duc-khuyen-hoc/trang-2.htm'
        listLinks = obj.getLinks(url)
        for link in listLinks:
            print link        
        
    
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

