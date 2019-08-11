# -*- coding: utf-8 -*-

#from datetime import date, time, datetime, timedelta
import MySQLdb
#import pymysql
from TradingSystemApp import TWStockFuntion as TWS
from collections import namedtuple
import requests
import json
import datetime
import time
from datetime import timedelta

from TradingSystemApp import Stock as stockObj, Account as account
from TradingSystemApp import GetAllDailyData



from TradingSystemApp.TradingStrategy import TurtleStrategy as turtleStrategyObj
def StartTrading(stockId,nDays):

    cashAcount=account.CashAccount('Carl',500000)
   
    stockCode=stockId
    # 往前計算n天
    n=int(nDays)

    #更新資料庫至今日的紀錄
    #GetAllDailyData.getDailyData('上市','0050')

    #進場，突破/跌破 n日最高價/低價，輸出stockCode
    #getMaxClosedPriceOf_nDay

    #測試用，可輸入指定日期當作today
    today= datetime.datetime.strptime('2019-01-16','%Y-%m-%d')
    #today=datetime.date.today()

    delta=datetime.timedelta(days = -n+1)
    pastDate=today+delta
    
    strDelta=str(pastDate)
    strToday=str(today)


    #取得最近交易日/今日的收盤價

    #初始化StockClass資料
    db = MySQLdb.connect(host="127.0.0.1",user="root",passwd="abcd951236",db="stock_db",charset="UTF8")
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()

    sqlStr="select chCode,dTDate,deBPrice,deHPrice, deLPrice, deEPrice,deDiff from dailydetail where dTDate between '"+strDelta+"' and '"+strToday +"' and chCode='"+str(stockCode)+"'"
    stockObjArray=[] 
    try:
        # 执行sql语句
        cursor.execute(sqlStr)
        # 执行sql语句
        results = cursor.fetchall()
        PDC=0  
        for row in results:
            stockId=str(row[0])
            #*日期先用str暫存
            d=str(row[1])
            bPrice=float(row[2])
            hPrice=float(row[3])
            lPrice=float(row[4])
            cPrice=float(row[5])
            diff=float(row[6])
            #第一筆的PDC (previous date closed)用diff漲跌幅回推前一日收盤價
            if PDC==0:
                PDC=cPrice-diff

            stockObjArray.append(stockObj.Stock(stockId,d,bPrice,hPrice,lPrice,cPrice,PDC))
            #更新PDC，將今日收盤價暫存給下一筆
            PDC=cPrice
            #print out for testing, datetime need to be converted to str
            #print(row[0]+"\n")
               
    except:
        print("Error: unable to fetch data into StockObj.")
    #目前試驗先用20日ATR計算
    ATRArray=turtleStrategyObj.getATR(stockObjArray,20)
    #列印 stock obj list 內容
    for obj in stockObjArray:
        print(str(obj.H)+"\t"+str(obj.L)+"\t"+str(obj.Closed)+"\t"+str(obj.PDC)+"\t"+str(obj.TR)+"\n")    

    #print ATR array
    #for atr in ATRArray:
    #    print(atr)
    #print("\n")
    #取得最近新的ATR
    latestATR=ATRArray[len(ATRArray)-1]

    #計算部位規模，回傳單位數
    StockQtyForEveryUnit=turtleStrategyObj.getInvestingShares(500000,latestATR,stockCode,strToday)

    #測試加碼與停損
    #計算加碼和停損價位，輸入進場價位和最新的ATR，輸出2個List (最多四次加碼)
    overWeightList=turtleStrategyObj.getOverWeightList(9.05,latestATR) 
    stopPriceList=turtleStrategyObj.getStopPriceList(overWeightList,latestATR)
    print("加碼價位")
    for p in overWeightList:
        print(str(p))

    print("停損價位")
    for p in stopPriceList:
        print(str(p))

    #決定獲利了結出場，做多/空=>價格跌破10或20日低點/穿越10或20日高點





    return StockQtyForEveryUnit,overWeightList,stopPriceList
       
