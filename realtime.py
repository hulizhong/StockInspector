#!/usr/bin/env python
# coding=utf-8

import tushare as ts  

codes = ["002344", "300273", "002818", "300458", "300369", "300004", "300164", "300379", "399006"]
res = ts.get_realtime_quotes(codes)
print "   name,     close,     open,isUP,   price,    diff,     high,     low,        volume"
for index, row in res.iterrows():
    diffValue = float(row["price"]) - float(row["open"])
    if len(row["name"]) == 3:
        row["name"] = "nn" + row["name"]
    if row["pre_close"] < row["open"]:
        isup = "Y"
    else:
        isup = "N"
    print "%4s  %8s  %8s  %2s  %8s  %8s  %8s  %8s  %12s" % (row["name"], row["pre_close"], row["open"], isup, row["price"], diffValue, row["high"], row["low"], row["volume"]) 
    #print row["name"], row["pre_close"], row["open"], isup, row["price"], row["high"], row["low"], row["volume"]
#print res
