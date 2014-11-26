# -*- coding: utf-8 -*-
'''
Created on Jun 1, 2014

@author: kimphuc
'''
import redis

class RedisQueue(object):
    """Simple Queue with Redis Backend"""
    def __init__(self, name, namespace='queue', **redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""
        self.__db= redis.Redis(**redis_kwargs)
        if len(namespace) > 0:
            self.key = '%s:%s' %(namespace, name)
        else: 
            self.key = name
        self.namespace = namespace

    def qsize(self):
        """Return the approximate size of the queue."""
        return self.__db.llen(self.key)

    def empty(self):
        """Return True if the queue is empty, False otherwise."""
        return self.qsize() == 0

    def put(self, item):
        """Put item into the queue."""
        self.__db.rpush(self.key, item)

    def get(self, block=True, workerName=None, timeout=None):
        """Remove and return an item from the queue. 

        If optional args block is true and timeout is None (the default), block
        if necessary until an item is available."""
        if block:
            #item = self.__db.blpop(self.key, timeout=timeout)
            newQueue = '%s:%s' %(self.namespace, workerName)
            #print 'Queue: ', newQueue
            item = self.__db.brpoplpush(self.key, newQueue, 0)
            #print "Get item: "  + item
            res = self.__db.lrem(newQueue, item, 0)
            #print 'Delete from ', newQueue , ", item: " + item
        else:
            item = self.__db.lpop(self.key)
            if item:
                item = item[1]
            
        return item
    def get_nowait(self):
        """Equivalent to get(False)."""
        return self.get(False)
    def delete(self, queueName):
        return self.__db.delete(self.namespace + ":" + queueName)