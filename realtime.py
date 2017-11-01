#!/usr/bin/env python
# coding=utf-8

import tushare as ts  

codes = ["300369", "002344", "300273", "300458", "300004", "300379", "399006"]
res = ts.get_realtime_quotes(codes)
print "   name,     close,     open,isUP,   price,     high,     low,        volume"
for index, row in res.iterrows():
    if row["pre_close"] < row["open"]:
        isup = "Y"
    else:
        isup = "N"
    print "%4s  %8s  %8s  %2s  %8s  %8s  %8s  %12s" % (row["name"], row["pre_close"], row["open"], isup, row["price"], row["high"], row["low"], row["volume"]) 
    #print row["name"], row["pre_close"], row["open"], isup, row["price"], row["high"], row["low"], row["volume"]
#print res
