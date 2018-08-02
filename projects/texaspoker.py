#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

'''
德州扑克

基本规则:

1. 玩家人数2-10人, 开局每位玩家发2张牌,开始叫牌
2. 牌桌发牌最多三次,第一次3张,以后两次每次一张

计算牌面分数:
1. 5张手牌才能计算分数
2. 优先计算计算牌型,牌型相同优先比较触发牌型的牌面数值,最后比较高牌的面值,总分最高的获胜
3. 当牌桌上的牌超过3张的时候,取手牌 + 牌桌牌中最好的5张

牌型一共10种
18  同花大顺  = 同花 + 顺子 + A开头
17  同花顺   = 同花 + 顺子
11  四条     = 四条
10  葫芦     = 对子 + 三条
9   同花     = 同花
8   顺子     = 顺子
7   三条     = 三条
6   两对     = 对子 + 对子
3   对子     = 对子
1   高牌     = 无

计算分数:

    分数 =  牌型 * 1000000 + 首判点数 * 10000 + 二判点数 * 100  +  脚牌点数

    具体步骤

    1. 判断牌型
    2. 判断首判点数
    3. 判断二判点数
    4. 脚牌

    示例:

    本副牌:['♣7', '♦A', '♠2', '♦7', '♦2']

    score : 6 *1000000 + 12*10000+ 2*100 +13 =  6120213

'''


