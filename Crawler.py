# -*- coding: utf-8 -*-
import os.path, sys
from time import sleep
sys.path.append(os.path.join(os.path.dirname(os.path.realpath('__file__')), os.pardir))
from sites.ISite import ISite
from SitesConfig import SITES
from sites.dantri_com_vn import dantri_com_vn
from sites.vnexpress_net import vnexpress_net
from sites.nongnghiep_vn import nongnghiep_vn
from sites.tuoitre_vn import tuoitre_vn
import pika
import json
'''
Created on Oct 25, 2014

@author: phuckx
'''
import logging

#FORMATER = '[%(asctime)-15s] - %(message)s'
#FORMATER = '%(asctime)s\t%(process)-6d\t%(levelname)-6s\t%(name)s\t%(message)s'
#logging.basicConfig(level=logging.DEBUG, format=FORMATER,)

import logging.handlers
formatter = logging.Formatter('%(asctime)s\t%(process)-6d\t%(levelname)-6s\t%(name)s\t%(message)s')

logger = logging.getLogger('CRAWLER')

logger.setLevel(logging.DEBUG)
file_handler = logging.handlers.RotatingFileHandler('logs/crawl_url.txt', 'a', 5000000, 5) # 5M - 5 files
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

#logger.addHandler(file_handler) 
logger.addHandler(console_handler)

logging.getLogger('pika').setLevel(logging.INFO)
logging.getLogger('pika.frame').setLevel(logging.INFO)


QUEUE_URL = 'QUEUE_URL'

import re

if __name__ == '__main__':
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_URL, durable=True)
    #channel.queue_declare(queue=QUEUE_ANTI_DUPLICATE, durable=True)

    MULTI_URL_REGEX = re.compile('.*?\$\{(\d+\-\d+)\}\.html')
    
    for site in SITES:
        for siteName in site:
            #print '==========================='
            #print siteName
            #print '==========================='
            for cate in site[siteName]:
                cateId = cate['cate_id']
                cateUrl = cate['url']
                className = cate['class']
                #logging.info("URL: " + cateUrl)
                cateUrl = cateUrl.strip()
                if len(cateUrl) > 0:
                    listCateUrls = []
                    
                    # check multi URL
                    matches = MULTI_URL_REGEX.match(cateUrl)
                    if matches:                        
                        pageRangeStr = matches.group(1)
                        pageRangeArr = pageRangeStr.split('-')
                        for p in range(int(pageRangeArr[0]), int(pageRangeArr[1])):
                            url = re.sub(r'\$\{\d+\-\d+\}', str(p), cateUrl)
                            print url
                            listCateUrls.append(url)
                    else:
                        listCateUrls.append(cateUrl)
                                        
                    initCommand = className + "()"
                    siteObj = eval(initCommand)
                    #print siteObj
                    
                    for tmpCateUrl in listCateUrls:
                        links = siteObj.getLinks(tmpCateUrl)
                        logger.info('Total link: ' + str(len(links)) + ' in category: ' + tmpCateUrl)
                        for link in links:
                            logging.info(link)
                            urlInfo = {'className' : className, 'cateId' : cateId, 'cateUrl' : tmpCateUrl, 'url' : link}
                            content = json.dumps(urlInfo)
                            #Push to queue
                            channel.basic_publish(exchange='',
                                          routing_key=QUEUE_URL,
                                          body=content,
                                          properties=pika.BasicProperties(delivery_mode=2, # make message persistent
                                     ))
                        sleep(3)
                    #logging.info('-----------------------')

    #logging.info('DONE')
        