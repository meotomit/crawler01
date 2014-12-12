# -*- coding: utf-8 -*-
'''
Created on Dec 3, 2014

@author: phuckx
'''
import json
from time import sleep
from DB import DB
import math
import hashlib
from tokenizer.VnTokenizer import VnTokenizer
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

NUM_DOCS = 10735
#NUM_WORDS = 95328 # so word trong TF (ko loai nhung tu co TF > 0)
#NUM_WORDS = 31945 # so word trong TF (ko loai nhung tu co TF > 1)
#NUM_WORDS = 19432 # so word trong TF (ko loai nhung tu co TF > 1)
# NUM_WORDS = 4863  # so word trong TF > 8

TABLE = 'site_content_2'
LIST_CATE = [3, 6, 8, 11, 12, 13, 14]
TF_THRESHOLD = 8 # chi lay cac tu co term frequency > 1
WORDS = {}
NUMWORDS = {'total_word': 0}
WORD_INCATE = {}
mapCategoryCounter = {}
NUMBER_OF_DOC = 0

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

def existKey(key):
    res = True
    if rc.exists(key) == 0:
        res = False
    return res

def pushTfIdf(word, docId, tf, idf, tfidf, cateId = None):

    hashKey = "%s_%s" %(hashlib.sha1(word.encode('utf-8')).hexdigest(), docId)
    hashKeyWordCate = "%s_%s" %(hashlib.sha1(word.encode('utf-8')).hexdigest(), cateId)
    totalWeightCate = "weight_%s" %(cateId)


    #Tong trong so cac tu trong cate
    if(WORD_INCATE.has_key(totalWeightCate) != True):
        WORD_INCATE[totalWeightCate] = tf
    else:
        WORD_INCATE[totalWeightCate] += tf

    if(WORD_INCATE.has_key(hashKeyWordCate) != True):
        WORD_INCATE[hashKeyWordCate] = tf #Trọng số của từ voi lan xuat hien dau tiên trong cate
        if(WORD_INCATE.has_key(cateId)):
            WORD_INCATE[cateId] += 1
        else:
            WORD_INCATE[cateId] = 1
    else:
        WORD_INCATE[hashKeyWordCate] += tf #Trong so cua tu do voi lan xuat hien tiep theo trong cate

    pipe = rc.pipeline()
    pipe.multi()
    if existKey(hashKey):
        pipe.hdel(hashKey, 'tf')
        pipe.hdel(hashKey, 'idf')
        pipe.hdel(hashKey, 'tfidf')

    if(existKey(hashKey) != True):
        pipe.hset(hashKey, 'tf', tf)
        pipe.hset(hashKey, 'idf', idf)
        pipe.hset(hashKey, 'tfidf', tfidf)

    pipe.execute()

    # print hashKey, 'tf', rc.hget(hashKey, 'tf')
    # print hashKey, 'idf', rc.hget(hashKey, 'idf')
    # print hashKey, 'tfidf', rc.hget(hashKey, 'tfidf')

