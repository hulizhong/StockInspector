#!/usr/bin/env python
# coding=utf-8

import tushare as ts  
import pandas as pd
import datetime
from  KingMail import KingMail
from ProCommon import logger
  
import sys
reload(sys)
sys.setdefaultencoding('utf8')  

def getACodes(dic):
    '''
    get code & goal price.
    A. 价格周期性循环，定期分红；
    '''
    dic['600827'] = 6.0  #百联股份
    dic['600266'] = 6.0  #北京城建
    dic['601117'] = 5.0  #中国化学
    dic['600279'] = 3.8  #重庆港九 +++
    dic['000039'] = 8.0  #中集集团
    dic['600239'] = 2.0  #云南城投
    dic['600106'] = 2.3  #重庆路桥
    dic['000900'] = 2.9  #现代投资
    dic['600665'] = 2.5  #天地源
    dic['000926'] = 5.6  #福星股份
    dic['600510'] = 4.0  #黑牡丹
    dic['000402'] = 4.0  #金融街
    dic['600068'] = 5.2  #葛洲坝
    dic['000903'] = 2.0  #云内动力
    dic['000623'] = 10.0 #吉林敖东
    dic['600295'] = 6.37 #鄂尔多斯 ++
    dic['600382'] = 5.2  #广东明珠
    dic['600051'] = 5.4  #宁波联合
    dic['002092'] = 4.57 #中泰化学
    dic['600428'] = 3.05 #中远海特
    #dic[''] =  #
    #dic[''] =  #

def realtime_quotes(codesDic, hasData):
    try:
        codes = codesDic.keys()
        res = ts.get_realtime_quotes(codes)
        msg = ""
        msgPositive = "Positive-Alter\r\n"
        msgNegative = "Negative-Alter\r\n"
        rowNum = len(res)
        for row in range(rowNum):
            qStart = float(res.ix[row, 'open'])
            code = res.ix[row, 'code']
            if qStart == 0: ## stop board
                print "code.", code, "not start."
                continue
            qClose = float(res.ix[row, 'pre_close'])
            qCurrent = float(res.ix[row, 'price'])
            qTime = res.ix[row, 'time']

            # the diff price(current & goal) rate.
            if qCurrent > codesDic[code]:
                diffRate = ((qCurrent-codesDic[code])*100) / float(codesDic[code])
            else:
                diffRate = -0.0

            # get the code name.
            if len(res.ix[row, 'name']) == 3:
                codename = "--" + res.ix[row, 'name']
            else:
                codename = res.ix[row, 'name']

            print "%6s %4s preclose.%6.2f current.%6.2f < %6.2f diffRate.%6.2f" % (code, codename, qClose, qCurrent, codesDic[code], diffRate)
            if (qClose <= codesDic[code] or qCurrent <= codesDic[code]):
                alterData = "    %s  P: %.2f(%.2f), goal(%.2f) %s\r\n" % (codename, qCurrent, qClose, codesDic[code], qTime)
                msgPositive += alterData
                hasData["has"] = True
            else:
                pass
        msg = msgPositive + "\r\n" + msgNegative
        #print msg
        return msg 
    except Exception, e:
        logger.errLog("Error: realtime_quotes", e)
        return ""

import email.MIMEMultipart

if __name__ == '__main__':  
    codes = {}
    getACodes(codes)
    hasAlter = {"has" : False}
    mailContent = realtime_quotes(codes, hasAlter)
    if hasAlter["has"]:
        print 'has content.\n', mailContent
        mail = KingMail()
        res = mail.sendtxt(mailContent, 'goal')
        if res == False:
            logger.errLog("Error: send quotes mail failed.")
        else:
            logger.infoLog("Info: send quotes mail succeed.")

