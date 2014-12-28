'''
Created on Sep 21, 2012

@author: kimphuc
'''
import MySQLdb

#import os, sys
#current_path = os.path.dirname(sys.argv[0])
#lib_path = os.path.abspath(os.path.join(current_path, '.'))
#sys.path.append(lib_path)

import Config
from MySQLdb.cursors import DictCursor

class DB:
    conn = None

    def connect(self):
        self.conn = MySQLdb.connect(host=Config.DB_CRAWLER['host'], user=Config.DB_CRAWLER['user'], passwd=Config.DB_CRAWLER['pass'], db=Config.DB_CRAWLER['db'], cursorclass=DictCursor)
        self.conn.set_character_set('utf8')
        
    def cursor(self):
        try:
            cursor = self.conn.cursor()            
            #cursor.execute('SET NAMES utf8;')
            #cursor.execute('SET CHARACTER SET utf8;')
            return cursor
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            cursor = self.conn.cursor()
            #cursor.execute('SET NAMES utf8;')
            #cursor.execute('SET CHARACTER SET utf8;')
            return cursor
                    
    def query(self, sql):
        try:
            cursor = self.conn.cursor()
            #cursor.execute('SET NAMES utf8;')
            #cursor.execute('SET CHARACTER SET utf8;')
            cursor.execute(sql)
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            cursor = self.conn.cursor()
            #cursor.execute('SET NAMES utf8;')
            #cursor.execute('SET CHARACTER SET utf8;')
            cursor.execute(sql)
        return cursor
        

#db = DB()
#import pdb
#pdb.set_trace()
#cur = db.cursor()

# EXAMPLE: http://stackoverflow.com/questions/207981/how-to-enable-mysql-client-auto-re-connect-with-mysqldb
#db = DB()
#cur = db.cursor()
## wait a long time for the Mysql connection to timeout
#cur = db.cursor()
## still works

#sql = "SELECT * FROM foo"
#cur = db.query(sql)
