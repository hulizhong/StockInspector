#!/usr/bin/env python
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')  

import sys
import tushare as ts  

def getRealtime(whichList):
    codes = []
    if whichList == '1' or whichList == '0':
        codes.append("601006") #大秦铁路 <8
        codes.append("002344") #海宁皮城 <4
        codes.append("002763") #汇洁股份
        codes.append("601360") #360
        codes.append("300393") #中来股份
        codes.append("300467") #迅游科技
    if whichList == '2' or whichList == '0':
        codes.append("002250") #联化科技
        codes.append("300004") #南风股份
        codes.append("300369") #绿盟科技
        codes.append("600433") #冠豪高新
        codes.append("300458") #全志科技
        codes.append("300273") #和佳股份
        codes.append("600598") #北大荒
        codes.append("002818") #富森美
    #codes.append("") #
    codes.append("399006") #创业板指

    res = ts.get_realtime_quotes(codes)
    print "   name,     close,     open,isUP,   price,     diff,     high,     low,        volume"
    for index, row in res.iterrows():
        diffValue = float(float(row["price"]) - float(row["open"]))
        if len(row["name"]) == 3:
            row["name"] = "--" + row["name"]
        if row["pre_close"] < row["open"]:
            isup = "Y"
        else:
            isup = "N"
        print "%4s  %8s  %8s  %2s  %8s  %8s  %8s  %8s  %12s" % (row["name"], row["pre_close"], row["open"], isup, row["price"], diffValue, row["high"], row["low"], row["volume"]) 
        #print row["name"], row["pre_close"], row["open"], isup, row["price"], row["high"], row["low"], row["volume"]
    #print res


if __name__ == '__main__':
    '''
    try:
        pro = ts.pro_api('de9b1451bddbd602befadae7d472354e3306e6b3b33561ec33404627')
        df = pro.repurchase(ts_code='300369', ann_date='20180101')
        print df
    except Exception as err:
        print err
    '''
    if len(sys.argv) == 2:
        arg = sys.argv[1]
    else:
        arg = "0"
    getRealtime(arg)
