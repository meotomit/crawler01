# -*- coding: utf-8 -*-
import os.path, sys
from time import sleep
sys.path.append(os.path.join(os.path.dirname(os.path.realpath('__file__')), os.pardir))
from bs4 import BeautifulSoup

from sites.ISite import ISite
#import requests
#import urllib2
#import re

from SitesConfig import SITES
import traceback
import re
class vnexpress_net(ISite):
    
    SUFFIX_URL = '.html'
    
    def filterUrl(self, url):
        url = ISite.filterUrl(self, url)
        if url:
            search = re.search("/page/\d+\.html", url)
            if search: # neu la trang paging
                return None
        return url
        
    def getLinks(self, url):
        '''
            Lay danh sach cac trang chi tiet trong 1 trang chuyen muc
        '''
        results = []
        html = self.getHtml(url)
        
        # check category prefix
        if url.find('thethao.vnexpress.net') > 0:
            categoryPrefix = 'http://thethao.vnexpress.net/tin-tuc/'
        else :
            posPaging = url.find('/page/')
            categoryPrefix = url
            if posPaging > 1:
                categoryPrefix = url[:posPaging+1] #
         
        soup = BeautifulSoup(html)
        content = soup.find('div', {'class' : 'block_mid_new'})
        if content:
            links = content.findAll('a')
            for link in links:
                if link.has_attr('href'):                
                    href = link['href']
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
        #mainContent = soup.find('div', {'class' : 'block_col_480'})
        mainContent = soup.find('div', {'class'  :'fck_detail width_common'})
        #mainContent = soup.find('div', {'id' : 'left_calculator'})        
        if mainContent:
            try:
                mainContent = self.filterTags(mainContent)
                #elem1 = mainContent.find('div', {'class' : 'block_timer_share'})
                #elem1.extract()

                #elem2 = mainContent.find('div', {'class' : 'div-fbook width_common title_div_fbook'})
                #elem2.extract()

                text = mainContent.get_text().strip()

                #text = self.filterContent(text)
            except:
                return None
            if text :
                return text
            else:
                print 'Content size < 400 chars or can NOT filter content, URL : ' + pageUrl
                return None
        else :
            print 'can not parse'
            return None

'''
    def run(self):
        # init redis client
        rc = redis.Redis('localhost')
        
        # init mysql client
        conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='16_crawler', cursorclass=DictCursor);
        conn.set_character_set('utf8')
        cursor = conn.cursor()
        
        config = SITES[0]['vnexpress.net']
        print config
        for cate in config:
            try:
                cateUrl = cate['url']
                cateId = cate['cate_id']
                if len(cateUrl) < 10:
                    pass
                print 'Crawling category URL: ', cateUrl
                
                listLinks = self.getLinks(cateUrl)
                print 'Total page: ', len(listLinks)
                
                for detailUrl in listLinks:
                    try:
                        # check URL in redis
                        if rc.sismember(self.QUEUE_DOWNLOADED_URL, detailUrl) == 0:
                            print 'Crawling detail URL: ', detailUrl
                            mainContent = self.getPageDetail(detailUrl)
                            if len(mainContent) > 0:                            
                                print mainContent
                                #TODO: add --> downloaded URL
                                rc.sadd(self.QUEUE_DOWNLOADED_URL, detailUrl)
                                
                            print '-----------------------'
                            sleep(5) # sleep between detail URL
                        else:
                            print 'URL: ' + detailUrl + ' da ton tai'
                    except Exception, e2:
                        print e2.message;
                        tb = traceback.format_exc()
                        print tb
                        pass
                    
                print '=============================='
                sleep(5)    # sleep between category URL
            
            except Exception, e1:
                print e1.message;
                tb = traceback.format_exc()
                print tb
                pass
'''        
if __name__ == '__main__':
        obj = vnexpress_net()
        
        
        # test get urls
        url = 'http://vnexpress.net/tin-tuc/phap-luat'
        url = 'http://thethao.vnexpress.net/'
        url = 'http://giaitri.vnexpress.net/'
        url = 'http://doisong.vnexpress.net/'
        url = 'http://sohoa.vnexpress.net/'
        url = 'http://sohoa.vnexpress.net/tin-tuc/kinh-nghiem'
        url = 'http://kinhdoanh.vnexpress.net/tin-tuc/tien-cua-toi/page/1.html'
        url =  'http://thethao.vnexpress.net/tin-tuc/cac-mon-khac/page/1.html'
        url = 'http://thethao.vnexpress.net/page/2.html'
        url = 'http://thethao.vnexpress.net/tin-tuc/bong-da/la-liga/page/8.html'
        
        listLinks = obj.getLinks(url)
        count = 0
        for link in listLinks:
            count += 1
            print count, link
        
    
        
        # Test get page detail
#       url = 'http://kinhdoanh.vnexpress.net/tin-tuc/doanh-nghiep/khu-vui-choi-tre-em-thi-truong-3-ty-dola-3091745.html'
        url = 'http://vnexpress.net/tin-tuc/phap-luat/ho-so-pha-an/ke-lam-cong-nhot-xac-ba-chu-trong-gieng-3023642.html'
        url = 'http://doisong.vnexpress.net/tin-tuc/suc-khoe/cac-ngoi-sao-mac-chung-tang-dong-thoi-nien-thieu-3089584.html'
        url = 'http://sohoa.vnexpress.net/tin-tuc/cong-dong/hoi-dap/co-6-7-trieu-dong-mua-dien-thoai-2-sim-nao-2979347.html'
        url = 'http://sohoa.vnexpress.net/tin-tuc/doi-song-so/bao-mat/nguy-co-mat-tai-khoan-tu-duong-link-gia-mao-tren-facebook-3093560.html'
        #url = 'http://sohoa.vnexpress.net/tin-tuc/kinh-nghiem/cai-dat-zalo-tren-nokia-asha-503-2979309.html'
        #url = 'http://kinhdoanh.vnexpress.net/tin-tuc/tien-cua-toi/bi-kip-thanh-cong-cua-ty-phu-richard-branson-2965029.html'
        url = 'http://thethao.vnexpress.net/tin-tuc/affcup/malaysia-viet-nam-hien-ngang-vao-hang-hum-3117205.html'
        url = 'http://thethao.vnexpress.net/tin-tuc/giai-ngoai-hang-anh/stoke-city-3-2-arsenal-tro-lai-mat-dat-3117167.html'
        url = 'http://sohoa.vnexpress.net/tin-tuc/san-pham/dien-thoai/philips-ra-mat-bo-ba-smartphone-moi-tai-viet-nam-3116756.html'
        mainContent = obj.getPageDetail(url)
        print mainContent
        

        print 'DONE'

