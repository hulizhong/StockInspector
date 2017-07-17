#!/usr/bin/env python
# coding=utf-8

import psycopg2
from ConfigParse import ConfigParse
from ProCommon import logger

#############################################################
#goal: postgres client
#############################################################
class PgClient(object):
    """
    postgres db client
    make sure python-psycopg2 has been installed by apt-get.
    """
    #def __init__(self, db, user, passwd, host, port):
    def __init__(self, xmlfile):
        try:
            self.dbok = False
            config = ConfigParse(xmlfile)
            dbuser = config.getValue('config.pg.user')
            dbpasswd = config.getValue('config.pg.passwd')
            db = config.getValue('config.pg.db')
            dbhost = config.getValue('config.pg.host')
            dbport = config.getValue('config.pg.port')
            self.conn = psycopg2.connect(database=db, user=dbuser, password=dbpasswd, host=dbhost, port=dbport)
            self.cursor = self.conn.cursor()
            self.dbok = True
            logger.debugLog('connect pg succeed')
        except Exception,e:
            #traceback.print_exc()
            logger.errLog('PgClient init error, cause: ', e)

    def __del__(self):
        try:
            if self.dbok == False:
                raise AssertionError("PgClient connection not ready.")
            self.conn.close()
            logger.debugLog('close connection to pg')
        except Exception,e:
            logger.errLog('PgClient del error, cause: ', e)

    def exc(self, sql, isCommit=True):
        try:
            if self.dbok == False:
                raise AssertionError("PgClient connection not ready.")
            self.cursor.execute(sql)
            if isCommit:
                self.conn.commit()
            return True
        except Exception, e:
            logger.errLog("execute sql failed cause:", e, " sql:", sql)
            return False

    def cancelExe(self):
        """
        rollback since last commit()
        """
        try:
            if self.dbok == False:
                raise AssertionError("PgClient connection not ready.")
            self.conn.rollback()
            return True
        except Exception, e:
            logger.errLog("cancel execute sql failed cause:", e)
            return False

    def query(self, sql):
        try:
            if self.dbok == False:
                raise AssertionError("PgClient connection not ready.")
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            return rows
        except Exception, e:
            logger.errLog("query sql failed cause:", e, " sql:", sql)
            return []

