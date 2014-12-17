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
CATE_TITLE = {3: 'Kinh Te- Tai chinh', 6: 'Doi song, nghe thuat, giai tri', 8: 'Y hoc suc khoe', 11: 'Xa hoi, van hoa', 12: 'The thao', 13 : 'Cong nghe', 14: 'Oto - xe may'}
TF_THRESHOLD = 1 # chi lay cac tu co term frequency > 1
#WORDS = {}
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
                    count = 0
                    pipe = rc.pipeline()
                    pipe.multi()
                            
                    for word in wordsObj:
                        tf = int(wordsObj[word])   
                        if tf > TF_THRESHOLD :                
                            #print word, ' : ', tf
                            
                            if isinstance(word, unicode):
                                word = word.encode('utf-8')
                            #pipe.hincrby("total_cate_weight", cateId, tf) # tính tổng trọng số của các từ thuộc vào cate
                            #pipe.hincrby("word_cate", word + "|" +str(cateId), tf) # tính tổng trọng số của từng từ trong một cate
                            pipe.hincrby("DF", word, 1) # số văn bản mà từ này xuất hiện
                            pipe.hset("TF", word, tf)
                            pipe.sadd("CATE_" + str(cateId), word) # Thêm word vào cate --> để sau này check xem word có thuộc cate hay không
                            #pipe.hset('CATE', word, cateId) # xac dinh word thuoc cate nao
                            count += 1
                            #pipe.execute()
                            if count % 1000 == 0:
                                pipe.execute()
                                #print 'sleep ...'
                                #sleep(3)
                            '''
                            if WORDS.has_key(word) == False:
                                WORDS[word] = 1
                                NUMWORDS['a'] += 1
                            '''
                    pipe.execute()
                except:
                    logger.error('Error in DOC_ID: ' + str(docId))
                    tb = traceback.format_exc()
                    logging.error(tb)
        WINDOW_INDEX += 1
    logger.info('Done counting TF, DF')

'''
    Tinh trong so cua cac tu theo TF_IDF
'''
'''
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
        
        #tfidf = tf * (1 + math.log10(NUM_DOCS / (idf + 1)))
        
        tfidf = (1 + math.log10(tf)) * math.log10(NUM_DOCS / df)
        
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
    
'''
    Tính trọng số tổng của cả cate
'''
def countTotalWeightInCate():
    #mapTfIdf = rc.hgetall('TF_IDF')
    mapTfIdf = rc.hgetall('TF') # tinh theo TF, ko tinh theo TF_IDF nua
    count= 1
    pipe = rc.pipeline()
    pipe.multi()
    
    for word in mapTfIdf:
        tfidf = float(mapTfIdf[word])
        #print tfidf
        for cateId in LIST_CATE:
            #print cateId
            #print word
            #print redisKey
            #print tfidf # trong so cua tu
            #print rc.sismember("CATE_" + str(cateId), word)
            #print '--------------'
            pipe.hincrbyfloat("WEIGHT_CATE", "CATE_" + str(cateId), tfidf) # total weight of word in cate
            
            if rc.sismember("CATE_" + str(cateId), word): # neu word la member cua cateId
                pipe.hincrbyfloat("WEIGHT_WORD_CATE", word + "|" + str(cateId) , tfidf) # total weight of word in cate               
        count += 1
        if count % 1000 == 0:
            pipe.execute()
            print 'Count: ', count
    print 'Count: ', count
    pipe.execute()    

'''
    Tinh xac xuat XkCi
