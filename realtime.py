#!/usr/bin/env python
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')  

import sys
import tushare as ts  

def getRealtime(whichList):
    ##Step 1. set the codes.
    codes = []
    if whichList == '1' or whichList == '0': #----持仓区
        codes.append("600016") #民生银行 <5.95, 650
        codes.append("000402") #金融街 <5.95, 650
        codes.append("002253") #川大智胜 15.45
        codes.append("002818") #富森美
        codes.append("601006") #大秦铁路 <8
        codes.append("600051") #宁波联合 <8, 735
        codes.append("000581") #威孚高科 <
        codes.append("600266") #北京城建 <8
    if whichList == '2' or whichList == '0': #----入手区
        codes.append("000423") #东阿阿胶 <40
        codes.append("601006") #大秦铁路 <8
        codes.append("000581") #威孚高科 <
        codes.append("002344") #海宁皮城 <4
        codes.append("600557") #康缘药业 <8
        codes.append("002763") #汇洁股份
        codes.append("601360") #360
        codes.append("300393") #中来股份
        codes.append("300467") #迅游科技
    if whichList == '3' or whichList == '0': #----观察区
        codes.append("002250") #联化科技
        codes.append("300004") #南风股份
        codes.append("300369") #绿盟科技
        codes.append("600433") #冠豪高新
        codes.append("300458") #全志科技
        codes.append("300273") #和佳股份
        codes.append("600598") #北大荒
        codes.append("002818") #富森美
    if whichList == '4' or whichList == '0': #-----破净观察区
        codes.append("000625") #长安汽车 <6.5
        codes.append("600266") #北京城建 <8
        codes.append("002344") #海宁皮城 <4.5
        codes.append("600016") #民生银行 <5.95
    if whichList == '5' or whichList == '0': #-----观察区A.
        codes.append("601006") #大秦铁路 <8
        codes.append("000581") #威孚高科 <
        codes.append("600674") #川投能源
        codes.append("600585") #海螺水泥
        codes.append("603858") #步长制药
        codes.append("600703") #三安光电
        codes.append("000423") #东阿阿胶 <40
        codes.append("600516") #方大炭素
        codes.append("002027") #分众传媒
    #codes.append("") #
    codes.append("399006") #创业板指

    ##Step 2. unique the codes.
    uniqueCodes = []
    for i in codes:
        if i not in uniqueCodes:
            uniqueCodes.append(i)

    ##Step 3. get the realtime quotes.
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
        print "%4s  %8s  %8s  %2s  %8s  %8s  %8s  %8s  %6s  %12s" % (row["name"], row["pre_close"], row["open"], isup, row["price"], diffValue, row["high"], row["low"], rateStr, row["volume"]) 
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
