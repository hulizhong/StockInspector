#!/usr/bin/env python
# coding=utf-8
import sys
import tushare as ts
from CodeList import DataItem, StockRepository
from CodeList import insertWatchCode, insertPbLess1Code, insertTraceCode, insertHandingCode

reload(sys)
sys.setdefaultencoding('utf8')  

def getRealtime(whichList):
    ## Step 1. set the codes.
    codes = []
    if whichList == '1' or whichList == '0' or whichList == '11': #----持仓区
        volDic = {} #volume.
        insertHandingCode(volDic, codes, whichList)
    if whichList == '2' or whichList == '0': #----入手区，跟踪区
        priDic = {} #price
        insertTraceCode(priDic, codes)
    if whichList == '3' or whichList == '0': #-----破净观察区
        insertPbLess1Code(codes)
    if whichList == '4' or whichList == '0': #----观察区
        insertWatchCode(codes)
    codes.append("399006") #创业板指

    ## Step 2. unique the codes.
    uniqueCodes = []
    for i in codes:
        if i not in uniqueCodes:
            uniqueCodes.append(i)

    ## Step 3. get the realtime quotes.
    res = ts.get_realtime_quotes(uniqueCodes)
    print "   name,     close,     open,isUP,   price,     diff,     high,     low,    rate,       volume"
    todayPL = 0.0  # today's profit and loss.
    for index, row in res.iterrows():
        #diffValue = float(float(row["price"]) - float(row["open"]))
        diffValue = float(float(row["price"]) - float(row["pre_close"]))
        rate = (diffValue*100)/float(row["pre_close"])
        rateStr = '%.2f' % (rate)
        if len(row["name"]) == 3:
            row["name"] = "--" + row["name"]
        if row["pre_close"] < row["open"]:
            isup = "Y"
        else:
            isup = "N"

        if whichList == '1': 
            if volDic.has_key(row["code"]):
                itemPL = diffValue * int(volDic[row["code"]]) #volume.
                todayPL += itemPL;
                print "%4s  %8s  %8s  %2s  %8s  %8s  %8s  %8s  %6s  %12s  %6s" % (row["name"], row["pre_close"], row["open"], isup, row["price"], diffValue, row["high"], row["low"], rateStr, row["volume"], itemPL) 
            else:
                print "%4s  %8s  %8s  %2s  %8s  %8s  %8s  %8s  %6s  %12s" % (row["name"], row["pre_close"], row["open"], isup, row["price"], diffValue, row["high"], row["low"], rateStr, row["volume"]) 
        else:
            print "%4s  %8s  %8s  %2s  %8s  %8s  %8s  %8s  %6s  %12s" % (row["name"], row["pre_close"], row["open"], isup, row["price"], diffValue, row["high"], row["low"], rateStr, row["volume"]) 
    if whichList == '1':
        print "----------- today's profit.", todayPL
    #print res

def autoTrace():
    '''
    '''
    ## Step 1, set the codes.
    dic = {}
    codes = []
    insertTraceCode(dic, codes)

    ##Step 2. unique the codes.
    uniqueCodes = []
    for i in codes:
        if i not in uniqueCodes:
            uniqueCodes.append(i)

    ## Step 3. get the realtime quotes.
    res = ts.get_realtime_quotes(uniqueCodes)
    print "   name,     close,     open,isUP,   price,     diff,     high,     low,    rate,       volume"
    for index, row in res.iterrows():
        #diffValue = float(float(row["price"]) - float(row["open"]))
        diffValue = float(float(row["price"]) - float(row["pre_close"]))
        rate = (diffValue*100)/float(row["pre_close"])
        rateStr = '%.2f' % (rate)
        if len(row["name"]) == 3:
            row["name"] = "--" + row["name"]
        if row["pre_close"] < row["open"]:
            isup = "Y"
        else:
            isup = "N"
        if float(row["price"]) < float(dic[row["code"]]):
            print "%4s  %8s  %8s  %2s  %8s  %8s  %8s  %8s  %6s  %12s" % (row["name"], row["pre_close"], row["open"], isup, row["price"], diffValue, row["high"], row["low"], rateStr, row["volume"]) 


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

    if arg.isdigit():
        getRealtime(arg)
    else:
        autoTrace()

'''
ts's API refer.
  res = ts.get_realtime_quotes(uniqueCodes)
  for index, row in res.iterrows():
        name                 海宁皮城
        open                4.520
        pre_close           4.510
        price               4.610
        high                4.670
        low                 4.520
        bid                 4.600
        ask                 4.610
        volume            9921310
        amount       45523595.200
        b1_v                   52
        b1_p                4.600
        b2_v                  308
        b2_p                4.590
        b3_v                 2110
        b3_p                4.580
        b4_v                 1026
        b4_p                4.570
        b5_v                  949
        b5_p                4.560
        a1_v                  187
        a1_p                4.610
        a2_v                  692
        a2_p                4.620
        a3_v                  766
        a3_p                4.630
        a4_v                  483
        a4_p                4.640
        a5_v                  835
        a5_p                4.650
        date           2019-07-15
        time             15:00:03
        code               002344
'''
