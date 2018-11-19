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
from collections import OrderedDict

reload(sys)
sys.setdefaultencoding('utf8')  

class ReqClient(object):
    """
    http client with requests package.
    """
    def __init__(self):
        '''
        argsHeaders must include 
            "Host": "www.zhihu.com",
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
        '''
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Host": "gateio.io",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        }
        self.doc = None
        self.isFastCheck = False
        self.fastCheckFile = "/tmp/btscnt"
        #self.isLocalCache = True
        self.isLocalCache = False
        self.isSndMail = False

    def __del__(self):
        pass


    def getPage(self, urls, charset='utf8'):
        """
        """
        if (self.isFastCheck):
            if os.path.exists(self.fastCheckFile) == True:
                f = open(self.fastCheckFile, "r+")
                cnt = f.read()
                if int(cnt) == 0:
                    f.close()
                    os.remove(self.fastCheckFile)
                else:
                    newCnt = int(cnt)-1
                    f.seek(0, 0)
                    f.write(str(newCnt))
                    f.close()
                    logger.debugLog('Not need to detecting.')
                    return

        res = ""
        for it in urls:
            url = it["url"]
            name = it["name"]
            ret = self.__getPage(url, name, charset)
            if ret is not None:
                res = res + "\n" + ret
        if res != "":
            if (self.isSndMail):
                mail = KingMail()
                mail.sendtxt(content=str(res), sub='BTS')
            else:
                print res
            logger.infoLog('send an bts email.')
        else:
            logger.debugLog('nothing warnning in bts detected.')
            if (self.isFastCheck):
                f = open(self.fastCheckFile, "w")
                f.write("5")
                f.close()


    def __getPage(self, url, name, charset):
        if (self.isLocalCache == False):
            try:
                response = requests.get(url, headers=self.headers, timeout=10, verify=False)
                if response.ok:
                    if charset == 'utf8':
                        response.encoding = 'utf8'
                        self.doc = response.text
                    else:
                        #maybe gbk, gb2312, utf8.
                        self.doc = (response.content.decode(charset)).encode('utf8')
                    ff = open("/tmp/x.x", "w")
                    ff.write(self.doc)
                    ff.close()
                else:
                    logger.errLog('get not ok, ', response.code)
                    self.doc = None
                    return None
            except RequestException as e:
                logger.errLog('RequestException', e)
                return None
            except Exception as e:
                logger.errLog('DownloadException', e)
                return None

        try:
            f = open("/tmp/x.x", "r")
            docc = f.read()
            res = OrderedDict()
            ## get the high's bid.
            idx = re.search("tHigh", docc, flags=0).start()
            f.seek(idx+7, 0)
            bidstr = f.read(6)
            if bidstr[5] != "<":
                bidH = float(bidstr)
            else:
                bidstr = bidstr[0:4]
                bidH = float(bidstr)
            res["Hig"] = bidH
	     
            ## get the Low's bid.
            idx = re.search("tLow", docc, flags=0).start()
            f.seek(idx+6, 0)
            bidstr = f.read(6)
            if bidstr[5] != "<":
                bidL = float(bidstr)
            else:
                bidstr = bidstr[0:4]
                bidL = float(bidstr)
            res["Low"] = bidL
            res["10%"] = round((bidH-bidL)/10.0 + bidL, 3)
            res["90%"] = round((bidH-bidL)*9/10.0 + bidL, 3)
            res["Df"] = round(bidH/bidL, 3)
            res["19Df"] = round(res["90%"]/res["10%"], 3)
 
            ## get the current's bid.                                 
            idx = re.search("datas_bids=\[\[", docc, flags=0).start()
            f.seek(idx+14, 0)
            bidstr = f.read(6)
            bidC = float(bidstr)
            print "---------", bidstr 
            if bidstr[5] != "<":
                bidC = float(bidstr)
            else:
                bidstr = bidstr[0:4]
                bidC = float(bidstr)
            res["Now"] = bidC
            res["Nam"] = name
     
            prettystr1 = "Rat<%5s, %5s>  01P<%6s, %6s>  " %(str(res["Df"]), str(res["19Df"]), str(res["Low"]), str(res["Hig"]))
            prettystr2 = "19P<%5s, %5s> %6s %s" %(str(res["10%"]), str(res["90%"]), str(res["Now"]), res["Nam"])
            prettystr = prettystr1 + prettystr2
            logger.infoLog(prettystr)
            if (self.isSndMail):
                if (name=="lrc") and (bidC>0.752 or bidC<0.552):
                    logger.infoLog('LRC', prettystr)
                    return str(prettystr)
                elif (name=="ae") and (bidC>3.52 or bidC<2.02):
                    logger.infoLog('AE', prettystr)
                    return str(prettystr)
                elif (name=="bts") and (bidC>0.302 or bidC<0.202):
                    logger.infoLog('BTS', prettystr)
                    return str(prettystr)
                else:
                    return None
            else:
                return str(prettystr)
            #if (bidC<res["10%"]) or (bidC>res["90%"]):
            #    return str(res)
            #else:
            #    return None
     
            f.close()
        except Exception as e:
            logger.errLog('ParseException', e)
            f.close()
            return None


if __name__ == '__main__':
    '''
        {"url": "https://gateio.io/trade/BTM_USDT", "name": "btm"},
        {"url": "https://gateio.io/trade/BTO_USDT", "name": "bto"},
        {"url": "https://gateio.io/trade/LRC_USDT", "name": "lrc"},
        {"url": "https://gateio.io/trade/BTS_USDT", "name": "bts"},
        {"url": "https://gateio.io/trade/IOTA_USDT", "name": "iota"},
        {"url": "https://gateio.io/trade/AE_USDT", "name": "ae"},
    '''
    urls = [
        {"url": "https://gateio.io/trade/BTM_USDT", "name": "btm"},
        {"url": "https://gateio.io/trade/BTO_USDT", "name": "bto"},
        {"url": "https://gateio.io/trade/LRC_USDT", "name": "lrc"},
        {"url": "https://gateio.io/trade/BTS_USDT", "name": "bts"},
        {"url": "https://gateio.io/trade/IOTA_USDT", "name": "iota"},
       ]
    req = ReqClient()
    resp = req.getPage(urls)

