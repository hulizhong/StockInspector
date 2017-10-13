#!/usr/bin/env python
# coding=utf-8

import tushare as ts  

codes = ["300458", "300369", "300403", "603566", "002749", "399006"]
res = ts.get_realtime_quotes(codes)
print "   name, close,  open,  price,  high,  low,  volume"
for index, row in res.iterrows():
    print row["name"], row["pre_close"], row["open"], row["price"], row["high"], row["low"], row["volume"]
#print res
