#!/usr/bin/env python
# coding=utf-8

import tushare as ts  
import pandas as pd
  
import os
import sys
import time
#print 'sys.getdefaultencoding', sys.getdefaultencoding() 
reload(sys)
sys.setdefaultencoding('utf8')  

class Crawler(object):
    '''
    db crawler.
    '''
    def __init__(self, startTime="2013-08-30", endTime=""):
        '''
        @startTime param, start time, must > stop time.
        @endTime param, stop time.
        '''
        self.startTm = startTime
        self.endTm = endTime
        ##save zhongxiaoban list.
        self.fileSme = "codelst/sme.csv"
        ##save chuangyeban list.
        self.fileGem = "codelst/gem.csv"
        ##download time interval second.
        self.sleepTm = 60


    def __download(self, code):
        '''
        '''
        try:
            filename = code + ".csv"
            #res = ts.get_h_data(code="300458", start="2015-01-11", end="2017-09-20")
            res = ts.get_h_data(code, self.startTm, self.endTm)
            if res is not None:
                res.to_csv(filename)
            return True
        except IOError, er:
            #print '1111', er.errno
            print time.time(), " >> ", er
            return False
        except Exception as er:
            print time.time(), " >> ", er
            return False


    def download(self):
        '''
        down load trading db to csv file.
        '''
        ### zhongXiaoBan
        #dfSme = pd.DataFrame.from_csv(self.fileSme)
        #seSmeCodeLst = dfSme['code']
        #smeLst = []
        #for idx, code in seSmeCodeLst.iteritems():
        #    smeLst.append("00" + str(code))
        #count = 0
        #for it in smeLst:
        #    res = self.__download(it)
        #    while res == False:
        #        time.sleep(self.sleepTm)
        #        res = self.__download(it)
        #    #count = count + 1
        #    #if count == 2:
        #    #    count = 0
        #    #    time.sleep(self.sleepTm)
        #    time.sleep(6)

        ## chuangYeBan
        dfGem = pd.DataFrame.from_csv(self.fileGem)
        seGemCodeLst = dfGem['code']
        gemLst = []
        for idx, code in seGemCodeLst.iteritems():
            gemLst.append(str(code))
        for it in gemLst:
            res = self.__download(it)
            while res == False:
                time.sleep(self.sleepTm)
                res = self.__download(it)
            time.sleep(6)


    def downloadWithList(self, codeList):
        '''
        down load trading db to csv file.
        '''
        for it in codeList:
            res = self.__download(it)
            while res == False:
                time.sleep(self.sleepTm)
                res = self.__download(it)
            time.sleep(6)


    def getCodeList(self):
        '''
        @brief: get A stock code list.
        '''
        ### zhongXiaoBan
        #sme = ts.get_sme_classified()
        #sme.to_csv(self.fileSme)
        ## chuangYeBan
        gem = ts.get_gem_classified()
        gem.to_csv(self.fileGem)


if __name__ == '__main__':  
    cr = Crawler(endTime="2017-10-27")
    #cr.getCodeList()
    #cr.download()
    watchList = ["002344", "300273", "300369"]
    cr.downloadWithList(watchList)

