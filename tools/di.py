#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pymongo import MongoClient
import redis
import pymysql as mysql
import elasticsearch
import re
import time

"""
依赖注入
"""


class ConfigParser():

    def getConfigMap(self, filename):
        f = open(filename, "r")
        res = {}
        pSection = r'^\[(.*)\]$'
        pValue = r'^(.*)=(.*)$'
        sectionContent = None
        sectionName = None
        for line in f.readlines():
            line = line.strip()
            if re.match(pSection, line):
                sectionName = line.strip("[]")
                sectionContent = {}.copy()
                res[sectionName] = sectionContent
            elif re.match(pValue, line): 
                k = line.split("=")[0]
                v = line.split("=")[1]
                sectionContent[k] = v
        f.close()
        return res


class Di():

    def __init__(self):
        Di.redis = None
        Di.mongodb = None
        Di.es = None
        Di.config = ConfigParser().getConfigMap("/Users/lixiumeng/code/python/Galadriel/config/config.ini")
        self.start = time.time()
        self.end = time.time()

    # redis client
    def getRedis(self):
        config = Di.config["redis"]
        if Di.redis == None:
            Di.redis = redis.Redis(config["host"],int(config["port"]))
        return Di.redis

    # mongodb client
    def getMongoDb(self):
        config = Di.config["mongodb"]
        if Di.mongodb == None:
            Di.mongodb = MongoClient(config["host"],int(config["port"]))
        return Di.mongodb

    """
    mysql client
    """
    def getMysql(self):
        config = Di.config["mysql"]
        if Di.mysql == None:
            Di.mysql = mysql.connect(host='127.0.0.1', port=3306, user='root', passwd='password')
        return Di.mysql.cursor()

    def getElasticsearch(self):
        if Di.es == None:
            Di.es = elasticsearch.Elasticsearch(["localhost:9200"])
        return Di.es

    def test(self, flag):
        if flag == 'es':
            cli = self.getElasticsearch()
            cli.index(index="test",doc_type="match",body={"name":"test","age":10})
            data = cli.search(index="test", doc_type="match",body={"query":{"match_all":{}},"size":2} )
        if flag == 'mongodb':
            cli = self.getMongoDb()
            db = cli.test.test
            db.insert({"test": "success"})
            data = db.find_one()
        if flag == 'redis':
            cli = self.getRedis()
            cli.set("test_file", "redis test success")
            data = cli.get("test_file")

        if flag == 'mysql':
            cli = self.getMysql()
            data = 'success'
        print(data)
    
    # 往某文件写入内容
    def log(self,filename,content):
        fh = open(filename,"w+")
        fh.write(content)
        fh.close()

    def get_time(self):
        return self.time2str(time.time())
    
    def str2time(self,i):
        return time.mktime(time.strptime(i,"%Y-%m-%d %H:%M:%S"))
    
    def time2str(self,moment):
        return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(moment))
        
    def cost(self, log=''):
        tmp = time.time()
        total, last = tmp - self.start, tmp - self.end
        self.end = tmp
        self.logging("INFO","%s 总消耗时间:%s s,距上次%s s" % (log, total, last))

    def logging(self,level,msg):
        print("%s [%s]: %s" % (self.get_time(),level,msg))


if __name__ == '__main__':
    m = Di()
    m.test('mongodb')
    # print(m.config)