class Poker:  # 扑克牌类

    def __init__(self, id, no, color):
        self.id = id
        Poker.no = ('', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')  # 牌面
        Poker.color = ('♠', '♥', '♣', '♦')  # 花色
        self.cid = color  # 颜色id
        self.nid = no    # 牌面id
        self.no = Poker.no[no]
        self.color = Poker.color[color]
        self.name = self.color + self.no


class Player:  # 玩家类

    def __init__(self, id):
        self.id = id  # 玩家编号
        self.hand = []  # 玩家的手牌
        self.pokers = []  # 玩家手牌中最好的一副牌
        self.score = 0  # 玩家的最大分数


class PokerPack:  # 一副扑克牌

    def __init__(self):
        self.pack = []
        self.getPackOfTexasPoker()  # 一副牌
        self.open = self.pack  # 未使用过的牌
        self.close = []  # 使用过的牌

    def getPackOfTexasPoker(self):  # 构建一副未被使用的德州扑克牌
        pid = 1  # poker的id
        for no in range(1, 14):  # 德州扑克不含大小鬼
            for color in range(0, 4):
                pid = pid + 1
                self.pack.append(Poker(pid, no, color))

    def delFromPokers(self, poker, pokers):  # 从一副牌中删除一张牌
        for idx, i in enumerate(pokers):
            if i.name == poker.name:
                pokers.pop(idx)
                return True
            else:
                continue

    def closePoker(self, poker):  # 将一张牌添加到一个使用过的牌库中
        self.close.append(poker)

    def getPoker(self):  # 从该副牌中获取一张牌
        poker = random.choice(self.open)  # 从未使用的牌中随即一张
        self.delFromPokers(poker, self.open)  # 将其从未使用的牌库中移入已使用的牌库
        self.closePoker(poker)
        return poker


class Match():  # 比赛

    tablePokerLimit = 5  # 牌桌上最大牌数
    debug = 0  # 是否打印所有玩家的手牌组合

    def __init__(self, num):
        self.num = num  # 玩家数量
        self.pack = PokerPack()  # 生成一副牌
        self.used = self.pack.close
        self.user = []  # 所有玩家
        self.table = []  # 牌桌
        self.userReady()  # 牌桌上的玩家准备

        # 以下为全排列准备
        self.proccess = [0, 0, 0, 0, 0]
        self.cm = 7
        self.cn = 5
        self.tpk = [2, 3, 4, 5, 7, 8, 9]
        self.all = []

    def userReady(self):  # 玩家准备,每个玩家手牌为空
        for n in range(1, self.num + 1):
            self.user.append(Player(n))

    def sendPokerToUser(self, userid):  # 给某用户发牌
        for user in self.user:
            if user.id == userid:
                user.hand.append(self.pack.getPoker())

    def sendPokerToTable(self, n):  # 亮n张牌
        if n < 1:
            n = 1
        for i in range(0, n):
            self.table.append(self.pack.getPoker())

    def Start(self):  # 比赛开始
        for uid in range(1, self.num + 1):  # 给每个用户发第一张牌
            self.sendPokerToUser(uid)
        for uid in range(1, self.num + 1):  # 给每个用户发第二张牌
            self.sendPokerToUser(uid)
        self.sendPokerToTable(2)  # 牌桌两张牌
        self.con = 'y'
        while self.con == 'y':
            self.sendPokerToTable(1)
            self.Report()
            if len(self.table) == self.tablePokerLimit:
                self.con = 'n'
                self.check_winner()
                print("亮牌,游戏结束")
            else:
                self.con = input("是否继续游戏? Y or N\n")

    def showhand(self, pokers):  # 玩家展示手牌,选出所有牌中最好的一副
        if len(pokers) < 5:
            return False
        max_score = 0
        self.tpk = pokers
        self.cm = len(pokers)
        self.all = []
        self.c_m_n()  # 生成所有手牌的全排列组合
        rt = []
        for c in self.all:
            i = self.calculateScore(c)
            if self.debug == 1:
                print(i)
            if i["pokerscore"] >= max_score:
                max_score = i["pokerscore"]
                rt = i
        return rt

    def user_report(self, u):  # 玩家报告手牌
        print("玩家 %s 亮牌:" % u.id)
        logstr = ''
        for p in (u.hand + self.table):
            logstr = logstr + p.color + p.no + ";"
        print("所有牌: %s" % logstr)
        print("最好的牌:%s" % (';'.join([n + "" for n in u.pokers])))
        print("牌型: %s;type [%s] 分数: %s" % (u.appraise["typeNick"], ''.join(
            [str(n) + " " for n in u.appraise["typecode"]]), u.appraise["pokerscore"]))
        print("")

    def c_m_n(self, st=0, pic=0):  # 从m中取n个数的全排列
        if pic == self.cn:
            self.all.append(self.proccess.copy())
            return self.proccess
        max_n = self.cm - self.cn + pic
        for j in range(st, max_n + 1):
            self.proccess[pic] = self.tpk[j]
            self.c_m_n(j + 1, pic + 1)

    def check_winner(self):  # 检查胜利者
        b = 0
        winner = []
        for u in self.user:
            pi = self.showhand(u.hand + self.table)
            u.pokers = pi["graphs"]
            u.score = pi["pokerscore"]
            u.appraise = pi
            self.user_report(u)
            if u.score > b:
                winner = [u]
                b = u.score
            elif u.score == b:
                winner.append(u)

        print("胜利者是:")
        for u in winner:
            print("玩家 %s : 获胜牌型:" % u.id)
            print(u.pokers)

    def Report(self):  # 报告当前比赛局势
        log = "台桌上的牌:"
        # 报牌桌上的手牌
        for id, a in enumerate(self.table):
            log = log + a.name + ";"
        print(log)
        print("本次比赛已使用%s张牌" % len(self.used))

    def printPoker(self, ps, title="这副牌"):
        log = title + ':'
        for p in ps:
            log = log + p.name + ";"
        print(log)

    def calculateScore(self, pokers):  # 计算手牌的得分
        if len(pokers) < 5:  # 不足5张牌得分为 0
            return False
        # self.printPoker(pokers, "参与计算分数的牌")
        statistic = {
            "colors": [],  # 所有花色 无意义
            "colorCount": [0, 0, 0, 0],  # 每个花色的数量
            "graphs": [],    # 所有牌的形状
            "numCount": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 每个数字的张数
            "pokertype": [],  # 牌型统计
            "members": [],
            "fp": [],  # 首判部分
            "sp": [],  # 二判
            "ep": []  # 三叛
        }  # 统计对象
        for p in pokers:
            statistic["graphs"].append(p.name)
            # 统计基本信息
            co = {
                "id": p.cid,
                "members": [p.id],
                "count": 1
            }
            is_count = False
            # print(statistic["colors"])
            for c in statistic["colors"]:
                if c["id"] == co["id"]:
                    c["members"].extend(co["members"].copy())
                    c["count"] = c["count"] + 1
                    is_count = True
            if not is_count:
                statistic["colors"].append(co)

            no = {
                "id": p.nid,
                "members": [p.id],
                "count": 1
            }
            is_count = False
            for c in statistic["members"]:
                if c["id"] == no["id"]:
                    c["members"].extend(no["members"].copy())
                    c["count"] = c["count"] + 1
                    is_count = True
            if not is_count:
                statistic["members"].append(no)
            statistic["numCount"][p.nid] = statistic["numCount"][p.nid] + 1

        # 判断同花
        for v in statistic["colors"]:
            if v["count"] == 5:
                statistic["pokertype"].append(9)
                statistic["fp"].extend(v["members"].copy())
        # 判断 四条,三条,一对,两对
        for p in statistic["members"]:
            if p["count"] == 4:
                statistic["pokertype"].append(11)
                statistic["fp"].extend(p["members"].copy())
            elif p["count"] == 3:
                statistic["pokertype"].append(7)
                statistic["fp"].extend(p["members"].copy())
            elif p["count"] == 2:
                statistic["pokertype"].append(3)
                if len(statistic["fp"]) == 3:  # 葫芦,葫芦的情况将对子置为二判
                    statistic["sp"].extend(p["members"].copy())
                elif len(statistic["fp"]) == 2:  # 如果首判的对子的值比当前值小
                    for v in pokers:
                        if v.id == statistic["fp"][0]:
                            fpv = v.nid
                    if fpv < p["id"]:  # 如果首判对子没有当前对子大
                        statistic["sp"].extend(statistic["fp"].copy())
                        statistic["fp"] = p["members"].copy()
                    else:
                        statistic["sp"].extend(p["members"].copy())
                else:  # 如果没有置位首判
                    statistic["fp"].extend(p["members"].copy())
            else:
                statistic["ep"].extend(p["members"].copy())

        # 判断顺子
        con = 0
        for p in statistic["numCount"]:
            if p > 0:  # 检查顺子
                con = con + 1
                if con >= 5:
                    statistic["pokertype"].append(8)
            else:
                con = 0
        # 牌型判断完毕
        typeName = "高牌"
        if len(statistic["pokertype"]) == 0:
            pokertype = 1
        else:
            pokertype = sum(statistic["pokertype"])

        if len(statistic["pokertype"]) == 1:
            if statistic["pokertype"][0] == 11:
                typeName = "四条"
            if statistic["pokertype"][0] == 9:
                typeName = "同花"
            if statistic["pokertype"][0] == 8:
                typeName = "顺子"
            if statistic["pokertype"][0] == 7:
                typeName = "三条"
            if statistic["pokertype"][0] == 3:
                typeName = "对子"
        if len(statistic["pokertype"]) == 2:
            if statistic["pokertype"].count(3) == 2:
                typeName = "两对"
            if statistic["pokertype"].count(3) == 1 and 1 == statistic["pokertype"].count(7):
                typeName = "葫芦"
            if statistic["pokertype"].count(9) == 1 and 1 == statistic["pokertype"].count(8):
                typeName = "同花顺"
        cfp = 0
        csp = 0
        cep = 0
        for p in pokers:
            if p.id in statistic["fp"]:
                cfp = cfp + p.nid
            if p.id in statistic["sp"]:
                csp = csp + p.nid
            if p.id in statistic["ep"]:
                cep = cep + p.nid
        score = (pokertype * 1000000) + cfp * 10000 + csp * 100 + cep
        info = {
            "typeNick": typeName,
            "pokertype": pokertype,
            "pokerscore": score,
            "typecode": statistic["pokertype"],
            "graphs": statistic["graphs"],
            "statistic": statistic
        }
        return info


'''
开始
'''


if __name__ == '__main__':
    players = int(input("请输入玩家数量:"))
    while players < 2 or players > 10:
        players = int(input("玩家数量非法,请重新输入玩家数量:"))
    m = Match(players)
    m.Start()