#!/usr/bin/env python
# coding=utf-8
import sys
import tushare as ts
import collections

reload(sys)
sys.setdefaultencoding('utf8')  


# ----------------------------------------------------------------- split line (trade trace as follow.)----------------------------- #
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
        self.datas = collections.OrderedDict() #self.datas = {}

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
    sr.push(DataItem('603299', '苏盐井神', '190820', 8.04, 800))
    sr.push(DataItem('603299', '', '190826', 8.14, -800))

    sr.push(DataItem('600266', '北京城建', '190723', 8.24, 600))
    sr.push(DataItem('600266', '', '190802', 7.8, -600))

    sr.push(DataItem('002253', '川大智胜', '190624', 15.45, 200))
    sr.push(DataItem('002253', '', '190806', 13.49, -200))

    sr.push(DataItem('002818', '--富森美', '190430', 14.75, 170)) #25.08 * -100
    sr.push(DataItem('002818', '', '190806', 11.49, -170))

    sr.push(DataItem('600338', '西藏珠峰', '190829', 12.45, 1000))
    sr.push(DataItem('600338', '', '190830', 11.80, -1000))

    sr.push(DataItem('600016', '民生银行', '190423', 6.47, 1100))
    sr.push(DataItem('600016', '', '190820', 5.84, -1100))

    sr.push(DataItem('000402', '--金融街', '190422', 8.51, 800))
    sr.push(DataItem('000402', '', '190802', 7.35, -800))
    sr.push(DataItem('000402', '', '190809', 7.24, 1200))
    sr.push(DataItem('000402', '', '190812', 7.33, -1200))
    sr.push(DataItem('000402', '', '190816', 7.64, 1200))
    sr.push(DataItem('000402', '', '190828', 7.56, -1200))

    sr.push(DataItem('002241', '歌尔股份', '190820', 13.10, 700))
    sr.push(DataItem('002241', '', '190826', 13.60, -700))
    sr.push(DataItem('002241', '', '190830', 13.15, 1200))
    sr.push(DataItem('002241', '', '190902', 13.51, -1200))

    sr.push(DataItem('600823', '世茂股份', '190829', 4.06, 2000))
    sr.push(DataItem('600823', '', '190902', 4.10, -2000))

    sr.push(DataItem('600682', '南京新百', '190904', 11.60, 1100))
    sr.push(DataItem('600682', '', '190905', 11.93, -1100))
    sr.push(DataItem('600682', '', '190905', 11.68, 1100))
    sr.push(DataItem('600682', '', '190906', 11.62, -1100))

    sr.push(DataItem('002045', '国光电器', '190905', 6.42, 2000))
    sr.push(DataItem('002045', '', '190906', 6.60, -2000))

    if (flag == '11'):
        sr.des()
        showProfits19()
        #showProfits20()
        return

    dic['000402'] = sr.getVolume('000402'); #金融街 <5.95, 650
    dic['002241'] = sr.getVolume('002241'); #歌尔股份
    dic['603299'] = sr.getVolume('603299'); #苏盐井神
    dic['600016'] = sr.getVolume('600016'); #民生银行 <5.95, 650
    dic['600266'] = sr.getVolume('600266'); #北京城建 <8
    dic['002253'] = sr.getVolume('002253'); #川大智胜 15.45
    dic['002818'] = sr.getVolume('002818'); #富森美
    dic['600338'] = sr.getVolume('600338'); #西藏珠峰
    dic['600823'] = sr.getVolume('600823'); #世茂股份
    dic['600173'] = sr.getVolume('600173'); #卧龙地产
    dic['300198'] = sr.getVolume('300198'); #纳川股份
    dic['002128'] = sr.getVolume('002128'); #露天煤业
    dic['000537'] = sr.getVolume('000537'); #广宇发展
    dic['600682'] = sr.getVolume('600682'); #南京新百
    dic['002045'] = sr.getVolume('002045'); #国光电器
    #dic[''] = sr.getVolume(''); #

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


# ----------------------------------------------------------------- split line (profit trace as follow.)----------------------------- #
class ToolSet(object):
    '''
    calc util.
    '''
    def __init__(self):
        pass

    def multipleInterest(self, base, rate, cycle):
        '''
        '''
        i = 1
        print "|---------|"
        while (i <= cycle):
            base *= (1+rate)
            print "|%2s %6.2f|" % (str(i), base)
            i += 1
        print "|---------|"
        return base

    def multipleInterestOneYear(self, base, rate):
        '''
        has 52 work's week in an year.
        '''
        return self.multipleInterest(base, rate, 52)

class ProfitTrace(object):
    '''
    profit trace log.
    '''
    def __init__(self):
        self.profits = collections.OrderedDict()

    def des(self):
        lastTot = 0
        profit = 0 # profit = value - lastTot
        rate = 0   # rate = profit / lastTot
        print "|-----------------------------------|"
        for key,value in self.profits.items():
            if (lastTot != 0):
                profit = value - lastTot
                rate = (profit / lastTot) * 100
            else:
                profit = 0
                rate = 0
            if (rate < 0):
                rate *= -1
            rateStr = '%.2f' % (rate)
            lastTot = value
            print "|%4s Tot.%6s gain.%6s(%6s)|" % (key, str(value), str(profit), str(rateStr))
        print "|-----------------------------------|"

    def push(self, date, vol):
        self.profits[date] = vol

def showProfits19():
    pt19 = ProfitTrace()
    pt19.push('0830', 25.08)
    pt19.push('0912', 27.00)
    pt19.push('1231', 40.25)
    pt19.des()

def showProfits20():
    pt20 = ProfitTrace()
    pt20.push('0106', 40.25)
    pt20.push('1231', 187.20)
    pt20.des()

#t = ToolSet()
#print "%.2f" % t.multipleInterest(25.08, 0.03, 16)
'''
|---------|
| 1  25.83|+26.22
| 2  26.61|
| 3  27.41|
| 4  28.23|
| 5  29.07|
| 6  29.95|
| 7  30.85|
| 8  31.77|
| 9  32.72|
|10  33.71|
|11  34.72|
|12  35.76|
|13  36.83|
|14  37.94|
|15  39.07|
|16  40.25|
|---------|
'''
#print "%.2f" % t.multipleInterestOneYear(40.25, 0.03)

