#!/usr/bin/env python
# -*- coding:utf-8 -*-

import di
import random
import time


'''
基于Bitmap算法的会员标签匹配

支持的操作:

1. 判断某用户是否含有某一或多个标签
2. 获取某个标签下面的所有用户

存储方案:

1. 基于redis的string类型, 使用setbit操作以节省存储空间

示例:

user:vip: 010101010000110

类似以上表示 用户ID为 1,3,5,7,12,13的用户是vip会员(相应位置的比特位为1)

'''


class Bitmap:

    def __init__(self):
        self.redis = di.Di().getRedis()
        self.mongo = di.Di().getMongoDb()
        self.set_bit_table()

    def get_random(self):
        return (int)(random.random() < 0.49)

    def init_db(self, n):
        db = self.mongo["bitmap"]["user"]
        uid = 1
        user_list = []
        for i in range(1, n):
            data = {
                "id": i,
                "member": self.get_random(),  # 是否会员
                "vip": self.get_random(),  # 是否vip
                "sex": self.get_random(),  # 性别
                "coder": self.get_random(),  # 是否程序员
                "rapper": self.get_random(),  # 是否说唱歌手
                "mac": self.get_random(),
                "supervip": self.get_random()
            }
            user_list.append(data)
            self.redis.setbit("user:all", i, data['id'])
            self.redis.setbit("user:member", i, data['member'])
            self.redis.setbit("user:vip", i, data['vip'])
            self.redis.setbit("user:coder", i, data['coder'])
            self.redis.setbit("user:rapper", i, data['rapper'])
            self.redis.setbit("user:supervip", i, data['supervip'])
            if data['sex'] == 1:
                sex_key = "user:sex_female"
            else:
                sex_key = "user:sex_male"
            self.redis.setbit(sex_key, i, 1)
            print("done:", i)
        db.insert(user_list)

    def set_bit_table(self):
        self.bit_table = [[], [8], [7], [7, 8], [6], [6, 8], [6, 7], [6, 7, 8], [5], [5, 8], [5, 7],[5, 7, 8], [5, 6], [5, 6, 8], [5, 6, 7], [5, 6, 7, 8], [4], [4, 8], [4, 7], [4, 7, 8],[4, 6], [4, 6, 8], [4, 6, 7], [4, 6, 7, 8], [4, 5], [4, 5, 8], [4, 5, 7], [4, 5, 7, 8], [4, 5, 6],[4, 5, 6, 8], [4, 5, 6, 7], [4, 5, 6, 7, 8], [3], [3,8], [3, 7],[3, 7, 8], [3, 6], [3, 6, 8], [3, 6, 7], [
                              3, 6, 7, 8], [3, 5], [3, 5, 8], [3, 5, 7],
                          [3, 5, 7, 8], [3, 5, 6], [3, 5, 6, 8], [
                              3, 5, 6, 7], [3, 5, 6, 7, 8], [3, 4],
                          [3, 4, 8], [3, 4, 7], [3, 4, 7, 8], [3, 4, 6], [
                              3, 4, 6, 8], [3, 4, 6, 7], [3, 4, 6, 7, 8],
                          [3, 4, 5], [3, 4, 5, 8], [3, 4, 5, 7], [
                              3, 4, 5, 7, 8], [3, 4, 5, 6], [3, 4, 5, 6, 8],
                          [3, 4, 5, 6, 7], [3, 4, 5, 6, 7, 8], [
                              2], [2, 8], [2, 7], [2, 7, 8], [2, 6],
                          [2, 6, 8], [2, 6, 7], [2, 6, 7, 8], [2, 5], [
                              2, 5, 8], [2, 5, 7], [2, 5, 7, 8],
                          [2, 5, 6], [2, 5, 6, 8], [2, 5, 6, 7], [
                              2, 5, 6, 7, 8], [2, 4], [2, 4, 8], [2, 4, 7],
                          [2, 4, 7, 8], [2, 4, 6], [2, 4, 6, 8], [
                              2, 4, 6, 7], [2, 4, 6, 7, 8], [2, 4, 5],
                          [2, 4, 5, 8], [2, 4, 5, 7], [2, 4, 5, 7, 8], [2, 4, 5, 6], [2, 4, 5, 6, 8],
                          [2, 4, 5, 6, 7], [2, 4, 5, 6, 7, 8], [
                              2, 3], [2, 3, 8], [2, 3, 7], [2, 3, 7, 8],
                          [2, 3, 6], [2, 3, 6, 8], [2, 3, 6, 7], [
                              2, 3, 6, 7, 8], [2, 3, 5], [2, 3, 5, 8],
                          [2, 3, 5, 7], [2, 3, 5, 7, 8], [2, 3, 5, 6], [
                              2, 3, 5, 6, 8], [2, 3, 5, 6, 7],
                          [2, 3, 5, 6, 7, 8], [2, 3, 4], [2, 3, 4, 8], [2, 3, 4, 7], [2, 3, 4, 7, 8],
                          [2, 3, 4, 6], [2, 3, 4, 6, 8], [2, 3, 4, 6, 7], [
                              2, 3, 4, 6, 7, 8], [2, 3, 4, 5],
                          [2, 3, 4, 5, 8], [2, 3, 4, 5, 7], [2, 3, 4, 5, 7, 8], [
                              2, 3, 4, 5, 6], [2, 3, 4, 5, 6, 8],
                          [2, 3, 4, 5, 6, 7], [2, 3, 4, 5, 6, 7, 8], [1], [
                              1, 8], [1, 7], [1, 7, 8], [1, 6], [1, 6, 8],
                          [1, 6, 7], [1, 6, 7, 8], [1, 5], [1, 5, 8], [
                              1, 5, 7], [1, 5, 7, 8], [1, 5, 6], [1, 5, 6, 8],
                          [1, 5, 6, 7], [1, 5, 6, 7, 8], [1, 4], [1, 4, 8], [1, 4, 7], [
                              1, 4, 7, 8], [1, 4, 6], [1, 4, 6, 8], [1, 4, 6, 7],
                          [1, 4, 6, 7, 8], [1, 4, 5], [1, 4, 5, 8], [1, 4, 5, 7], [1, 4, 5, 7, 8],
                          [1, 4, 5, 6], [1, 4, 5, 6, 8], [1, 4, 5, 6, 7], [1, 4, 5, 6, 7, 8], [1, 3],
                          [1, 3, 8], [1, 3, 7], [1, 3, 7, 8], [1, 3, 6], [1, 3, 6, 8], [1, 3, 6, 7],
                          [1, 3, 6, 7, 8], [1, 3, 5], [1, 3, 5, 8], [
                              1, 3, 5, 7], [1, 3, 5, 7, 8], [1, 3, 5, 6],
                          [1, 3, 5, 6, 8], [1, 3, 5, 6, 7], [1, 3, 5, 6, 7, 8], [
                              1, 3, 4], [1, 3, 4, 8], [1, 3, 4, 7],
                          [1, 3, 4, 7, 8], [1, 3, 4, 6], [1, 3, 4, 6, 8], [
            1, 3, 4, 6, 7], [1, 3, 4, 6, 7, 8], [1, 3, 4, 5],
            [1, 3, 4, 5, 8], [1, 3, 4, 5, 7], [1, 3, 4, 5, 7, 8], [1, 3, 4, 5, 6], [1, 3, 4, 5, 6, 8],
            [1, 3, 4, 5, 6, 7], [1, 3, 4, 5, 6, 7, 8], [1, 2], [
                1, 2, 8], [1, 2, 7], [1, 2, 7, 8], [1, 2, 6],
            [1, 2, 6, 8], [1, 2, 6, 7], [1, 2, 6, 7, 8], [1, 2, 5], [
                1, 2, 5, 8], [1, 2, 5, 7], [1, 2, 5, 7, 8],
            [1, 2, 5, 6], [1, 2, 5, 6, 8], [1, 2, 5, 6, 7], [
                1, 2, 5, 6, 7, 8], [1, 2, 4], [1, 2, 4, 8], [1, 2, 4, 7],
            [1, 2, 4, 7, 8], [1, 2, 4, 6], [1, 2, 4, 6, 8], [
                1, 2, 4, 6, 7], [1, 2, 4, 6, 7, 8], [1, 2, 4, 5],
            [1, 2, 4, 5, 8], [1, 2, 4, 5, 7], [1, 2, 4, 5, 7, 8], [1, 2, 4, 5, 6], [1, 2, 4, 5, 6, 8],
            [1, 2, 4, 5, 6, 7], [1, 2, 4, 5, 6, 7, 8], [1, 2, 3], [
                1, 2, 3, 8], [1, 2, 3, 7], [1, 2, 3, 7, 8],
            [1, 2, 3, 6], [1, 2, 3, 6, 8], [1, 2, 3, 6, 7], [
                1, 2, 3, 6, 7, 8], [1, 2, 3, 5], [1, 2, 3, 5, 8],
            [1, 2, 3, 5, 7], [1, 2, 3, 5, 7, 8], [1, 2, 3, 5, 6], [
                1, 2, 3, 5, 6, 8], [1, 2, 3, 5, 6, 7],
            [1, 2, 3, 5, 6, 7, 8], [1, 2, 3, 4], [1, 2, 3, 4, 8], [1, 2, 3, 4, 7], [1, 2, 3, 4, 7, 8],
            [1, 2, 3, 4, 6], [1, 2, 3, 4, 6, 8], [1, 2, 3, 4, 6, 7], [
                1, 2, 3, 4, 6, 7, 8], [1, 2, 3, 4, 5],
            [1, 2, 3, 4, 5, 8], [1, 2, 3, 4, 5, 7], [1, 2, 3, 4, 5, 7, 8], [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6, 8], [1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5, 6, 7, 8]]

    def build_bit_table(self):  # 生成0-255的表
        arr = []
        for i in range(0, 256):
            tmp_arr = []
            tstr = bin(i).replace('0b', '').zfill(8)
            n = 0
            for k in tstr:
                n = n + 1
                if int(k) == 1:
                    tmp_arr.append(n)
            arr.append(tmp_arr)
        self.bit_table = arr

    def get(self, key):  # 获取redis某key的值
        return self.redis.get(key)

    def key2array(self, key):  # 将二进制('\x05'->'0b00000101')变为数组[5,7], 表示第五位和第七位为1
        tmpstr = ''.join([bin(i).replace('0b', '').zfill(8) for i in key])
        # print(tmpstr)
        arr = []
        str_len = len(tmpstr)
        for i in range(0, str_len):
            if int(tmpstr[i]) == 1:
                arr.append(i)
        return (arr)

    def key2array2(self, key):
        arr = []
        n = 0  # 每次循环的最低数字
        for i in key:
            k = 0
            if i > 0:
                for p in bin(i).replace('0b', '').zfill(8):
                    k = k + 1
                    if int(p) == 1:
                        arr.append(n + k - 1)
            n = n + 8
        return (arr)

    def key2array3(self, key):  # 查表法
        arr = []
        n = 0
        for i in key:
            pos = self.bit_table[i]
            for k in pos:
                arr.append(n + k - 1)
            n = n + 8
        return (arr)
    # 耗费的时间

    def cost(self, tag):
        if tag == 'start':
            self.start = time.time()
            print("start:", self.start)
        else:
            self.end = time.time()
            print("cost time:", self.end - self.start ," s")

    # 性能测试
    def benchmark(self):
        key = self.get("user:vip")
        self.cost("start")
        self.key2array(key)
        self.cost("end")
        self.cost("start")
        self.key2array2(key)
        self.cost("end")
        self.cost("start")
        self.key2array3(key)
        self.cost("end")

    def str2bin(self, str):
        return bin(int(str, 10))

    def encode(self, s):
        return ' '.join([bin(ord(c)).replace('0b', '') for c in s])

    def decode(self, s):
        return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])

# 测试
if __name__ == '__main__':
    bm = Bitmap()
    # bm.init_db(10000)
    # print(bm.key2array(bm.get("user:vip")))
    # bm.key2array2(bm.get("test_a"))
    # bm.key2array3(bm.get("test_a"))
    bm.benchmark()