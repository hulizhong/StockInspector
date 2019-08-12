#!/usr/bin/env python
# coding=utf-8

import tushare as ts  
import pandas as pd
import datetime
from  KingMail import KingMail
from ProCommon import logger
from CodeList import DataItem, StockRepository
from CodeList import insertWatchCode, insertPbLess1Code, insertTraceCode, insertHandingCode
  
import sys
reload(sys)
sys.setdefaultencoding('utf8')  
#print 'sys.getdefaultencoding', sys.getdefaultencoding() 

def realtime_quotes(codes, hasData):
    try:
        res = ts.get_realtime_quotes(codes)
        msg = ""
        msgPositive = "Positive-Alter\r\n"
        msgNegative = "Negative-Alter\r\n"
        rowNum = len(res)
        for row in range(rowNum):
            qStart = float(res.ix[row, 'open'])
            ## stop board
            if qStart == 0:
                continue
            qClose = float(res.ix[row, 'pre_close'])
            qCurrent = float(res.ix[row, 'price'])
            #qVolume = int(res.ix[row, 'volume'])/100
            qTime = res.ix[row, 'time']
            qRate = ((qCurrent-qStart)*100)/qStart
            qRate2 = ((qCurrent-qClose)*100)/qClose
            if (qRate > 3):
                alterData = "    %s  R: %.2f(%.2f), P: %.2f(%.2f), %s\r\n" % (res.ix[row, 'name'], qRate, qRate2, qCurrent, qClose, qTime)
                msgPositive += alterData
                hasData["has"] = True
            elif (qRate < -3):
                alterData = "    %s  R: %.2f(%.2f), P: %.2f(%.2f), %s\r\n" % (res.ix[row, 'name'], qRate, qRate2, qCurrent, qClose, qTime)
                msgNegative += alterData
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
    codes = []
    insertHandingCode({}, codes, "no-use-str")
    hasAlter = {"has" : False}
    mailContent = realtime_quotes(codes, hasAlter)
    if hasAlter["has"]:
        mail = KingMail()
        res = mail.sendtxt(mailContent, 'quotes')
        if res == False:
            logger.errLog("Error: send quotes mail failed.")
        else:
            logger.infoLog("Info: send quotes mail succeed.")

