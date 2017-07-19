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
#print 'sys.getdefaultencoding', sys.getdefaultencoding() 

def realtime_quotes(codes, hasAlter):
    try:
        res = ts.get_realtime_quotes(codes)
        msg = ""
        msgPositive = "Positive-Alter\r\n"
        msgNegative = "Negative-Alter\r\n"
        rowNum = len(res)
        for row in range(rowNum):
            qStart = float(res.ix[row, 'open'])
            qClose = float(res.ix[row, 'pre_close'])
            qCurrent = float(res.ix[row, 'price'])
            qVolume = int(res.ix[row, 'volume'])/100
            qRate = ((qCurrent-qStart)*100)/qStart
            qRate2 = ((qCurrent-qClose)*100)/qStart
            if (qRate > 3):
                alterData = "    %s  %.2f(%.2f), %.2f(%.2f), %d\r\n" % (res.ix[row, 'name'], qRate, qRate2, qCurrent, qClose, qVolume)
                msgPositive += alterData
                hasAlter.append('succeed')
            elif (qRate < -3):
                alterData = "    %s  %.2f(%.2f), %.2f(%.2f), %d\r\n" % (res.ix[row, 'name'], qRate, qRate2, qCurrent, qClose, qVolume)
                msgNegative += alterData
                hasAlter.append('succeed')
            else:
                pass
        msg = msgPositive + "\r\n" + msgNegative
        return msg 
    except Exception, e:
        logger.errLog("Error: realtime_quotes", e)
        return ""

import email.MIMEMultipart

if __name__ == '__main__':  
    codes = ["300458", "300369", "002467"]
    hasAlter = []
    res = realtime_quotes(codes, hasAlter)
    if len(hasAlter) != 0:
        mail = KingMail()
        mail.sendtxt(res, 'quotes')

