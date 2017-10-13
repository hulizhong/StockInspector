#!/usr/bin/env python
# coding=utf-8

import tushare as ts  
import pandas as pd
  
import os
import sys
#import decimal
#print 'sys.getdefaultencoding', sys.getdefaultencoding() 
reload(sys)
sys.setdefaultencoding('utf8')  

def download(code, start, end, filename):
    '''
    @brief: value level.
    @start param, start time, must > stop time.
    @stop param, stop time.
    @filename, save into csv.
    '''
    #res = ts.get_h_data(code="300458", start="2015-01-11", end="2017-09-20")
    res = ts.get_h_data(code, start, end)
    res.to_csv(filename)

def show(filename):
    '''
    foreach dataframe res.
    '''
    res = pd.DataFrame.from_csv(filename)
    for index, row in res.iterrows():
        print type(row), row['close']

def showBig(filename, diffPri):
    '''
    '''
    print '-----------------价值>', diffPri, '的日子里'
    res = pd.DataFrame.from_csv(filename)
    res = res[res['close'] > diffPri]
    for index, row in res.iterrows():
        print index, row['close']

def showLittle(filename, diffPri):
    '''
    '''
    print '-----------------价值<', diffPri, '的日子里'
    res = pd.DataFrame.from_csv(filename)
    res = res[res['close'] < diffPri]
    for index, row in res.iterrows():
        print index, row['close']

def __analyzePrice(filename):
    '''
    called by analyzePrice, return (diff, rate) base 80%-20% price.
    '''
    res = pd.DataFrame.from_csv(filename)
    itemsNum = len(res)
    #closeOrder = res['close'].order()
    now = res['close'][0]
    closeOrder = res['close'].sort_values()
    time4_5 = closeOrder[itemsNum*4/5]
    time1_5 = closeOrder[itemsNum/5]
    price1_10 = closeOrder[itemsNum/10]
    diff = round(time4_5-time1_5, 2)
    #rate = decimal.Decimal((time4_5-time1_5)*100/time1_5).quantize(decimal.Decimal('0.00'))
    #rate = '{:.2f}'.format((time4_5-time1_5)*100/time1_5)
    rate = round((time4_5-time1_5)*100/time1_5, 2)
    return (diff, rate, price1_10, now)


def analyzePrice(stdRate, stdRateList, starList, tomorrowStarList):
    '''
    @brief 
    @stdRate, input param, diff rate value.
    @stdRateList, output param, the name list witch rate > stdRasteList.
    @starList, output param, the name list witch %10price >= nowPrice.
    @tomorrowStarList, output param, the name list witch ((rate > stdRateList) && (%10price >= nowPrice))
    '''
    #dstPath = "/home/intranet/pythonPractice/"
    dstPath = "/home/RabinHu/StockInspector/database/chuangyeban"
    postfix = 'csv'  
    data = pd.DataFrame(columns=['name','diff','rate', '10%', 'now'])
    for file in os.listdir(dstPath):
        if file.endswith(postfix):
            (diff, rate, price1_10, now) = __analyzePrice(file)
            ## must set index, otherwith cant set in data.
            se = pd.Series([file, diff, rate, price1_10, now], index=['name','diff','rate','10%','now'])
            data = data.append(se, ignore_index=True)
            ## rabinhu, find watch code.
            fixNow = now - 2
            if price1_10 >= now:
            #if price1_10 >= fixNow:
                print '\033[1;31;40m------------find Star: \033[0m', file
                starList.append(file)
    print '\033[1;31;40m------------Sort with rate----------\033[0m'
    #dataRate = data.sort(columns='rate', ascending=False)
    dataRate = data.sort_values(by='rate', ascending=False)
    print dataRate
    #for idx, row in dataRate.iterrows():
    #    print idx, row

    ## get intersection from stdRateList and starList.
    stdRateName = dataRate[dataRate['rate']>stdRate]['name']
    for idx, name in stdRateName.iteritems():
        stdRateList.append(name)
    #intersectionList = list(set(stdRateList).intersection(set(starList)))
    for name in stdRateList:            
        if starList.count(name) != 0:
            tomorrowStarList.append(name)

    #print '\033[1;31;40m------------Sort with diff----------\033[0m'
    ##dataDiff = data.sort(columns='diff', ascending=False)
    #dataDiff = data.sort_values(by='diff', ascending=False)
    #print dataDiff