'''
def PXkCi():
    #for cateId in (3,6,8,11,12,13,14):
    #    print cateId
    #(là tổng trọng số của từ A trong cate C1 + 1 )/ (tổng trọng số của các từ trong cate C1 + số từ trong văn bản)
    
    mapWeightCate = rc.hgetall('WEIGHT_CATE')
    mapWeightWordCate = rc.hgetall('WEIGHT_WORD_CATE')
    count = 0
    pipe = rc.pipeline()
    pipe.multi()
    
    totalWord = rc.hlen("TF")
    
    for cateId in LIST_CATE:
        mapWordInCate = rc.smembers("CATE_" + str(cateId))
        weightCate = mapWeightCate["CATE_" + str(cateId)] # total weight of cate
        for word in mapWordInCate:
            key = word + "|" + str(cateId)
            totalWeightOfWordInCate = float(mapWeightWordCate[key])            
            pxkci = float( totalWeightOfWordInCate + 1) / float( float(weightCate) + totalWord)
            count += 1
            #pxkci = float(int(wordWeightInCate) + 1) / float(int(mapCateWeight[cate]) + NUM_WORDS)        # --> laplace
            #print pxkci
            #print '---------------'
        
            pipe.hset('pxkci', key, pxkci)
            if count % 1000 == 0:
                pipe.execute()
                print count
        
    pipe.execute()
    print count 
    print 'Count PXkCi --> Done'

'''
Tinh xac xuat tung chuyen muc
'''
def countProbabilityOfCategory():
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
    print 'Count Probability of each Category --> DONE'

def predictor():
    import codecs, os
    stopwordsFile = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/data/test.txt')
    stopwordsFile = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/data/stopwords.txt')
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
    
    # tính tf*idf cho document mới
    for word in termFrequencyDict:
        print word
        if type(word) == unicode:
            word = word.encode('utf-8')
        tf = termFrequencyDict[word]
    
    # tinh xac xuat tung cate
    for cateId in LIST_CATE:
        pc = float(rc.hget('PC', cateId))
        pcateNew = math.log10(pc)
        print 'CateID: ', cateId
        #print 'PC : ', pc
        #print 'PC : ', pcateNew
        for word in termFrequencyDict:
            tf = termFrequencyDict[word]
            
#             oldTf = rc.hget("TF", word)
#             oldDf = rc.hget("DF", word)
#             if oldTf != None and oldDf != None:     
#                 oldTf = float(oldTf)
#                 oldDf = float(oldDf)
                #tfidf = (1 + math.log10(tf)) * math.log10(NUM_DOCS / df)            
                #tfidf = tf * (1 + math.log10(NUM_DOCS / (idf + 1)))            
                #tfidf = (1 + math.log10(tf + oldTf)) * math.log10(NUM_DOCS / (oldDf + 1))            
            pxkci = rc.hget('pxkci', word + "|" + str(cateId))
            if not pxkci:
                pxkci = 0
            else:
                pxkci = float(pxkci)
            if (pxkci != 0):
                #pcateNew = pcateNew + math.log10(tfidf * pxkci)
                pcateNew = pcateNew + math.log10(tf * pxkci)
                #print pcateNew

        pcateNew = math.fabs(pcateNew)
        print pcateNew
        mapResult[cateId] = pcateNew
        #import pdb
        #pdb.set_trace()
        print 'Cate: ', cateId, ' --> ', float(pcateNew)
        
        print '--------------------------------'
        #mapResult[cateId : pcateNew]
    
    # check max

    max = -9999999999
    cateMax = 0
    for cate in mapResult:
        # print cate
        if mapResult[cate] > max:
            max = mapResult[cate]
            cateMax = cate
    print 'Result: '    
    print cateMax
    print max
    print CATE_TITLE[cateMax] 
    

    
    #print content2
    
if __name__ == '__main__':
    
    # Step 1: Tinh DF
    #countDF()
    
    # Step 2: Tinh TF_IDF    --> ko can neu ko tinh theo TF_IDF
    #https://lucene.apache.org/core/4_0_0/core/org/apache/lucene/search/similarities/TFIDFSimilarity.html
    #countTF_IDF()
    
    # Step 3 --> ko can neu ko tinh theo TF_IDF
    #countTotalWeightInCate()
    
    
    # Step 
    #PXkCi()
    
    # step 
    #countProbabilityOfCategory()
    
    # step
    predictor()
    
    
    '''
    WINDOW_INDEX = 0
    WINDOW_SIZE = 1000  # so luong item muon fetch
    
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
    
    '''
    print 'DONE'
