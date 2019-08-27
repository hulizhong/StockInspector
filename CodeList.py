#!/usr/bin/env python
# coding=utf-8
import sys
import tushare as ts

reload(sys)
sys.setdefaultencoding('utf8')  


class DataItem(object):
    '''
    StockRepository's data item.
    '''
    def __init__(self, code, name, date, price, volume):
        self.code = code
        self.name = name
        self.date = date
        self.price = price
        self.volume = volume
        self.amount = price * volume

    def des(self):
        print self.date, self.name, self.price, "*", self.volume, "=", self.amount

class StockRepository(object):
    '''
    stock trace repository.
    '''
    def __init__(self):
        self.datas = {}

    def push(self, item):
        if self.datas.has_key(item.code):
            self.datas[item.code].append(item)
        else:
            self.datas[item.code] = []
            self.datas[item.code].append(item)

    def des(self):
        print "|-----------------------------------|"
        for key,value in self.datas.items():
            #print "|....................%6s %10s|" % (key, value[0].name) 
            print "|%6s %10s                    |" % (key, value[0].name) 
            volume = 0
            amount = 0.0
            for item in value:
                print "|%8s %6s * %5s = %9s|" % (item.date, str(item.price), str(item.volume), str(item.amount)) 
                volume += item.volume
                amount += (item.amount/-1)
            if (volume < 0):
                volume /= -1
            print "|    vol.%5s      amount.%9s|" % (str(volume), str(amount)) 
        print "|-----------------------------------|"

    def getVolume(self, code):
        if self.datas.has_key(code):
            val = self.datas[code]
            volume = 0
            for item in val:
                volume += item.volume

            if (volume < 0):
                volume /= -1
            #print "Get the code.%s vol.%s" %(code, volume)
            return volume
        else:
            return 0


def insertHandingCode(dic, codes, flag):
    '''
    持仓区
    '''
    #it = DataItem('000236', '测试名称', '190806', 8.54, 100)
    #it.des()

    sr = StockRepository()
    sr.push(DataItem('600016', '民生银行', '190423', 6.47, 1100))
    sr.push(DataItem('600016', '民生银行', '190820', 5.84, -1100))

    sr.push(DataItem('000402', '--金融街', '190422', 8.51, 800))
    sr.push(DataItem('000402', '', '190802', 7.35, -800))
    sr.push(DataItem('000402', '', '190809', 7.24, 1200))
    sr.push(DataItem('000402', '', '190812', 7.33, -1200))
    sr.push(DataItem('000402', '', '190816', 7.64, 1200))

    sr.push(DataItem('600266', '北京城建', '190723', 8.24, 600))
    sr.push(DataItem('600266', '', '190802', 7.8, -600))

    sr.push(DataItem('002818', '--富森美', '190430', 14.75, 170)) #25.08 * -100
    sr.push(DataItem('002818', '', '190806', 11.49, -170))

    sr.push(DataItem('002253', '川大智胜', '190624', 15.45, 200))
    sr.push(DataItem('002253', '', '190806', 13.49, -200))

    sr.push(DataItem('002241', '歌尔股份', '190820', 13.10, 700))
    sr.push(DataItem('002241', '歌尔股份', '190826', 13.60, -700))

    sr.push(DataItem('603299', '苏盐井神', '190820', 8.04, 800))
    sr.push(DataItem('603299', '苏盐井神', '190826', 8.14, -800))

    sr.push(DataItem('600338', '西藏珠峰', '190826', 12.60, 0))

    if (flag == '11'):
        sr.des()

    dic['000402'] = sr.getVolume('000402'); #金融街 <5.95, 650
    dic['002241'] = sr.getVolume('002241'); #歌尔股份
    dic['603299'] = sr.getVolume('603299'); #苏盐井神
    dic['600016'] = sr.getVolume('600016'); #民生银行 <5.95, 650
    dic['600266'] = sr.getVolume('600266'); #北京城建 <8
    dic['002253'] = sr.getVolume('002253'); #川大智胜 15.45
    dic['002818'] = sr.getVolume('002818'); #富森美
    dic['600338'] = sr.getVolume('600338'); #西藏珠峰

    for it in dic.keys():
        codes.append(it)

def insertTraceCode(dic, codes):
    '''
    长期跟踪区；
    '''
    dic["000423"] = 30  #东阿阿胶 <40, 190715/30.
    dic["601006"] = 7   #大秦铁路 <8, 190715/7.
    dic["000581"] = 18  #威孚高科 <
    dic["002344"] = 4   #海宁皮城 <4
    dic["600557"] = 8   #康缘药业 <8
    dic["002763"] = 8   #汇洁股份
    dic["600051"] = 8   #宁波联合 <8, 735
    dic["600266"] = 8   #北京城建 <8
    for it in dic.keys():
        codes.append(it)

def insertPbLess1Code(codes):
    '''
    破净观察区
    '''
    codes.append("000625") #长安汽车 <6.5
    codes.append("600266") #北京城建 <8
    codes.append("002344") #海宁皮城 <4.5
    codes.append("600016") #民生银行 <5.95

def insertWatchCode(codes):
    '''
    观察区A
    '''
    codes.append("601006") #大秦铁路 <8
    codes.append("000581") #威孚高科 <
    codes.append("600674") #川投能源
    codes.append("600585") #海螺水泥
    codes.append("603858") #步长制药
    codes.append("600703") #三安光电
    codes.append("000423") #东阿阿胶 <40
    codes.append("600516") #方大炭素
    codes.append("002027") #分众传媒
    codes.append("002250") #联化科技
    codes.append("300004") #南风股份
    codes.append("300369") #绿盟科技
    codes.append("600433") #冠豪高新
    codes.append("300458") #全志科技
    codes.append("300273") #和佳股份
    codes.append("600598") #北大荒
    codes.append("002818") #富森美

