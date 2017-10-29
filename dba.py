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


class DBA(object):
    """
    """
    def __init__(self, stdRate=60, fixNowFlag=False, fixValue=1.0):
        '''
        '''
        ## makde stdRate = ((%80-%20)*100)/%20
        self.stdRate = stdRate
        ## the name list witch rate > stdRasteList.
        self.stdRateList = []
        ## the name list witch %10price >= nowPrice.
        self.starList = []
        ## the name list witch ((rate > stdRateList) && (%10price >= nowPrice))
        self.tomorrowStarList = []
        ## the csvPath
        self.dstPath = "./"
        ## use fix price.
        self.fixPriceFlag = fixNowFlag
        self.fixPrice = fixValue
        self.exceptList = ["300392.csv", "300431.csv", "002796.csv", "002071.csv", "002413", "002164.csv"]


    def __analyzePrice(self, filename):
        '''
        called by analyzePrice, return (diff, rate) base 80%-20% price.
        '''
        try:
            res = pd.DataFrame.from_csv(filename)
            itemsNum = len(res)
            now = res['close'][0]
            #closeOrder = res['close'].order()
            closeOrder = res['close'].sort_values()
            time4_5 = closeOrder[itemsNum*4/5]
            time1_5 = closeOrder[itemsNum/5]
            price1_10 = closeOrder[itemsNum/10]
            diff = round(time4_5-time1_5, 2)
            rate28 = round((time4_5-time1_5)*100/time1_5, 2)
            rateNow = round((time4_5-now)*100/now, 2)
            return (diff, rate28, price1_10, now, rateNow)
        except Exception as er:
            print filename, " >> ", er
            return (0, 0, 0, 0, 0)
        


    def analyzePrice(self):
        '''
        @brief 
        '''
        postfix = 'csv'  
        data = pd.DataFrame(columns=['name', 'diff', '28rate', '10%', 'now', 'nowrate'])
        for file in os.listdir(self.dstPath):
            if file.endswith(postfix):
                (diff, rate28, price1_10, now, rateNow) = self.__analyzePrice(file)
                se = pd.Series([file, diff, rate28, price1_10, now, rateNow], index=['name','diff','28rate','10%','now', 'nowrate'])
                data = data.append(se, ignore_index=True)
                ## rabinhu, find watch code.
                fixNow = now
                if self.fixPriceFlag == True:
                    fixNow = now - self.fixPrice
                if price1_10 >= fixNow:
                    #print '\033[1;31;40m------------find Star: \033[0m', file
                    self.starList.append(file)
        print '\033[1;31;40m------------Sort with rate----------\033[0m'
        sortByNowrate = True ## sort by nowrate.
        #sortByNowrate = False ## sort by 28rate.
        if sortByNowrate:
            #dataRate = data.sort(columns='28rate', ascending=False)
            dataRate = data.sort_values(by='nowrate', ascending=False)
            for idx, row in dataRate.iterrows():
                print "%s, diff: %6.2f, 28rate: %6.2f, 10: %6.2f, now: %6.2f, nowrate: %6.2f" % (row['name'], row['diff'], row['28rate'], row['10%'], row['now'], row['nowrate'])
            ## get intersection from stdRateList and starList.
            stdRateName = dataRate[dataRate['nowrate']>self.stdRate]['name']
            for idx, name in stdRateName.iteritems():
                self.stdRateList.append(name)
            for name in self.stdRateList:            
                if self.starList.count(name) != 0 and self.exceptList.count(name) == 0:
                    self.tomorrowStarList.append(name)
        else:
            dataRate = data.sort_values(by='28rate', ascending=False)
            for idx, row in dataRate.iterrows():
                print "%s, diff: %6.2f, 28rate: %6.2f, 10: %6.2f, now: %6.2f, nowrate: %6.2f" % (row['name'], row['diff'], row['28rate'], row['10%'], row['now'], row['nowrate'])
            ## get intersection from stdRateList and starList.
            stdRateName = dataRate[dataRate['28rate']>self.stdRate]['name']
            for idx, name in stdRateName.iteritems():
                self.stdRateList.append(name)
            for name in self.stdRateList:            
                if self.starList.count(name) != 0 and self.exceptList.count(name) == 0:
                    self.tomorrowStarList.append(name)


    def price(self, filename, isColor=True):
        '''
        '''
        if isColor:
            print '\033[1;32;40m>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\033[0m', filename
        else:
            print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', filename
        ##res = pd.core.frame.DataFrame.from_csv('qzkj.csv')
        res = pd.DataFrame.from_csv(filename)
        now = res['close'][0]
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
        rateNow = round((time4_5-now)*100/now, 2)
        print '80%: ', time4_5
        print '75%: ', closeOrder[itemsNum*3/4]
        print '50%: ', closeOrder[itemsNum/2]
        print '33%: ', closeOrder[itemsNum/3]
        print '25%: ', closeOrder[itemsNum/4]
        print '20%: ', time1_5
        print '10%: ', closeOrder[itemsNum/10]
        if isColor:
            print '\033[1;31;40mdif(80-20):\033[0m', time4_5 - time1_5, ' \033[1;31;40mrate(diff/20):\033[0m', (time4_5-time1_5)*100/time1_5, " Now: ", res['close'][0], " nowrate: ", reateNow
        else:
            print 'dif(80-20):', time4_5 - time1_5, ' rate(diff/20):', (time4_5-time1_5)*100/time1_5, " Now: ", res['close'][0], " nowrate: ", rateNow
      
        #print '>>>>--------------->>>>>价值<?的日子里'
        #print res[res['close']<price1_3]
        #print '<<<<<----------------------------<<<<<<<'
        #print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'

    def printStdRateLst(self):
        '''
        '''
        for file in self.stdRateList:
            self.price(file)

    def printStarLst(self):
        '''
        '''
        for file in self.starList:
            self.price(file)

    def printTomorrowStarLst(self, toFileFlag=False):
        '''
        '''
        if toFileFlag == True:
            fp = open("tomorrowStartLst.lst", "w")
            for file in self.tomorrowStarList:
                fp.write(file + "\n")
            fp.close()
        for file in self.tomorrowStarList:
            self.price(file, False)

    def showBig(self, filename, diffPri):
        '''
        '''
        print filename, '-----------------价值>', diffPri, '的日子里'
        res = pd.DataFrame.from_csv(filename)
        res = res[res['close'] > diffPri]
        for index, row in res.iterrows():
            print index, row['close']


    def showLittle(self, filename, diffPri):
        '''
        '''
        print filename, '-----------------价值<', diffPri, '的日子里'
        res = pd.DataFrame.from_csv(filename)
        res = res[res['close'] < diffPri]
        for index, row in res.iterrows():
            print index, row['close']



if __name__ == '__main__':  
    '''                              
    analyze db.
    '''                              
    dba = DBA(stdRate=40)
    #dba = DBA(stdRate=40, fixNowFlag=True, fixValue=1.5)
    dba.analyzePrice()
    dba.printTomorrowStarLst()
    #dba.printTomorrowStarLst(True)

    #dba.price("300369.csv")
    #dba.showLittle("300369.csv", 9.80)
    #dba.price("300273.csv")
    #dba.showLittle("300273.csv", 10.50)
    #dba.price("002344.csv")
    #dba.showLittle("002344.csv", 8.08)

    #dba.printStarLst()
    #dba.printStdRateLst()
    #dba.showLittle("300369.csv", 10.00)