def price(filename):
    '''
    '''
    print '\033[1;32;40m>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\033[0m', filename
    ##res = pd.core.frame.DataFrame.from_csv('qzkj.csv')
    res = pd.DataFrame.from_csv(filename)
    itemsNum = len(res)

    print itemsNum  ##the number of items.
    print '-----------------价值划线'
    closeMax = res['close'].max()
    closeMin = res['close'].min()
    MaxSubtractMin = closeMax - closeMin ##sub = Subtract
    print 'max: ', closeMax
    print 'mean: ', res['close'].mean()
    print 'min: ', closeMin
    print 'max-min: ', MaxSubtractMin 
    #print '\033[1;31;40mmedian: \033[0m', res['close'].median()

    print '-----------------时间划线'
    ## cant sort cause [open,high,close,low,volume,amount] was a object.
    #print res.sort(['close'], ascending=[True])
    ## new dataframe sort method.
    #print res.sort_values(by='clode', ascending=False)
    #closeOrder = res['close'].order()
    closeOrder = res['close'].sort_values()
    #print closeOrder
    time4_5 = closeOrder[itemsNum*4/5]
    time1_5 = closeOrder[itemsNum/5]
    print '80%: ', time4_5
    print '75%: ', closeOrder[itemsNum*3/4]
    print '50%: ', closeOrder[itemsNum/2]
    print '33%: ', closeOrder[itemsNum/3]
    print '25%: ', closeOrder[itemsNum/4]
    print '20%: ', time1_5
    print '10%: ', closeOrder[itemsNum/10]
    print '\033[1;31;40mdif(80-20):\033[0m', time4_5 - time1_5, ' \033[1;31;40mrate(diff/20):\033[0m', (time4_5-time1_5)*100/time1_5, " Now: ", res['close'][0]
  
    #print '>>>>--------------->>>>>价值<?的日子里'
    #print res[res['close']<price1_3]
    #print '<<<<<----------------------------<<<<<<<'
    #print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'


def downloadList():
    '''
    call download()
    '''
    startTime = "2013-08-30"
    endTime = "2017-10-10"
    ##download('000423', startTime, endTime, '000423.csv') #东阿阿胶
    #price('000423.csv')
    ##download('002467', startTime, endTime, '002467.csv') #二六三
    #price('002467.csv')
    ##<44#download('002749', startTime, endTime, '002749.csv') #国光股份 *
    ##<44#price('002749.csv')
    ##download('002818', startTime, endTime, '002818.csv') #富林美
    #price('002818.csv')
    ##<44#download('300026', startTime, endTime, '300026.csv') #红日药业
    ##<44#price('300026.csv')
    ##<44#showLittle('300026.csv', 4.4)
    ##<44#download('300105', startTime, endTime, '300105.csv') #龙源技术
    #price('300105.csv')
    ##showLittle('300105.csv', 7.16)
    ##download('300106', startTime, endTime, '300106.csv') #西部牧业
    #price('300106.csv')
    ##showLittle('300106.csv', 9.99)
    ##download('300124', startTime, endTime, '300124.csv') #汇川科技
    #price('300124.csv')
    ##download('300139', startTime, endTime, '300139.csv') #晓程科技
    #price('300139.csv')
    ##download('300147', startTime, endTime, '300147.csv') #香雪制药
    #price('300147.csv')
    ##showLittle('300147.csv', 10.05)
    ##download('300164', startTime, endTime, '300164.csv') #通源石油
    #price('300164.csv')
    ##showLittle('300164.csv', 6.06)
    ##download('300169', startTime, endTime, '300169.csv') #天晟新材
    #price('300169.csv')
    ##download('300171', startTime, endTime, '300171.csv') #东富龙
    #price('300171.csv')
    ##download('300273', startTime, endTime, '300273.csv') #和佳股份
    #price('300273.csv')
    ##showLittle('300273.csv', 10.43)
    ##download('300275', startTime, endTime, '300275.csv') #梅安森
    #price('300275.csv')
    ##download('300369', startTime, endTime, '300369.csv') #绿盟科技
    #price('300369.csv')
    ##download('300380', startTime, endTime, '300380.csv') #安硕信息
    #price('300380.csv')
    ##<44#download('300403', startTime, endTime, '300403.csv') #地尔汉宇 *
    ##<44#price('300403.csv')
    ##download('300425', startTime, endTime, '300425.csv') #环能科技
    #price('300425.csv')
    ##download('300458', startTime, endTime, '300458.csv') #全志科技
    #price('300458.csv')
    ##<44#download('300471', startTime, endTime, '300471.csv') #度普股份
    ##<44#price('300471.csv')
    ##download('300474', startTime, endTime, '300474.csv') #景嘉微
    #price('300474.csv')
    ##<44#download('300487', startTime, endTime, '300487.csv') #蓝晓科技
    ##<44#price('300487.csv')
    ##download('600519', startTime, endTime, '600519.csv') #贵州茅台
    #price('600519.csv')
    ##<44#download('300613', startTime, endTime, '300613.csv') #富瀚微
    ##<44#price('300613.csv')
    ##download('600773', startTime, endTime, '600773.csv') #西藏诚投
    #price('600773.csv')
    ##<44#download('603566', startTime, endTime, '603566.csv') #普莱柯 *
    ##<44#price('603566.csv')

    #download('', startTime, endTime, '.csv') #


if __name__ == '__main__':  
    '''                              
    download db, once time can download 2 code.
    '''                              
    #downloadList()

    '''                              
    analyze db.
    '''                              
    stdRateLst = []
    starLst = []
    tomorrowStarLst = []
    analyzePrice(45, stdRateLst, starLst, tomorrowStarLst)
    #for file in stdRateLst:
    #for file in starLst:
    for file in tomorrowStarLst:
        price(file)

