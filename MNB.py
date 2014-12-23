# -*- coding: utf-8 -*-
__author__ = 'Nghiep'

import json
from time import sleep
from DB import DB
import math
import hashlib
from tokenizer.VnTokenizer import VnTokenizer
import logging.handlers

from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics
from operator import itemgetter
from sklearn.metrics import classification_report
import csv
import os
import numpy as np


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

NUM_DOCS = 10735 # Tong so van ban

TABLE = 'site_content_2'
LIST_CATE = [3, 6, 8, 11, 12, 13, 14]
TF_THRESHOLD = 2 # chi lay cac tu co term frequency > 1
WORDS = {} # Nhan tu trong tap du lieu hoc
NUMWORDS = {'total_word': 0}
WORD_INCATE = {}
mapCategoryCounter = {}
NUM_DOCS_IN_CATE = {}

DOC_TRAIN = np.array([])
CLASS_TRAIN = np.array([])

def getWords():
    WINDOW_SIZE = 1000  # so luong item muon fetch
    WINDOW_INDEX = 0
    NUMBER_OF_DOC = 0
    db = DB()
    # STEP 1: tính tổng trọng số của các lớp
    # Đọc toàn bộ db, khi nào ko còn row nào thì thôi
    while True:
        start = WINDOW_SIZE * WINDOW_INDEX  + 1
        stop  = WINDOW_SIZE * (WINDOW_INDEX + 1)
        # things = query.slice(start, stop).all()
        query = "select id, cate_id, tf from " + TABLE + " order by id limit " + str(start) + ", " + str(WINDOW_SIZE)
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
                # print content
                try :
                    mapWeightInDoc = json.loads(content)
                except:
                    continue

                for word in mapWeightInDoc:
                    if(str(type(word)) == '<type \'unicode\'>'):
                        word = word.encode('utf-8')

                    if WORDS.has_key(word) == False:
                        WORDS[word] = 0

            rc.hset('words', 'data', json.dumps(WORDS, ensure_ascii=False, encoding='utf-8'))
        # sleep(2)
        WINDOW_INDEX += 1
    # print WORD_INCATE
    return WORD_INCATE


def convertData():
    print "Converting..."

    WINDOW_SIZE = 10  # so luong item muon fetch
    WINDOW_INDEX = 0
    NUMBER_OF_DOC = 0
    db = DB()
    # STEP 1: tính tổng trọng số của các lớp
    # Đọc toàn bộ db, khi nào ko còn row nào thì thôi
    while True:
        start = WINDOW_SIZE * WINDOW_INDEX  + 1
        stop  = WINDOW_SIZE * (WINDOW_INDEX + 1)
        # things = query.slice(start, stop).all()
        query = "select id, cate_id, tf from " + TABLE + " order by id limit " + str(start) + ", " + str(WINDOW_SIZE)
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
                # print content
                try :
                    mapWeightInDoc = json.loads(content)
                except:
                    continue
                trainItem = np.array([])
                for word in mapWeightInDoc:
                    if WORDS.has_key(word):
                        trainItem = np.append([mapWeightInDoc[word]])
                    else:
                        trainItem = np.append([0])

                DOC_TRAIN = np.append([trainItem])
                trainItem = np.fill(0)
                CLASS_TRAIN = np.append([cateId])
            print CLASS_TRAIN
            return None

def classifier():
    nb = MultinomialNB(alpha=0)
    nb.fit(DOC_TRAIN, CLASS_TRAIN)
    db = DB()
    query = 'select cate_id, tf, url, content from site_content_3'

    cursor = db.cursor()
    logger.info(query)
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        currentCateId = row['cate_id']
        print 'rowID => ', row['cate_id'];
        url = row['url']
        tf = row['tf']
        content = row['content']
        termFrequencyDict = {}
        # continue

        try:
            termFrequencyDict = json.loads(tf)
        except:
            print 'error => ', url
            continue

        testItem = np.array([])
        for word in termFrequencyDict:
            tf = termFrequencyDict[word]
            if WORDS.has_key(word):
                testItem = np.append([tf])
            else:
                testItem = np.append([0])

        print "CURRENT CATE ", currentCateId
        print "NEW ", nb.predict(testItem)


if __name__ == '__main__':
    getWords()
    print 'MultinomialNB'
    convertData()
