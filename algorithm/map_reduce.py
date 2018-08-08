#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import itertools
import jieba
from collections import Counter

class MapReduce:
    __doc__ = '''提供map_reduce功能'''

    @staticmethod
    def map_reduce(i, mapper, reducer):
        """
        map_reduce方法
        :param i: 需要MapReduce的集合
        :param mapper: 自定义mapper方法
        :param reducer: 自定义reducer方法
        :return: 以自定义reducer方法的返回值为元素的一个列表
        """
        intermediate = []  # 存放所有的(intermediate_key, intermediate_value)
        for (key, value) in i.items():
            intermediate.extend(mapper(key,value))

        # sorted返回一个排序好的list，因为list中的元素是一个个的tuple，key设定按照tuple中第几个元素排序
        # groupby把迭代器中相邻的重复元素挑出来放在一起,key设定按照tuple中第几个元素为关键字来挑选重复元素
        # 下面的循环中groupby返回的key是intermediate_key，而group是个list，是1个或多个
        # 有着相同intermediate_key的(intermediate_key, intermediate_value)
        groups = {}
        for key, group in itertools.groupby(sorted(intermediate, key=lambda im: im[0]), key=lambda x: x[0]):
            groups[key] = [y for x, y in group]
        # groups是一个字典，其key为上面说到的intermediate_key，value为所有对应intermediate_key的intermediate_value
        # 组成的一个列表
        # print(groups)
        return [reducer(intermediate_key, groups[intermediate_key]) for intermediate_key in groups]


class test:

    def get_most_common_from_text(self,text,n = 100):
        word_list = [x for x in jieba.cut(text) if len(x) >= 2]
        return Counter(word_list).most_common(n)

    def map(self,k,v): # k 文档名, v 文档内容
        return self.get_most_common_from_text(v,10000)

    def reducer(self,k,v): # k 词  v 词出现的次数
         return k, sum(v)
    
    def run(self):
        
        i = {
            "a":"The quick brown fox jumped over the lazy grey dogs.",
            "b":"That's one small step for a man, one giant leap for mankind.",
            "c":"　　Mary had a little lamb,Its fleece was white as snow;And everywhere that Mary went,The lamb was sure to go",
            "d":"I pledge to honor and defend you and yours above all others",
            "e":"To share in blessings and burdens, to be your advocate, your champion"
        }
        
        t = MapReduce.map_reduce(i,self.map,self.reducer)
        print(t)


m = test()
m.run()