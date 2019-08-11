#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scipy as sp
from TradingSystemApp import TWStockFuntion as TWS
import time
import datetime
import MySQLdb

class TurtleStrategy:
    def __init__(self,strategy):
        self.strategy=strategy

#取真實區間TR的20天簡單平均當作第一個ATR (也就是PDN)
    def getFirstATR(arrayOfNdaysStock):    
        tmpList=[]
        for obj in arrayOfNdaysStock:
            tmpList.append(obj.TR)       
        lengthOfList=len(tmpList)
        return sp.average(tmpList[0:lengthOfList])
 #n 為計算ATR的期間 天數
    def getATR(stockObjArray,n):
        ATRarray=[]
        #取stockObjArray元素第0~第n-1 個
        FirstATR=TurtleStrategy.getFirstATR(stockObjArray[0:n])
        ATRarray.append(FirstATR)        

        #前面n-1個TR已被拿去計算firstATR，所以從n開始計算之後的ATR
        #20天期ATR

           
        i=0
        N=n
        if N>len(stockObjArray)-1:
            print("查詢的期間天數小於計算的天數n")
        #19和20未來可改變成可調整參數讓user調整
        while N<len(stockObjArray):            
            ATR=(19*ATRarray[i]+stockObjArray[N].TR)/20
            ATRarray.append(ATR)
            i=i+1
            N=N+1
        return ATRarray

#決定部位規模
    def getInvestingShares(InputMoney,ATR,stockCode,strToday):

        strToday=str(strToday)

        db = MySQLdb.connect(host="127.0.0.1",user="root",passwd="abcd951236",db="stock_db",charset="UTF8")
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()

        sqlStr="select deEPrice from dailydetail where dTDate='"+strToday +"' and chCode='"+str(stockCode)+"'"
        try:
            # 执行sql语句
            cursor.execute(sqlStr)
            # 执行sql语句

            closedPriceToday=cursor.fetchone()

            InvestingShares=InputMoney*0.01/(ATR*float(closedPriceToday[0]))               
            db.close() 
        except:
            print("Error: unable to fetch data")
    
        return InvestingShares

#加碼，單一市場/標的最多持有4單位
    def getOverWeightList(enterPrice,latestATR):
        OverWeightList=[]
        OverWeightList.append(enterPrice)
        OverWeightList.append(enterPrice+0.5*1*latestATR)
        OverWeightList.append(enterPrice+0.5*2*latestATR)
        OverWeightList.append(enterPrice+0.5*3*latestATR)
        return OverWeightList
#停損價位表
    def getStopPriceList(OverWeightList,latestATR):
        StopPriceList=[]        
        for p in OverWeightList:
            StopPriceList.append(p-0.5*latestATR)
        return StopPriceList

