#!/usr/bin/env python
# coding=utf-8

import os
import tushare as ts  
import pandas as pd
import datetime
import time
from  KingMail import KingMail
from ProCommon import logger
  
import sys
reload(sys)
sys.setdefaultencoding('utf8')  
#print 'sys.getdefaultencoding', sys.getdefaultencoding() 

def notices(code, urls, tm):
    try:
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
    checktm = datetime.datetime.now().strftime('%Y-%m-%d');
    for code in codes:
        urls = []
        res = notices(code, urls, checktm)
        if res != None:
            recordfile = "/tmp/" + code + ".news"
            if (os.path.isfile(recordfile)):
                filectime = os.stat(recordfile).st_ctime
                filectimestr = time.strftime('%Y-%m-%d',time.localtime((filectime)))
                if checktm != filectimestr:
                    logger.warnLog("Warn: delete old news:", recordfile)
                    os.remove(recordfile)
                    ifs = open(recordfile, "w")
                    recordurls = ""
                else:
                    ifs = open(recordfile, "r+")
                    recordurls = ifs.read()
            else:
                ifs = open(recordfile, "w")
                recordurls = ""
            ## write res in mail. 
            msg = email.MIMEMultipart.MIMEMultipart()
            body = email.MIMEText.MIMEText(res, 'html', 'utf-8')
            msg.attach(body) 
            ## write attachemtn into mail and send mail.
            hasmail = False
            for url in urls:
                if recordurls.find(url) != -1:
                    logger.infoLog("Info: url has exist..:", url)
                    continue
                data = ts.notice_content(url)
                att = email.mime.text.MIMEText(data, 'plain', 'utf-8')
                att.add_header('content-disposition','attachment',filename='data.txt')
                #att["Content-Disposition"] = 'attachment; filename="data.txt"'
                msg.attach(att)
                hasmail = True
                ifs.write(url)
                ifs.write('\n')
            ifs.close()
            if hasmail:
                mail = KingMail()
                mail.sendWithAttachment(msg, 'news')

