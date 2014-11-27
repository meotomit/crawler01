# -*- coding: utf-8 -*-
'''
Created on Nov 26, 2014

@author: phuckx
'''
import subprocess 
import os
import traceback       
import logging
import codecs
 
# FORMATER = '[%(asctime)-15s] - %(message)s'
FORMATER = '%(asctime)s\t%(process)-6d\t%(levelname)-6s\t%(name)s\t%(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMATER,)
import hashlib
import time

class VnTokenizer(object):
    '''
    classdocs
    '''
    
    CMD_PATH = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../bin/vntokenizer/vnTokenizer.bat')
    TEMP_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../data/tmp')

    def __init__(self):
        '''
        Constructor
        '''
        pass
    def loadStopwords(self):
        stopwords = []
        stopwordsFile = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../data/stopwords.txt')
        f = codecs.open(stopwordsFile, encoding='utf-8', mode='r')
        lines = f.readlines()
        for line in lines:
            if len(line) > 1:
                line = line.strip()
                line = line.replace(' ', '_')
                stopwords.append(line.encode('utf-8'))
        return stopwords
        
    def tokenize(self, inputContent):
        content = None
        fileName = hashlib.md5(str(time.time())).hexdigest()
        f = codecs.open(self.TEMP_DIR + '/' + fileName, encoding='utf-8', mode='w')
        #f = open(os.path.join(self.TEMP_DIR, fileName), 'w')
        f.write(inputContent)
        f.close()
        logging.debug('Write content to file: ' + fileName)
        
        if os.path.isfile(self.TEMP_DIR + "/" + fileName): 
            try:
                # 1. token --> output file
                logging.info("** Tokenizing file: " + fileName + "...")
                inputFile = os.path.abspath(self.TEMP_DIR + "/" + fileName)
                outputFile = os.path.abspath(self.TEMP_DIR + "/" + fileName + ".TOK")
                cmd = self.CMD_PATH + " -i " + inputFile + " -o " + outputFile
                logging.debug(cmd)
                while(subprocess.call(cmd, shell=True)):
                    print '......'        
                logging.info("** Done tokenizing!")
                
                # 2. read file
                f = open(outputFile, 'r')
                content = f.read()
                f.close()
                
                # 3. remove file                
                os.remove(inputFile)
                logging.debug('Removed input file ' + fileName)
                
                os.remove(outputFile)
                logging.debug('Removed output file ' + fileName)
            except Exception:
                tb = traceback.format_exc()
                logging.error(tb)
        return content
    
if __name__ == '__main__':
    obj = VnTokenizer()
    # print obj.CMD_PATH
    #content = obj.tokenize('tai sao lai the nhi')
    #print content
    #words = content.split(',')
    #print words
    w = obj.loadStopwords()
    for i in w:
        print i
    
