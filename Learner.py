# -*- coding: utf-8 -*-
'''
Created on Dec 3, 2014

@author: phuckx
'''
import json
from time import sleep
from DB import DB    

import logging.handlers
formatter = logging.Formatter('%(asctime)s\t%(process)-6d\t%(levelname)-6s\t%(name)s\t%(message)s')

logger = logging.getLogger('CRAWLER')

logger.setLevel(logging.DEBUG)
file_handler = logging.handlers.RotatingFileHandler('logs/leraner.txt', 'a', 5000000, 5)  # 5M - 5 files
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler) 
logger.addHandler(console_handler)

logging.getLogger('pika').setLevel(logging.INFO)
logging.getLogger('pika.frame').setLevel(logging.INFO)

# Load URL --> redis
import redis
rc = redis.Redis('localhost')


if __name__ == '__main__':
    
    WINDOW_SIZE = 1000  # so luong item muon fetch
    WINDOW_INDEX = 0
    db = DB()
    
    # Tính total mỗi cate
    #Lớp C1 = “Comp” --> Tổng = 208
        
    mapCategoryCounter = {}
    
    # STEP 1: tính tổng trọng số của các lớp
    # Đọc toàn bộ db, khi nào ko còn row nào thì thôi    
    while True:
        start = WINDOW_SIZE * WINDOW_INDEX  + 1
        stop  = WINDOW_SIZE * (WINDOW_INDEX + 1)
        # things = query.slice(start, stop).all()
        query = "select cate_id, tf from site_content order by id limit " + str(start) + ", " + str(WINDOW_SIZE)
        logger.info(query) 
        
        cursor = db.cursor()
        logger.info(query)
        cursor.execute(query)
        rows = cursor.fetchall()
        #import pdb
        #pdb.set_trace()
            
        if rows == None or len(rows) == 0:
            break
        else:
            logger.info("Query size: " + str(len(rows)))
            
            for row in rows:
                content = row['tf']
                cateId = int(row['cate_id'])
                totalWeightInCate = 0
                
                mapWeightInDoc = json.loads(content)
                for word in mapWeightInDoc:
                    print word, ' : ', mapWeightInDoc[word]
                    totalWeightInCate += mapWeightInDoc[word]
                
                if mapCategoryCounter.has_key(cateId) :
                    mapCategoryCounter[cateId] = mapCategoryCounter[cateId] +  totalWeightInCate
                else:
                    mapCategoryCounter[cateId] =  totalWeightInCate
                print len(mapWeightInDoc)
                print '-------------------'
        sleep(2)
        WINDOW_INDEX += 1
        
    print mapCategoryCounter
    
    #STEP2: tính xác xuất P(Xk|Ci)
    # total Comp = 208
    # P(val|Comp) = (10 + 11 + 8) / 208 = 29/208 
    
    
    print 'DONE'
