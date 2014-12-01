# -*- coding: utf-8 -*-
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath('__file__')), os.pardir))
from bs4 import BeautifulSoup

from sites.ISite import ISite
#import requests
#import urllib2
import re

class vietnamnet_vn(ISite):
        
    SUFFIX_URL = '.html'

    def filterUrl(self, url):        
        url = ISite.filterUrl(self, url)
        if url:
            search = re.search("trang\d+/index.html", url)
            if search:
                return None
        url = 'http://vietnamnet.vn' + str(url)
        return url
            
    def getLinks(self, url):
        '''
            Lay danh sach cac trang chi tiet trong 1 trang chuyen muc
        '''
        results = []
        
        html = self.getHtml(url)
        soup = BeautifulSoup(html)
        content = soup.find('div', {'class' : 'BodyLayout460 left m-r-10'})
        if content:
            links = content.findAll('a')
            for link in links:
                if link.has_attr('href'):                
                    href = link['href']
                    #print href
                    tmp = self.filterUrl(href)
                    if tmp and (tmp not in results) and tmp != 'None':                        
                        results.append(tmp)
        else :
            print 'Can NOT parse URL: ', url
        
        return results


    def getPageDetail(self, pageUrl):   
        html = self.getHtml(pageUrl)
        soup = BeautifulSoup(html, 'lxml')
        titleSoup = soup.find('title')
        title = titleSoup.get_text().strip()
        title = re.sub('- VietNamNet', '', title)
        
        mainContent = soup.find('div', {'class' : 'ArticleContent'})       
        if mainContent:
            mainContent = self.filterTags(mainContent)
            
            # remove adContainer
            for elem in mainContent.findAll('div', {'class' : 'adContainer'}):
                elem.extract()
                
            # remove related page
            for elem in mainContent.findAll('a'):
                elem.extract()
                    
            text = mainContent.get_text().strip()
            
            text = self.filterContent(text)
            if text:
                text = re.sub(u'(Theo Dân trí)<', '', text)
                
                text = re.sub(u'XEM CLIP', '', text)
                text = re.sub(u'Play', '', text)
                text = title + text
                return text
            else :
                print 'Content size < 400 chars or can NOT filter content, URL : ' + pageUrl
                return None
        else :
            print 'Can NOT parse URL: ' + pageUrl 
            return None

if __name__ == '__main__':
        obj = vietnamnet_vn()
                
        # test get urls
        url = 'http://vietnamnet.vn/vn/xa-hoi/'
        url = 'http://vietnamnet.vn/vn/cong-nghe-thong-tin-vien-thong/'    
        url = 'http://vietnamnet.vn/vn/giao-duc/'
        url = 'http://vietnamnet.vn/vn/giao-duc/dien-dan/'
        url = 'http://vietnamnet.vn/vn/giao-duc/chuyen-giang-duong/'
        url = 'http://vietnamnet.vn/vn/doi-song/'
        url = 'http://vietnamnet.vn/vn/kinh-te/trang2/index.html'
        listLinks = obj.getLinks(url)
        for link in listLinks:
            print link        
        
    
        
        # Test get page detail
#         url = 'http://kinhdoanh.vnexpress.net/tin-tuc/doanh-nghiep/khu-vui-choi-tre-em-thi-truong-3-ty-dola-3091745.html'
        url = 'http://vietnamnet.vn/vn/xa-hoi/209520/sau-chuyen-bay-bi-cham-vi-mot-hanh-khach-dau-bung.html'
        url = 'http://vietnamnet.vn/vn/xa-hoi/209606/roi-thang-may-trong-quan-karaoke-nam-thanh-nien-chet-tham.html'
        url = 'http://vietnamnet.vn/vn/chinh-tri/209728/nghi-tet-am-lich-9-ngay--30-4-6-ngay.html'
        url = 'http://vietnamnet.vn/vn/van-hoa/209551/hoa-hau-viet-nam-nao-dep-nhat-.html'
        url = 'http://vietnamnet.vn/vn/chinh-tri/209609/ong-ba-thanh-tiep-tuc-vang-mat-tiep-xuc-cu-tri.html'
        url = 'http://vietnamnet.vn/vn/xa-hoi/207504/tai-hien-dam-cuoi-cam-dong-voi-ban-gai-da-mat.html'
        url= 'http://vietnamnet.vn/vn/xa-hoi/205900/duong-sat-tren-cao-hn--bat-dong--sau-tai-nan-chet-nguoi.html'
        url = 'http://vietnamnet.vn/vn/kinh-te/209541/can-canh-to-pho--an-het-duoc-thuong-mot-trieu-.html'
        url = 'http://vietnamnet.vn/vn/xa-hoi/209744/hon-12-000-ty-xay-duong-huyet-mach-khu-do-thi-thu-thiem.html'
        url = 'http://vietnamnet.vn/vn/kinh-te/209641/dai-gia-duong-bia--choi-nha-dat-vang-so-mot-viet-nam.html'
        url = 'http://vietnamnet.vn/vn/quoc-te/209695/trieu-tien-ra-tay-de-chan-phim-ve-kim-jong-un-.html'
        mainContent = obj.getPageDetail(url)
        print mainContent
        
        print 'DONE'

