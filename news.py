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

def notices(code, urls):
    try:
        tm = datetime.datetime.now().strftime('%Y-%m-%d');
        res = ts.get_notices(code, tm)
        ##print len(tuple(res.index)), len(res)#, res.nrow()
        idxNum = len(res)
        for idx in range(idxNum):
            contentUrl = res.ix[idx, 'url']
            urls.append(contentUrl)
        return res.to_html()
    except Exception, e:
        logger.warnLog("Warn: notices data empty:", e)
        return None

import email.MIMEMultipart# import MIMEMultipart  
#import email.MIMEText# import MIMEText  
#import email.MIMEBase# import MIMEBase  
#import mimetypes  

if __name__ == '__main__':  
    codes = ["300458", "300369", "002467"]
    for code in codes:
        urls = []
        res = notices(code, urls)
        if res != None:
            ## write res in mail. 
            msg = email.MIMEMultipart.MIMEMultipart()
            body = email.MIMEText.MIMEText(res, 'html', 'utf-8')
            msg.attach(body) 
            ## write attachemtn into mail and send mail.
            for url in urls:
                data = ts.notice_content(url)
                att = email.mime.text.MIMEText(data, 'plain', 'utf-8')
                att.add_header('content-disposition','attachment',filename='data.txt')
                #att["Content-Disposition"] = 'attachment; filename="data.txt"'
                msg.attach(att)
            mail = KingMail()
            mail.sendWithAttachment(msg, 'news')

