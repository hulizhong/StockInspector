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
        self.fileIndustry = "codelst/industry.csv"
        self.fileConcept = "codelst/concept.csv"
        ##download time interval second.
        self.sleepTm = 60


    def __download(self, code):
        '''
        '''
        try:
            filename = code + ".csv"
            #res = ts.get_h_data(code="300458", start="2015-01-11", end="2017-09-20")
            res = ts.get_h_data(code, self.startTm, self.endTm)
            #cant use if res != None:
            if res is not None:
                res.to_csv(filename)
            return True
        except IOError, er:
            #print '1111', er.errno
            print time.time(), "(", code, ") >> ", er
            return False
        except Exception as er:
            print time.time(), "(", code, ") >> ", er
            return False


    def download(self, type):
        '''
        down load trading db to csv file.
        '''
        if type == "sme":
            self.__downloadSme()
        elif type == "gem":
            self.__downloadGem()
        elif type == "industry":
            self.__downloadIndustry()
        elif type == "concept":
            self.__downloadConcept()

    def __downloadSme(self):
        '''
        zhongXiaoBan
        '''
        dfSme = pd.DataFrame.from_csv(self.fileSme)
        seSmeCodeLst = dfSme['code']
        smeLst = []
        for idx, code in seSmeCodeLst.iteritems():
            smeLst.append("00" + str(code))
        for it in smeLst:
            res = self.__download(it)
            while res == False:
                time.sleep(self.sleepTm)
                res = self.__download(it)
            time.sleep(6)

    def __downloadGem(self):
        '''
        chuangYeBan
        '''
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

    def __downloadIndustry(self):
        '''
        '''
        dfIndustry = pd.DataFrame.from_csv(self.fileIndustry)
        seIndustryCodeLst = dfIndustry['code']
        industryLst = []
        for idx, code in seIndustryCodeLst.iteritems():
            if len(str(code)) == 3:
                industryLst.append('000' + str(code))
            elif len(str(code)) == 2:
                industryLst.append('0000' + str(code))
            elif len(str(code)) == 1:
                industryLst.append('00000' + str(code))
            else:
                industryLst.append(str(code))
        for it in industryLst:
            res = self.__download(it)
            while res == False:
                time.sleep(self.sleepTm)
                res = self.__download(it)
            time.sleep(6)

    def __downloadConcept(self):
        '''
        '''
        pass


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

    def downloadWithFile(self, filename):
        '''
        @brief: get A stock code list.
        '''
        fp = open(filename)
        while True:
            oriCode = fp.readline()
            if not oriCode:
                break;
            code = oriCode[0:6]
            res = self.__download(code)
            while res == False:
                time.sleep(self.sleepTm)
                res = self.__download(code)
            time.sleep(6)
        fp.close()


    def getCodeList(self, type):
        '''
        @brief: get A stock code list.
        '''
        if type == "sme":
            self.__getSmeList()
        elif type == "gem":
            self.__getGemList()
        elif type == "industry":
            self.__getIndustryList()
        elif type == "concept":
            self.__getConceptList()

    def __getSmeList(self):
        ## zhongXiaoBan
        sme = ts.get_sme_classified()
        sme.to_csv(self.fileSme)

    def __getGemList(self):
        ## chuangYeBan
        gem = ts.get_gem_classified()
        gem.to_csv(self.fileGem)

    def __getIndustryList(self):
        industry = ts.get_industry_classified()
        industry.to_csv(self.fileIndustry)
        #industry.to_excel("codelst/industry.xlsx")

    def __getConceptList(self):
        concept = ts.get_concept_classified()
        concept.to_csv(self.fileConcept)

    def tst(self, code):
        self.__download(code)


if __name__ == '__main__':  
    cr = Crawler(endTime="2017-11-16")
    #cr.download()
    #cr.getCodeList("sme")
    #cr.getCodeList("industry")
    #cr.getCodeList("concept")
    #cr.download("industry")
    #watchList = ["002344", "300273", "300369"]
    #watchList = ["300369"]
    #cr.downloadWithList(watchList)
    ## the task in weekday.
    cr.downloadWithFile("tomorrowStartLst.lst")

