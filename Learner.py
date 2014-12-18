# -*- coding: utf-8 -*-
'''
Created on Dec 3, 2014

@author: phuckx
'''
import json
from time import sleep
from DB import DB    
import traceback

import logging.handlers
from tokenizer.VnTokenizer import VnTokenizer
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
import math
import redis
rc = redis.Redis('localhost')

NUM_DOCS = 10735
#NUM_WORDS = 95328 # so word trong TF (ko loai nhung tu co TF > 0)
#NUM_WORDS = 31945 # so word trong TF (ko loai nhung tu co TF > 1)
#NUM_WORDS = 19432 # so word trong TF (ko loai nhung tu co TF > 1)
# NUM_WORDS = 4863  # so word trong TF > 8

TABLE = 'site_content_2'
LIST_CATE = [3, 6, 8, 11, 12, 13, 14]
WORDS = {}
NUMWORDS = {'a': 0}

'''
    Tinh document frequency (DF)
'''    
def countDF():
    db = DB()
    WINDOW_SIZE = 1000  # so luong item muon fetch
    WINDOW_INDEX = 0
    while True:
        start = WINDOW_SIZE * WINDOW_INDEX  + 1
        stop  = WINDOW_SIZE * (WINDOW_INDEX + 1)
        # things = query.slice(start, stop).all()
        query = "select id, cate_id, tf from " + TABLE + " order by id limit " + str(start) + ", " + str(WINDOW_SIZE)
        logger.info(query)
        sleep(2)
        
        cursor = db.cursor()
        logger.info(query)
        cursor.execute(query)
        rows = cursor.fetchall()
        #import pdb
        #pdb.set_trace()
            
        if rows == None or len(rows) == 0:
            logger.info("Query size: 0")
            break
        else:
            logger.info("Query size: " + str(len(rows)))
            
            for row in rows:
                content = row['tf']
                docId = row['id']
                cateId = int(row['cate_id'])
                try :
                    wordsObj = json.loads(content)
                    #print 'Total words: ' + str(len(wordsObj))
                    for word in wordsObj:
                        tf = int(wordsObj[word])   
                        if tf > TF_THRESHOLD :                
                            #print word, ' : ', tf
                            pipe = rc.pipeline()
                            pipe.multi()
                            if isinstance(word, unicode):
                                word = word.encode('utf-8')
                            pipe.hincrby("total_cate_weight", cateId, tf) # tính tổng trọng số của các từ thuộc vào cate
                            pipe.hincrby("word_cate", word + "|" +str(cateId), tf) # tính tổng trọng số của từng từ trong một cate
                            pipe.hincrby("DF", word, 1)
                            pipe.hset("TF", word, tf)
                            pipe.hset('CATE', word, cateId) # xac dinh word thuoc cate nao
                            pipe.execute()
                            if WORDS.has_key(word) == False:
                                WORDS[word] = 1
                                NUMWORDS['a'] += 1
                except:
                    logger.error('Error in DOC_ID: ' + str(docId))
                    tb = traceback.format_exc()
                    logging.error(tb)
        WINDOW_INDEX += 1
    logger.info('Done counting DF')



def countTF_IDF():
    count = 0
    pipe = rc.pipeline()
    pipe.multi()
    for word in rc.hkeys("DF"):
        
        tf = float(rc.hget("TF", word))
        df = float(rc.hget("DF", word))
        
        #import pdb
        #pdb.set_trace()
        #tfidf = (1 + math.log10(tf)) * math.log10(NUM_DOCS / df)
        tfidf = tf * (1 + math.log10(NUM_DOCS / (df + 1)))
        #tfidf2 = (1 + math.log10(tf)) * math.log10(NUM_DOCS / df)
        #print word
        #print 'TF: ', tf
        #print 'DF: ' + str(df)
        #print 'TF_IDF: ' + str(tfidf)
        #print 'TF_IDF: ' + str(tfidf2)
        #print '-------------'
        
        pipe.hset("TF_IDF", word, tfidf)
        count += 1
        #if count > 24:
        #    break
        if count % 1000 == 0:
            pipe.execute()
            print 'Total : ', count
    pipe.execute()
    print count

    
'''
    Tính trọng số tổng của cả cate
'''
def countTotalWeightInCate():
    listWords = rc.hgetall('CATE')
    count= 1
    for word in listWords:
        count += 1
        if count > 10:
            break
        print word
        print listWords[word]
        
        #print value    

