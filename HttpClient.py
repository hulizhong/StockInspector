#!/usr/bin/env python
# coding=utf-8

from ProCommon import logger 
from ConfigParse import ConfigParse
import ssl
import httplib
import time

#############################################################
#goal: http client
#############################################################
class HttpClient(object):
    """
    http client with python httplib
    make sure python-httplib2 has been installed by apt-get.
        /usr/share/pyshared/httplib2/ depends on /usr/lib/python2.7/httplib.py
    """
    def __init__(self, xmlfile):
        try:
            self.connok = False 
            config = ConfigParse(xmlfile)
            isssl = config.getValue('config.http.isssl')
            host = config.getValue('config.http.host')
            port = config.getValue('config.http.port')
            #capath = config.getValue('config.http.')
            #certpath = config.getValue('config.http.')
            #keypath = config.getValue('config.http.')

            ### set header
            self.header = {"Content-Type": "application/json", "Accept-Type":"application/json"}

            if isssl == 'false':
                self.conn = httplib.HTTPConnection(host, int(port))
            else:
                self.conn = httplib.HTTPSConnection(host, int(port))
                #self.conn._context.check_hostname = False
                #self.conn._context.verify_mode = ssl.CERT_NONE
            self.connok = True
        except Exception,e:
            #traceback.print_exc()
            logger.errLog("HttpClient init failed, des:", e)


    def __del__(self):
        try:
            if self.connok == False:
                raise AssertionError("HttpClient connection not ready.")
            self.conn.close()
        except Exception,e:
            logger.errLog("HttpClient del failed, des:", e)
        

    def sendRequest(self, method, url, body=None, head=None):
        """
        :param method, support POST, DELETE, PUT, GET
        """
        try:
            logger.errLog("----in:", time.ctime())
            if self.connok == False:
                raise AssertionError("HttpClient connection not ready.")

            logger.debugLog("httpclient.request", url)
            if head == None:
                self.conn.request(method, url, body, self.header)
            else:
                newheader = dict(self.header, **head)
                self.conn.request(method, url, body, newheader)
        except Exception,e:
            logger.errLog("send request excption cause: ", e, " url:", url)
            return None
        else:
            res = self.conn.getresponse()
            if res.status == 200:
                #res is HTTPResponse obj
                logger.errLog("----outok:", time.ctime())
                return res
            else:
                logger.errLog('send request failed, cause recv: ', res.status, res.read())
                return None

