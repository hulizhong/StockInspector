#!/usr/bin/env python
# coding=utf-8

from KingMail import KingMail
from ProCommon import logger
import sys
import requests
from requests.exceptions import RequestException
from pyquery import PyQuery as PQ
#from lxml import etree
import codecs
import chardet
import time
import datetime
import re
import os

'''
Python在安装时，默认的编码是ascii，当程序中出现非ascii编码时，python的处理常常会报这样的错
    UnicodeDecodeError: 'ascii' codec can't decode byte 0x?? in position 1: ordinal not in range(128)，
python没办法处理非ascii编码的，此时需要自己设置将python的默认编码，一般设置为utf8的编码格式。`
'''
#print 'sys.getdefaultencoding', sys.getdefaultencoding()  
reload(sys)
sys.setdefaultencoding('utf8')  
#print 'sys.setdefaultencoding utf8'
#print 'sys.getdefaultencoding', sys.getdefaultencoding()  
##sys.setdefaultencoding('gb2312')  


class ReqClient(object):
    """
    http client with requests package.
    """
    def __init__(self, argsHeaders):
        '''
        argsHeaders must include 
            "Host": "www.zhihu.com",
        '''
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        }
        for key in argsHeaders.keys():
            self.headers[key] = argsHeaders[key]
        self.doc = None

    def __del__(self):
        pass


    def getPage(self, url, charset='utf8'):
        """
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10, verify=False)
        except RequestException as e:
            logger.errLog('RequestException', e)
            self.doc = None
            return None
        else:
            if response.ok:
                if charset == 'utf8':
                    response.encoding = 'utf8'
                    self.doc = response.text
                else:
                    #maybe gbk, gb2312, utf8.
                    self.doc = (response.content.decode(charset)).encode('utf8')
                return self.doc
            else:
                logger.errLog('get not ok, ', response.code)
                self.doc = None
                return None


    def savePage(self, url, file, charset='utf8'):
        """
        """
        if self.doc == None:
            res = self.getPage(url, charset)
            if (res == None):
                return False
        fp = open(file, 'wb')
        fp.write(self.doc)
        fp.close()
        return True


    def parsePage(self):
        """
        """
        if self.doc == None:
            logger.errLog('invalid content')
            return None
        try:
            pg = PQ(self.doc)
        except Exception as e:
            logger.errLog('Exception ', e)



class SceeaNews(ReqClient):
    """
    parse http://www.sceea.cn/List/NewsList_18_1.html and get news.
    """
    def __init__(self, argsHeaders):
        super(SceeaNews, self).__init__(argsHeaders)

    def parsePage(self):
        """
        """
        if self.doc == None:
            logger.warnLog('invalid content')
            return None
        try:
            recordfile = "/tmp/sceea.news"
            if (os.path.isfile(recordfile)):
                filectime = os.stat(recordfile).st_ctime
                filetimestr = time.strftime('%Y-%m-%d',time.localtime(filectime))
                #filetimestr = "2017-08-01"
                checktm = datetime.datetime.now().strftime('%Y-%m-%d');
                #checktm = "2017-08-01"
                if checktm != filetimestr:
                    logger.warnLog("Warn: delete old news:", recordfile)
                    os.remove(recordfile)
                    ifs = open(recordfile, "w")
                    recordnews = ""
                else:
                    ifs = open(recordfile, "r+")
                    recordnews = ifs.read()
            else:
                ifs = open(recordfile, "w")
                recordnews = ""

            pg = PQ(self.doc)
            htmltime = time.strftime('%Y/%m/%d',time.localtime())
            #htmltime = "2017/08/01"
            maildata = u""
            for data in pg('div'):
                if PQ(data).attr('class') == 'item':
                    newsTitle = PQ(data).find('a').attr('title')
                    newsDate = PQ(data).find('b').text()
                    if (newsDate == htmltime):
                        if recordnews.find(newsTitle) != -1:
                            logger.infoLog("Info: url has exist..:", newsTitle)
                            continue
                        else:
                            maildata = maildata + newsTitle + u"\n\n";
                            ifs.write(newsTitle)
                            ifs.write('\n')
            ifs.close()
            if len(maildata) != 0:
                mail = KingMail()
                mail.sendtxt(content=maildata, sub='高考志愿')
        except Exception as e:
            logger.errLog('Exception ', e)

sceeaHeader = {"Host":"www.sceea.cn"}
req = SceeaNews(sceeaHeader)
resp = req.getPage("http://www.sceea.cn/List/NewsList_18_1.html")
req.parsePage()

