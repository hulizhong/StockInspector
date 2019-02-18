#!/usr/bin/env python
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')  

import sys
import tushare as ts  

def getRealtime(whichList):
    # 300393 中来股份, 300467 迅游科技
    codes = ["601360", "002763", "002250", "002344", "300004", "300369", "300393", "600433", "300467", "399006"]
    if whichList == '0':
        pass
    elif whichList == '1':
        codes.append("300458")
        codes.append("300273")
        codes.append("600598")
        codes.append("002818")
    else:
        pass

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
        arg = "3"
    getRealtime(arg)
