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
import re
from utils.StringTool import StringTool
 
# FORMATER = '[%(asctime)-15s] - %(message)s'
#FORMATER = '%(asctime)s\t%(process)-6d\t%(levelname)-6s\t%(name)s\t%(message)s'
#logging.basicConfig(level=logging.DEBUG, format=FORMATER,)

import hashlib
import time

class VnTokenizer(object):
    '''
    classdocs
    '''
    import platform
    if platform.system() == 'Linux':
        CMD_PATH = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../bin/vntokenizer/vnTokenizer.sh')
    else : 
        CMD_PATH = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../bin/vntokenizer/vnTokenizer.bat')
    
    print CMD_PATH
    
    TEMP_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../data/tmp')
    

    #SPECIAL_CHARS = '. , : " ; / [ ] \' ~ ? ~ @ # $ % ^ & * ( ) < > = + - – _ ... … '.split()
    # Có 2 dấu cách đặc biệt
    SPECIAL_CHARS = '”,“, ,…,–,—,’,‘,‘, , ̣,«,»'.split(',')
    STOP_WORDS = []
    
    def __init__(self):
        '''
        Constructor
        '''
        stopwords = self.loadStopwords()
        self.STOP_WORDS = stopwords
        pass
    
    '''
        Load stopword
    '''
    def loadStopwords(self):
        stopwords = []
        stopwordsFile = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../data/stopwords.txt')
        f = codecs.open(stopwordsFile, encoding='utf-8', mode='r')
        lines = f.readlines()
        for line in lines:
            line = line.strip()            
            line = line.replace(' ', '_')
            line = line.encode('utf-8')
            stopwords.append(line)
        #self.STOP_WORDS = stopwords
        return stopwords
    
    '''
        Ktra 1 từ có phải là stopword hay không
    '''
    def isStopWord(self, word):   
        if isinstance(word, unicode):
            word = word.encode('utf-8')
          
        word = word.strip()
        # Loại bỏ các từ nhỏ hơn 2 ký tự --> Loại được luôn các ký tự đặc biệt
        if len(word)< 2:
            return True
        
        # Loại bỏ ký tự đặc biệt    --> Loại trong trường hợp có 1 ký tự rồi
        for w2 in self.SPECIAL_CHARS:
            if w2 == word:
                return True
        
        # Loại bỏ ký tự số
        if StringTool.is_numeric(word):
            return True
        
        # Loại bỏ đơn vị đo lường
        if self.is_unit(word):
            return True
        
        # Loại bỏ các từ kiểu ngày tháng năm
        if self.is_date(word):
            return True
        
        # loại bỏ từ dừng
        for w1 in self.STOP_WORDS:
            if w1 == word:
                return True        
        return False    
    
    '''
        Kiểm tra 1 từ có phải có dạng kiểu DATE hay không
        Kiểu: dd/mm hoặc dd/mm/yyyy
    '''
    def is_date(self, word):
        dateRegex = re.compile(r"\d+\/\d+(/\d+)?")
        return dateRegex.match(str(word).strip()) is not None
    
    '''
        Ktra 1 từ có phải là đơn vị đo lường hay không
        30m2, 3,5m, 22kg
    '''
    def is_unit(self, word):
        unitRegex = re.compile(r"[-+]?\d+([\.,]\d+)?(%|ha|m|m2|kg)$")
        return unitRegex.match(str(word).strip()) is not None
    
    '''
        Tách từ
    '''
    def tokenize(self, inputContent):
        content = None
        fileName = hashlib.md5(str(time.time())).hexdigest()
        f = codecs.open(self.TEMP_DIR + '/' + fileName, encoding='utf-8', mode='w')
        #f = open(os.path.join(self.TEMP_DIR, fileName), 'w')
        f.write(inputContent)
        f.close()
        logging.debug('Write content to file: ' + fileName)
        print 'filename ==> ', fileName
        
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
    f = open("c:/Users/kim/Desktop/test.txt")
    content = f.read()
    f.close()
    import re
    arr = content.split()
    for s in arr:
        #print '--->aa' + re.sub('‘', '', s) + 'bbb'
        special = False
        for s2 in obj.SPECIAL_CHARS:
            if s == s2:
                special = True
                print '---> special char: START' + s + 'END' 
                
        if not special:
            print s
    
    
    '''
    print len('”')
    s = '22/22/22'
    print u'Ở'.lower()
    
    print obj.is_date(s)
    
    print len(obj.SPECIAL_CHARS)
    print ord(' ')
    print ord(' ')
    print ('ở' == u'ở'.encode('utf-8'))

    testvals = [
        # integers
        0, 1, -1, 1.0, -1.0,
        '0', '0.','0.0', '1', '-1', '+1', '1.0', '-1.0', '+1.0', '06',
        '0,0', '1', '-1', '+1', '1,0', '-1,0', '+1,0', '06',
        
        # non-integers
        1.1, -1.1, '1.1', '-1.1', '+1.1',
        '1.1.1', '1.1.0', '1.0.1', '1.0.0',
        '1.0.', '1..0', '1..',
        '0.0.', '0..0', '0..',
        'one', object(), (1,2,3), [1,2,3], {'one':'two'},
        # with spaces
        ' 0 ', ' 0.', ' .0','.01 '
    ]
    
    for v in testvals:
        print v, ' : ',StringTool.is_numeric(v)
    '''
    
    
