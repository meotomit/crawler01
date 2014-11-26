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
import time
import logging
'''
    Parse URL 
    Created on Oct 25, 2014
    @author: phuckx
'''
#import logging

FORMATER = '[%(asctime)-15s] - %(message)s'
#FORMATER = '%(asctime)s\t%(process)-6d\t%(levelname)-6s\t%(name)s\t%(message)s'
#logging.basicConfig(level=logging.DEBUG, format=FORMATER,)

QUEUE_URL = 'QUEUE_URL'
    

if __name__ == '__main__':
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_URL, durable=True)
    #channel.queue_declare(queue=QUEUE_ANTI_DUPLICATE, durable=True)    
    # Get content from Queue    
    def callback(ch, method, properties, content):
        logging.info('------------------------------------')
        print ('------------------------------------')
        #print ch
        #print method
        #print properties    
        obj = json.loads(content)
        url = obj['url']
        className = obj['className']
        initCommand = className + "()"
        siteObj = eval(initCommand)
        print url
        print json
        print siteObj
        content = siteObj.getPageDetail(url)
        print content
        
        #push_into_db(obj)        
        ch.basic_ack(delivery_tag=method.delivery_tag)
        #time.sleep(SLEEP_TIME)
        time.sleep(3)    
        
    channel.basic_qos(prefetch_count=1)    
    channel.basic_consume(callback, queue=QUEUE_URL)
    channel.start_consuming()

    #logging.info('DONE')
        