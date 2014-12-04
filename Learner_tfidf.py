# -*- coding: utf-8 -*-
'''
Created on Dec 3, 2014

@author: phuckx
'''
import json
from time import sleep
from DB import DB
import math

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

def checkKeyword(keyword, docId):
    query = "select id from keyword WHERE keyword='%s' AND doc_id = %s" % (keyword, docId)
    logger.info(query)
    cursor = db.cursor()
    logger.info(query)
    cursor.execute(query)
    rows = cursor.fetchall()
    # cursor.close()
    # print rows
    if rows == None or len(rows) == 0:
        return False
    else:
        return True

def increaseDi(keyword):
    query = "UPDATE keyword SET di = di + 1 WHERE keyword='%s'" %(keyword)
    logger.info(query)
    cursor = db.cursor()
    logger.info(query)
    cursor.execute(query)
    db.conn.commit()
    # cursor.close()

def updateTfidf(id, tfidf):
    query = "UPDATE site_content SET tf_idf = '%s' WHERE id=%s" %(tfidf, id)
    # logger.info(query)
    cursor = db.cursor()
    cursor.execute(query)
    db.conn.commit()

def checkKeywordRedis(keyword):
    query = "select id from keyword WHERE keyword='%s' AND doc_id = %s" % (keyword, docId)
    logger.info(query)
    cursor = db.cursor()
    logger.info(query)
    cursor.execute(query)
    rows = cursor.fetchall()
    # cursor.close()
    # print rows
    if rows == None or len(rows) == 0:
        return False
    else:
        return True

def increaseDi(keyword):
    query = "UPDATE keyword SET di = di + 1 WHERE keyword='%s'" %(keyword)
    logger.info(query)
    cursor = db.cursor()
    logger.info(query)
    cursor.execute(query)
    # db.conn.commit()
    cursor.close()

def insertKeyword(keyword, docId, tf):
    if checkKeyword(keyword, docId) == True:
        query = "UPDATE keyword SET tf = %s WHERE keyword='%s' AND doc_id = %s" %(tf, keyword, docId)
        cursor = db.cursor()
        logger.info(query)
        cursor.execute(query)
        db.conn.commit()
        # cursor.close()
        increaseDi(keyword)
    else:
        query = "INSERT INTO keyword(keyword, doc_id, tf, di) VALUES('%s', %s, %s, 1)" %(keyword, docId, tf)
        cursor = db.cursor()
        logger.info(query)
        cursor.execute(query)
        db.conn.commit()
        # cursor.close()


if __name__ == '__main__':
    
    WINDOW_SIZE = 1000  # so luong item muon fetch
    WINDOW_INDEX = 0
    db = DB()
    
    # Tính total mỗi cate
    #Lớp C1 = “Comp” --> Tổng = 208
        
    mapCategoryCounter = {}
    NUMBER_OF_DOC = 0
    
    # STEP 1: tính tổng trọng số của các lớp
    # Đọc toàn bộ db, khi nào ko còn row nào thì thôi    
    while True:
        start = WINDOW_SIZE * WINDOW_INDEX  + 1
        stop  = WINDOW_SIZE * (WINDOW_INDEX + 1)
        # things = query.slice(start, stop).all()
        query = "select id, cate_id, tf from site_content order by id limit " + str(start) + ", " + str(WINDOW_SIZE)
        logger.info(query) 
        
        cursor = db.cursor()
        # logger.info(query)
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
                cateId = row['cate_id']
                docId = row["id"]
                mapWeightInDoc = json.loads(content)
                NUMBER_OF_DOC = NUMBER_OF_DOC + 1
                for word in mapWeightInDoc:

                    if mapCategoryCounter.has_key(word) :
                        mapCategoryCounter[word] = mapCategoryCounter[word] +  1
                    else:
                        mapCategoryCounter[word] =  1

                    # print mapCategoryCounter
                    # tf = int(mapWeightInDoc[word])
                    # print docId, " --> ", word, ' : ', tf
                    # insertKeyword(word, docId, tf)
                    # print docId, " --> ", word, ' : ', tf


                #
                # totalWeightInCate = 0
                #
                # mapWeightInDoc = json.loads(content)
                # for word in mapWeightInDoc:
                #     print word, ' : ', mapWeightInDoc[word]
                #     totalWeightInCate += mapWeightInDoc[word]
                #
                # if mapCategoryCounter.has_key(cateId) :
                #     mapCategoryCounter[cateId] = mapCategoryCounter[cateId] +  totalWeightInCate
                # else:
                #     mapCategoryCounter[cateId] =  totalWeightInCate
                # print len(mapWeightInDoc)
                # print mapCategoryCounter
                print '-------------------'
        # sleep(2)
        WINDOW_INDEX += 1


    WINDOW_INDEX = 0;

    while True:
        start = WINDOW_SIZE * WINDOW_INDEX  + 1
        stop  = WINDOW_SIZE * (WINDOW_INDEX + 1)
        # things = query.slice(start, stop).all()
        query = "select id, cate_id, tf from site_content order by id limit " + str(start) + ", " + str(WINDOW_SIZE)
        logger.info(query)

        cursor = db.cursor()
        # logger.info(query)
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows == None or len(rows) == 0:
            break
        else:
            for row in rows:
                content = row['tf']
                cateId = row['cate_id']
                docId = row["id"]
                mapWeightInDoc = json.loads(content)
                allTfidf = {}
                for word in mapWeightInDoc:
                    tf = int(mapWeightInDoc[word])
                    tfidf = (1 + math.log10(tf)) * math.log10(NUMBER_OF_DOC / mapCategoryCounter[word])
                    allTfidf[word] = tfidf
                    tfidfJson = json.dumps(allTfidf, ensure_ascii=False, encoding='utf-8')
                    # print tfidf

                updateTfidf(docId, tfidfJson)
        WINDOW_INDEX += 1
    # print mapCategoryCounter
    
    #STEP2: tính xác xuất P(Xk|Ci)
    # total Comp = 208
    # P(val|Comp) = (10 + 11 + 8) / 208 = 29/208 
    
    
    print 'DONE'
