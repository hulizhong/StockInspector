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

def notices(code):
    try:
        tm = datetime.datetime.now().strftime('%Y-%m-%d');
        res = ts.get_notices(code, tm)
        return res.to_html()
    except Exception, e:
        logger.warnLog("Warn: notices data empty:", e)
        return None

if __name__ == '__main__':  
    mail = KingMail()
    codes = ["300458", "300369", "002467"]
    for code in codes:
        res = notices(code)
        if res != None:
            mail.sendhtml(res, 'news')


