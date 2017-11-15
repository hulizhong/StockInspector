#!/usr/bin/env python
# coding=utf-8


import smtplib
import chardet
from email.mime.text import MIMEText
from email.header import Header
from ProCommon import logger
from EncDec import EncDecGraph
 
class KingMail(object):
    """
    email sent class replace sms notify. 
    """
    def __init__(self, isSSL=True):
        try:
            self.mailhost = "smtp.yeah.net"
            self.user = "rabinhu"
            self.encpswd = "0lz96ur77o"
            self.sender = 'rabinhu@yeah.net'
            self.receivers = ['rabinhu@126.com']
            pswd = EncDecGraph()
            if isSSL:
                logger.infoLog('will connect mail server with ssl.')
                self.smtpObj = smtplib.SMTP_SSL()
                ##when has error and u can't see before, then u can set debug switch and analysis it.
                ##Q1: app rasie SMTPServerDisconnected('Connection unexpectedly closed',)
                ##Q1: http://feedback.mail.126.com/antispam/complain.php?user=rabinhu@yeah.net
                ## A1: the yeah.net anti spam.
                #self.smtpObj.set_debuglevel(1)
                self.smtpObj.connect(self.mailhost, 465)
            else:
                logger.infoLog('will connect mail server with non-ssl.')
                self.smtpObj = smtplib.SMTP()
                self.smtpObj.connect(self.mailhost, 25)
            logger.infoLog('will login mail server.')
            self.smtpObj.login(self.user, pswd.dec(self.encpswd))  
        except smtplib.SMTPException, e:
            logger.errLog("Error: Login mail server Failed, cause:", e)
        except:
            logger.errLog("Error: __init__ failed.")

    def __del__(self):
        ### bug, Exception smtplib.SMTPServerDisconnected: SMTPServerDisconnected('Connection unexpectedly closed',)
        #self.smtpObj.quit()
        pass

    def sendtxt(self, content, sub=""):
        try:
            ### text/plain will due to outlook recv mail as txt file.
            message = MIMEText(content, 'plain', 'utf-8')
            if len(sub) == 0:
                message['Subject'] = Header('金花策略', 'utf-8')
            else:
                newsub = "金花策略 - " + sub
                message['Subject'] = Header(newsub, 'utf-8')
            message['From'] = self.sender
            ### bug, if receivers is a list, use .join(receivers)
            #message['To'] = self.receivers
            message['To'] = ','.join(self.receivers)
            self.smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            return True
        except smtplib.SMTPException, e:
            #logger.errLog("Error: 无法发送邮件, cause:", e)
            logger.errLog("Error: sendtxt can't send mail, cause:", e)
            return False
            #print isinstance(e.smtp_error, unicode)
            #print isinstance(e.smtp_error, 'utf-8')
            #print type(e)
            #fencoding=chardet.detect(e.smtp_error)
            #print fencoding

    def sendhtml(self, content, sub=""):
        try:
            ### text/plain will due to outlook recv mail as txt file.
            message = MIMEText(content, 'html', 'utf-8')
            if len(sub) == 0:
                message['Subject'] = Header('金花策略', 'utf-8')
            else:
                newsub = "金花策略 - " + sub
                message['Subject'] = Header(newsub, 'utf-8')
            message['From'] = self.sender
            ### bug, if receivers is a list, use .join(receivers)
            #message['To'] = self.receivers
            message['To'] = ','.join(self.receivers)
            self.smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            return True
        except smtplib.SMTPException, e:
            #logger.errLog("Error: 无法发送邮件, cause:", e)
            logger.errLog("Error: sendhtml can't send mail, cause:", e)
            return False
            #print isinstance(e.smtp_error, unicode)
            #print isinstance(e.smtp_error, 'utf-8')
            #print type(e)
            #fencoding=chardet.detect(e.smtp_error)
            #print fencoding

    def sendWithAttachment(self, message, sub=""):
        try:
            if len(sub) == 0:
                message['Subject'] = Header('金花策略', 'utf-8')
            else:
                newsub = "金花策略 - " + sub
                message['Subject'] = Header(newsub, 'utf-8')
            message['From'] = self.sender
            ### bug, if receivers is a list, use .join(receivers)
            #message['To'] = self.receivers
            message['To'] = ','.join(self.receivers)
            self.smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            return True
        except smtplib.SMTPException, e:
            #logger.errLog("Error: 无法发送邮件, cause:", e)
            logger.errLog("Error: sendWithAttachment can't send mail, cause:", e)
            return False

if __name__ == '__main__':
    '''
    for test.
    '''
    k = KingMail()
    fs = open("/home/RabinHu/StockInspector/conf.xml")
    dt = fs.read()
    k.sendhtml(dt, 'news')