def calTfIdf():
    WINDOW_SIZE = 1000  # so luong item muon fetch
    WINDOW_INDEX = 0
    NUMBER_OF_DOC = 0
    # Tính total mỗi cate
    #Lớp C1 = “Comp” --> Tổng = 208


    # STEP 1: tính tổng trọng số của các lớp
    # Đọc toàn bộ db, khi nào ko còn row nào thì thôi
    while True:
        start = WINDOW_SIZE * WINDOW_INDEX  + 1
        stop  = WINDOW_SIZE * (WINDOW_INDEX + 1)
        # things = query.slice(start, stop).all()
        query = "select id, cate_id, tf from site_content WHERE  order by id limit " + str(start) + ", " + str(WINDOW_SIZE)
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
                NUMBER_OF_DOC = NUMBER_OF_DOC + 1
                for word in mapWeightInDoc:
                    if WORDS.has_key(word) == False:
                        WORDS[word] = 1
                        NUMWORDS['total_word'] += 1
                    if mapCategoryCounter.has_key(word) :
                        mapCategoryCounter[word] = mapCategoryCounter[word] +  1
                    else:
                        mapCategoryCounter[word] =  1

        # sleep(2)
        WINDOW_INDEX += 1


    WINDOW_INDEX = 0;

    while True:
        start = WINDOW_SIZE * WINDOW_INDEX  + 1
        stop  = WINDOW_SIZE * (WINDOW_INDEX + 1)
        # things = query.slice(start, stop).all()
        query = "select id, cate_id, tf from site_content_2 order by id limit " + str(start) + ", " + str(WINDOW_SIZE)
        logger.info(query)

        cursor = db.cursor()
        # logger.info(query)
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows == None or len(rows) == 0:
            break
        else:


            pipe = rc.pipeline()
            pipe.multi()
            count = 0
            for row in rows:
                content = row['tf']
                cateId = row['cate_id']
                docId = row["id"]
                # print docId
                count += 1
                try:
                    mapWeightInDoc = json.loads(content)
                except:
                    print 'error => ', docId
                    continue
                allTfidf = {}
                for word in mapWeightInDoc:
                    tf = int(mapWeightInDoc[word])
                    idf = mapCategoryCounter[word]
                    tfidf = (1 + math.log10(tf)) * math.log10(NUMBER_OF_DOC / idf)
                    allTfidf[word] = tfidf

                    hashKey = "%s_%s" %(hashlib.sha1(word.encode('utf-8')).hexdigest(), docId)
                    hashKeyWordCate = "%s_%s" %(hashlib.sha1(word.encode('utf-8')).hexdigest(), cateId)
                    totalWeightCate = "weight_%s" %(cateId)


                    #Tong trong so cac tu trong cate
                    if(WORD_INCATE.has_key(totalWeightCate) != True):
                        WORD_INCATE[totalWeightCate] = tf
                    else:
                        WORD_INCATE[totalWeightCate] += tf

                    if(WORD_INCATE.has_key(hashKeyWordCate) != True):
                        WORD_INCATE[hashKeyWordCate] = tf #Trọng số của từ voi lan xuat hien dau tiên trong cate
                        if(WORD_INCATE.has_key(cateId)):
                            WORD_INCATE[cateId] += 1
                        else:
                            WORD_INCATE[cateId] = 1
                    else:
                        WORD_INCATE[hashKeyWordCate] += tf #Trong so cua tu do voi lan xuat hien tiep theo trong cate


                    if existKey(hashKey):
                        pipe.hdel(hashKey, 'tf')
                        pipe.hdel(hashKey, 'idf')
                        pipe.hdel(hashKey, 'tfidf')

                    if(existKey(hashKey) != True):
                        pipe.hset(hashKey, 'tf', tf)
                        pipe.hset(hashKey, 'idf', idf)
                        pipe.hset(hashKey, 'tfidf', tfidf)

                    # pushTfIdf(word, docId, tf, idf, tfidf, cateId)
                    # exit()
                    # tfidfJson = json.dumps(allTfidf, ensure_ascii=False, encoding='utf-8')
                    # print tfidf
                if count % 100 == 0:
                    print 'Save Tfidf for ', cateId, "  => ", count
                    pipe.execute()
                # updateTfidf(docId, tfidfJson)
                # print 'save ifidf for ', docId
            print 'Save Tfidf for ', cateId
            pipe.execute()
        WINDOW_INDEX += 1
    # print mapCategoryCounter

    #STEP2: tính xác xuất P(Xk|Ci)
    # total Comp = 208
    # P(val|Comp) = (10 + 11 + 8) / 208 = 29/208

    print 'DONE'

