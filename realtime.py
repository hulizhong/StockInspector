#!/usr/bin/env python
# coding=utf-8

import tushare as ts  

codes = ["300273", "300369", "002344", "399006"]
res = ts.get_realtime_quotes(codes)
print "   name, close,  open,  price,  high,  low,  volume"
for index, row in res.iterrows():
    print row["name"], row["pre_close"], row["open"], row["price"], row["high"], row["low"], row["volume"]
#print res
