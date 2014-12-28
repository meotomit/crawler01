'''
Created on Dec 28, 2014

@author: phuckx
'''
from DB import DB
from tokenizer.VnTokenizer import VnTokenizer

import codecs

import logging
import numpy as np
import sys,os
from time import time
import traceback

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB

from sklearn.utils.extmath import density
from sklearn import metrics

import pickle

MODEL_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/model/')

class Learner(object):
    '''
    classdocs
    '''
    def getTrainingData(self):
        data = np.array([])
        yTrain = np.array([])
        db = DB()
        WINDOW_SIZE = 1000  # so luong item muon fetch
        WINDOW_INDEX = 0
        while True:
            start = WINDOW_SIZE * WINDOW_INDEX  + 1
            stop  = WINDOW_SIZE * (WINDOW_INDEX + 1)
            # things = query.slice(start, stop).all()
            query = "select id, cate_id, content from site_content_final order by id limit " + str(start) + ", " + str(WINDOW_SIZE)
        
            #query = "select cate_id, content from site_content_final"        
            cursor = db.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            
            if rows == None or len(rows) == 0:
                print("Total results: 0")
                break
            else:
                print("Total results: " + str(len(rows)))
                print(query)
        
                for row in rows:
                    try:
                        docId = row['id']
                        content = row['content']
                        cateId = int(row['cate_id'])
                        data = np.append(data, content)
                        yTrain = np.append(yTrain, cateId)
                    except:
                        print('Error in DOC_ID: ' + str(docId))
                        tb = traceback.format_exc()
                        logging.error(tb)
            WINDOW_INDEX += 1
            
        return data, yTrain
        
    def getTestData(self):
        data = np.array([])
        yTrain = np.array([])
        
        db = DB()
        
        WINDOW_SIZE = 1000  # so luong item muon fetch
        WINDOW_INDEX = 0
        while True:
            start = WINDOW_SIZE * WINDOW_INDEX  + 1
            stop  = WINDOW_SIZE * (WINDOW_INDEX + 1)
            # things = query.slice(start, stop).all()
            query = "select id, cate_id, word_2 as content from site_content_3 order by id limit " + str(start) + ", " + str(WINDOW_SIZE)
            print query

            cursor = db.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows == None or len(rows) == 0:
                print("Total results: 0")
                break
            else:
                print("Total results: " + str(len(rows)))
                for row in rows:
                    content = row['content']
                    cateId = int(row['cate_id'])
                    
                    data = np.append(data, content)
                    yTrain = np.append(yTrain, cateId)
            WINDOW_INDEX += 1
        return data, yTrain
        
    def benchmark(self, clf, X_train, y_train, X_test, y_test):
        print('-' * 80)
        print("Training: ")
        print(clf)
        t0 = time()
        clf.fit(X_train, y_train)
        train_time = time() - t0
        print("train time: %0.3fs" % train_time)
    
        t0 = time()
        pred = clf.predict(X_test)
        test_time = time() - t0
        print("test time:  %0.3fs" % test_time)
    
        score = metrics.f1_score(y_test, pred)
        print("f1-score:   %0.3f" % score)      
        
        print 'write model --> file'
        str = pickle.dumps(clf)
        
        fileName = str(clf).split('(')[0]
        
        file = MODEL_DIR + fileName
        
        f = codecs.open(file, "w", "utf-8")
        f.write(str)
        f.close()
        
        print("classification report:")
        print(metrics.classification_report(y_test, pred, target_names=[6, 12, 13, 14]))
        
    def loadModel(self, modelName):
        
        fullPath = MODEL_DIR + modelName
        f = codecs.open(fullPath, "r", "utf-8")
        content = f.read()
        clf = pickle.loads(content)
        return clf
    
    
    
    def __init__(self):
        '''
        Constructor
        '''
    
if __name__ == '__main__':
    
    
    print 'Loading data ...'
    obj = Learner()
    
    #vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5)
    vectorizer = TfidfVectorizer(sublinear_tf=True, min_df=10)
    
    dataTrain, yTrain = obj.getTrainingData()
    dataTest, yTest = obj.getTestData()
    print 'Data Loaded'
    print 'Total training documents: ', len(dataTrain)
    print 'Total test documents: ', len(dataTest)    
    print('-' * 80)
    
    #print yTrain
    
    print 'Extract features from training dataset ...'
    t0 = time()
    xTrain = vectorizer.fit_transform(dataTrain, yTrain)
    print xTrain    
    duration = time() - t0
    print("done in %fs" % (duration))
    print("number_samples: %d, number_features: %d" % xTrain.shape)
    print('-' * 80)    
    
    print("Extracting features from the test dataset ...")
    t0 = time()
    xTest = vectorizer.transform(dataTest)
    duration = time() - t0
    print("done in %fs" % (duration))
    print("n_samples: %d, n_features: %d" % xTest.shape)
    print('-' * 80)

    results = []
    results.append(obj.benchmark(MultinomialNB(alpha=.01)), xTrain, yTrain, xTest, yTest)
    
    indices = np.arange(len(results))

    results = [[x[i] for x in results] for i in range(4)]
    
    clf_names, score, training_time, test_time = results
    training_time = np.array(training_time) / np.max(training_time)
    test_time = np.array(test_time) / np.max(test_time)
    print score
    
           
    print 'DONE'