'''
    Tinh xac xuat XkCi
'''
def PXkCi():
    #for cateId in (3,6,8,11,12,13,14):
    #    print cateId
    # mapCateWeight = rc.hgetall('total_cate_weight')
    # print mapCateWeight
    count = 0
    pipe = rc.pipeline()
    pipe.multi()
    #Danh sach cac tu va tong so van ban chua tu do: mapCategoryCounter[word] = IDF value

    #Tinh P(Xk|Ci) = Tong trong so cua tu trong cate + 1 / (Tong trong so cua cate + Tong so tu)
    # Tong trong so tu của cate = WORD_INCATE[hashKeyWordCate]
    # Tong trong cac tu trong cate = WORD_INCATE[totalWeightCate]
    # Tong so tu trong Tap van ban = NUMWORDS['total_word']



    for word in mapCategoryCounter.keys():
        for cateId in LIST_CATE:
            count += 1
            # hashKey = "%s_%s" %(hashlib.sha1(word.encode('utf-8')).hexdigest(), docId)
            hashKeyWordCate = "%s_%s" %(hashlib.sha1(word.encode('utf-8')).hexdigest(), cateId)
            totalWeightCate = "weight_%s" %(cateId)
            NUM_WORDS = NUMWORDS['total_word']
            if(WORD_INCATE.has_key(hashKeyWordCate) != True):
                continue

            pxkci = float(int(WORD_INCATE[hashKeyWordCate]) + 1) / float(int(WORD_INCATE[totalWeightCate]) + NUM_WORDS)    # --> laplace
            pipe.hset(hashKeyWordCate, 'pxkci', pxkci)
            if count % 1000 == 0:
                pipe.execute()

    pipe.execute()

    print count
    print 'Count PXkCi --> Done'
'''
    for key in rc.hkeys('word_cate'):
        count += 1
        #if count > 10:
        #    break
        #print key
        word = key.split('|')[0]
        cate = key.split('|')[1]
        #print word
        #print cate

        totalWeightCate = "weight_%s" %(cateId)
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
'''
    # pipe.execute()


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

def checkUrl(url):
    query = "select id from test WHERE url='%s'" % (url)
    # logger.info(query)
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

def updateNewCate(cateId, new_cate_id, url, content):
    db = DB()
    if checkUrl(url) != True:
        query = "INSERT INTO test(url, content, cate_id, new_cate_id, status) VALUES('%s', '%s', '%s', '%s', 3)" %(url, '', cateId, new_cate_id)
        cursor = db.cursor()
        # logger.info(query)
        cursor.execute(query)
        db.conn.commit()
    else:
        query = "UPDATE test SET url = '%s', content = '%s', cate_id = '%s', new_cate_id = '%s', status = 3 WHERE url='%s'" %(url, '', cateId, new_cate_id, url)
        cursor = db.cursor()
        # logger.info(query)
        cursor.execute(query)
        db.conn.commit()

def predictor():
    import codecs, os
    # stopwordsFile = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/data/test.txt')
    # stopwordsFile = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/data/thethao.txt')
    # f = codecs.open(stopwordsFile, encoding='utf-8', mode='r')
    # content = f.read()
    # f.close()

    db = DB()
    query = 'select cate_id, tf, url, content from site_content_3'

    cursor = db.cursor()
    logger.info(query)
    cursor.execute(query)
    rows = cursor.fetchall()

    '''
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
        NUM_WORDS = NUMWORDS['total_word']
        print 'NUM_WORDS => ', NUM_WORDS
        print termFrequencyDict
    '''
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
        mapResult = {}

        for cateId in LIST_CATE:
            pc = float(rc.hget('PC', cateId))
            pcateNew = pc
            # print 'CateID: ', cateId
            # print 'PC : ', pc
            for word in termFrequencyDict:
                tf = termFrequencyDict[word]
                # print type(word)
                if(str(type(word)) == '<type \'unicode\'>'):
                    # print 'contvert'
                    word = word.encode('utf-8')
                hashKeyWordCate = "%s_%s" %(hashlib.sha1(word).hexdigest(), cateId)

                pxkci = rc.hget(hashKeyWordCate, 'pxkci')
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
        print "NewCate => ", cateMax
        print "Value => ", max
        print "Current Cate => ", currentCateId
        print "Url => ", url
        updateNewCate(currentCateId, cateMax, url, content)

def deleteUrl(url):
    db = DB()
    query = "DELETE FROM site_content_3 WHERE url='%s'" %(url)
    cursor = db.cursor()
    # logger.info(query)
    cursor.execute(query)
    db.conn.commit()

def deleteOther():
    query = "select url from test WHERE cate_id != new_cate_id"
    # logger.info(query)
    cursor = db.cursor()
    logger.info(query)
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        deleteUrl(row['url'])

if __name__ == '__main__':
    db = DB()
    print 'Classifier'

    #B1: Tính TF, IDF và TFIDF
    # calTfIdf()

    #B2: Tính P(Xk|Ci)
    # PXkCi()

    #B3: Tính P(Ci)
    # countPC()
    deleteOther();
    #B4: Phân lớp
    predictor()