'''
Tinh xac xuat tung chuyen muc
'''
def countPC():
    db = DB()
    query = 'select cate_id, count(cate_id) total_item from ' + TABLE + ' group by cate_id'
    cursor = db.cursor()
    logger.info(query)
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        cateId = row['cate_id']
        totalItem = row['total_item']
        pc = float(totalItem) / NUM_DOCS
        rc.hset("PC", cateId, pc)
    print 'Count PC --> DONE'

'''
    Tinh xac xuat XkCi
'''
def PXkCi():
    #for cateId in (3,6,8,11,12,13,14):
    #    print cateId
    mapCateWeight = rc.hgetall('total_cate_weight')
    print mapCateWeight
    count = 0
    pipe = rc.pipeline()
    pipe.multi()
    
    for key in rc.hkeys('word_cate'):
        count += 1
        #if count > 10:
        #    break
        #print key
        word = key.split('|')[0]
        cate = key.split('|')[1]
        #print word
        #print cate
        wordWeightInCate = rc.hget('word_cate', key)
        #print mapCateWeight[cate]
        #print wordWeightInCate 
        
        #pxkci = float(wordWeightInCate) / float(mapCateWeight[cate])
        NUM_WORDS = NUMWORDS['a']
        pxkci = float(int(wordWeightInCate) + 1) / float(int(mapCateWeight[cate]) + NUM_WORDS)    # --> laplace
        print pxkci
        print '---------------'
        #import pdb
        #pdb.set_trace()
        pipe.hset('pxkci_2', key, pxkci)
        if count % 1000 == 0:
            pipe.execute()
            print count
    
    pipe.execute()
    print count 
    print 'Count PXkCi --> Done'

def predictor():
    import codecs, os
    stopwordsFile = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/data/test.txt')
    stopwordsFile = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/data/thethao.txt')
    f = codecs.open(stopwordsFile, encoding='utf-8', mode='r')
    content = f.read()
    f.close()
    tokenizer = VnTokenizer()
    tokenContent = tokenizer.tokenize(content)
    
    words = tokenContent.split()
    termFrequencyDict = {}
    
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
    NUM_WORDS = NUMWORDS['a']
    print 'NUM_WORDS => ', NUM_WORDS
    print termFrequencyDict
    mapResult = {}
    # tinh xac xuat tung cate
    for cateId in LIST_CATE:
        pc = float(rc.hget('PC', cateId))
        pcateNew = pc
        print 'CateID: ', cateId
        print 'PC : ', pc
        for word in termFrequencyDict:
            tf = termFrequencyDict[word]
            
            pxkci = rc.hget('pxkci_2', word + "|" + str(cateId))
            #print word
            #print 'PXkCi: ', pxkci
            #print 'TF: ', tf
            #import pdb
            #pdb.set_trace()
            if not pxkci:
                pxkci = 0
            else:
                pxkci = float(pxkci)
            if (pxkci != 0):
                #import pdb
                #pdb.set_trace()
                pcateNew = pcateNew + math.log10(tf * pxkci)
                #print pcateNew

        pcateNew = math.fabs(pcateNew)
        mapResult[cateId] = pcateNew
        #import pdb
        #pdb.set_trace()
        print 'Cate: ', cateId, ' --> ', float(pcateNew)
        print '--------------------------------'
        #mapResult[cateId : pcateNew]
    
    # check max

    max = 0
    cateMax = 0
    for cate in mapResult:
        # print cate
        if mapResult[cate] > max:
            max = mapResult[cate]
            cateMax = cate
    print 'Result: '
    print cateMax
    print max 

    
    #print content2
    
if __name__ == '__main__':
    
    # Step 1: Tinh DF
    countDF()
    
    # Step 2: Tinh TF_IDF    --> ko can neu ko tinh theo TF_IDF
    #https://lucene.apache.org/core/4_0_0/core/org/apache/lucene/search/similarities/TFIDFSimilarity.html
    countTF_IDF()
    
    # Step 3 --> ko can neu ko tinh theo TF_IDF
    countTotalWeightInCate()
    
    # Step 
    PXkCi()
    
    # step 
    countPC()
    
    # step
    predictor()
    

    print 'DONE'
