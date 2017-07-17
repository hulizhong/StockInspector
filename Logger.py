#!/usr/bin/env python
# coding=utf-8

from ConfigParse import ConfigParse
import logging
from logging.handlers import RotatingFileHandler

#############################################################
#goal: logger base api
#############################################################
class Logger(object):
    """
    write log with logging lib
    """
    def __init__(self, filename, logfile="/var/log/logger.log"):
        """
        不能重载__init__函数吗，想再弄个直接传配置参数的初始化函数。
        """
        config = ConfigParse(filename)
        maxMB = config.getValue('config.logging.backup')
        maxB = int(maxMB) * 1024 * 1024
        maxbackup = config.getValue('config.logging.maxsize')
        level = config.getValue('config.logging.level')
        ###create logger
        self.logger = logging.getLogger('file')
        if level == "debug":
            self.logger.setLevel(logging.DEBUG)
        elif level == "info":
            self.logger.setLevel(logging.INFO)
        elif level == "warn":
            self.logger.setLevel(logging.WARN)
        elif level == "error":
            self.logger.setLevel(logging.ERROR)
        else:
            print "logging level only can set debug|info|warn|error, now use default info level"
            self.logger.setLevel(logging.INFO)
        ###create file handler
        self.fh = RotatingFileHandler(logfile, maxBytes=maxB, backupCount=int(maxbackup))
        ###create formatter
        fmt = "%(asctime)-15s %(levelname)s %(process)d %(message)s"
        datefmt = '%a %d %b %Y %H:%M:%S'
        self.formatter = logging.Formatter(fmt, datefmt)
        ###add handler to logger
        self.fh.setLevel(logging.DEBUG)
        self.fh.setFormatter(self.formatter)
        self.logger.addHandler(self.fh)

    def debugLog(self, *msg):
        self.logger.debug(msg)

    def infoLog(self, *msg):
        self.logger.info(msg)

    def warnLog(self, *msg):
        self.logger.warning(msg)

    def errLog(self, *msg):
        self.logger.error(msg)
        #str = ''
        #for k in msg:
        #    str += ' ' + k
        #self.logger.error(str)

    def criLog(self, *msg):
        self.logger.critical(msg)

#整个工程应该只有写日志的句柄。
#logger = Logger()

