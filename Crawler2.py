# -*- coding: utf-8 -*-
import os.path, sys
from time import sleep
from string import lower
sys.path.append(os.path.join(os.path.dirname(os.path.realpath('__file__')), os.pardir))
from sites.ISite import ISite
from SitesConfig import SITES
from sites.dantri_com_vn import dantri_com_vn
from sites.vnexpress_net import vnexpress_net
from sites.nongnghiep_vn import nongnghiep_vn
from sites.tuoitre_vn import tuoitre_vn
from tokenizer.VnTokenizer import VnTokenizer

import pika
import json
import time
import logging
import traceback  
import os

import json

'''
    Parse URL 
    Created on Oct 25, 2014
    @author: phuckx
'''
#import logging

#FORMATER = '[%(asctime)-15s] - %(message)s'
#FORMATER = '%(asctime)s\t%(process)-6d\t%(levelname)-6s\t%(name)s\t%(message)s'
#logging.basicConfig(level=logging.INFO, format=FORMATER,)
import logging.handlers
formatter = logging.Formatter('%(asctime)s\t%(process)-6d\t%(levelname)-6s\t%(name)s\t%(message)s')

logger = logging.getLogger('CRAWLER')

logger.setLevel(logging.DEBUG)
file_handler = logging.handlers.RotatingFileHandler('logs/log.txt', 'a', 5000000, 5) # 5M - 5 files
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

#logger.addHandler(file_handler) 
logger.addHandler(console_handler)

logging.getLogger('pika').setLevel(logging.INFO)
logging.getLogger('pika.frame').setLevel(logging.INFO)

QUEUE_URL = 'QUEUE_URL'

from DB import DB    

# Load URL --> redis
import redis
rc = redis.Redis('localhost')

'''
Load các URL đã crawler vào Redis để cache
'''
def loadURL2Redis():
    query1 = "select id, site, url from visited_url"
    db = DB()   
    cursor = db.cursor()
    logger.info(query1)
    cursor.execute(query1)
    rows = cursor.fetchall()
    for row in rows:
        site = row['site']
        url = row['url']    
        rc.sadd(site, url)
    logger.info('Load : ' + str(len(rows)) + ' to Redis')

'''
    Insert URL đã crawl được vào database và Redis
'''           
def insertUrl(site, url):
    query = "insert into visited_url (site, url) values( '%s', '%s') " % (site, url)
    logger.info(query)
    db = DB()
    cur = db.cursor()
    cur.execute(query)
    db.conn.commit()
    
    # add --> Redis    
    if rc.sadd(site, url) == 0:
        logger.error("Insert URL " + url + " to Redis --> Failed")
    
'''
    Ktra một URL đã được crawl hay chưa bằng cách check trong Redis
'''    
def existURL(siteName, url):
    res = True
    if rc.sismember(siteName, url) == 0:
        res = False
    return res

if __name__ == '__main__':
    
    logger.info('Load URL --> Redis')
    loadURL2Redis()    
    logger.info('Load URL --> Redis ==> OK')
    
    db = DB()

    tokenizer = VnTokenizer()
    print 'STOP WORDS: ' + str(len(tokenizer.STOP_WORDS))
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_URL, durable=True)
    
    #channel.queue_declare(queue=QUEUE_ANTI_DUPLICATE, durable=True)    
    # Get content from Queue    
    def callback(ch, method, properties, content):
        logger.info('------------------------------------')
        try :
            #print ch
            #print method
            #print properties    
            obj = json.loads(content)
            cateId = obj['cateId']
            #siteName = obj['className']
            url = obj['url']
            className = obj['className']
            initCommand = className + "()"
            siteObj = eval(initCommand)
            logger.info(url)
            
            termFrequencyDict = {} 
            
            #TODO: check URL da dc crawl hay chua
            if not existURL(className, url):
                content = siteObj.getPageDetail(url)
                if content:
                    # Tokenizing
                    tokenContent = tokenizer.tokenize(content)
                    words = tokenContent.split()
                    filterWords = []
                    for word in words:     
                        word = word.strip()
                        #check stop word
                        
                        # change to lower case
                        if isinstance(word, str): 
                            word = unicode(word, 'utf-8').lower().encode('utf-8')
                        else:
                            word = word.lower()
                                                                    
                        if not tokenizer.isStopWord(word):
                            filterWords.append(word)
                            
                            # check term freq
                            #word = word.encode('utf-8')
                            #print type(word)
                            if termFrequencyDict.has_key(word):
                                curCounter = termFrequencyDict.get(word)
                                termFrequencyDict[word] = curCounter + 1
                            else:
                                termFrequencyDict[word] = 1
                    #print json.dumps(termFrequency, sort_keys=True, indent=4, separators=(',', ': '))
                    termFrequencyJson = json.dumps(termFrequencyDict, ensure_ascii=False, encoding='utf-8')
                    logger.info(termFrequencyJson)
                    
                    # join --> string
                    filterContent = ' '.join(filterWords)
                    
                    #import pdb
                    #pdb.set_trace()
                    content = content.replace("'", "\\'")
                    tokenContent = tokenContent.replace("'", "\\'")
                    filterContent = filterContent.replace("'", "\\'")
                    
                    query = "INSERT INTO site_content (cate_id, site, url, content, word_1, word_2, tf) values (%s, '%s', '%s', '%s', '%s', '%s', '%s')" % \
                            (str(cateId), className.encode('utf-8'), url.encode('utf-8'), content.encode('utf-8'), tokenContent, filterContent, termFrequencyJson)
                    cur = db.cursor()
                    cur.execute(query)
                    db.conn.commit()
                    
                    # insert --> visited URL
                    insertUrl(className, url)
                                        
            
            ch.basic_ack(delivery_tag=method.delivery_tag)
            #time.sleep(SLEEP_TIME)
            time.sleep(3)    
        except:
            tb = traceback.format_exc()
            logging.error(tb)
    channel.basic_qos(prefetch_count=1)    
    channel.basic_consume(callback, queue=QUEUE_URL)
    channel.start_consuming()

    #logging.info('DONE')
        