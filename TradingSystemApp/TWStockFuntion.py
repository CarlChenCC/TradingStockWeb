# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 11:18:06 2017

@author: dufah
"""
#from datetime import date, time, datetime, timedelta
import MySQLdb
#import pymysql
from collections import namedtuple
import requests
import json
from datetime import datetime
import time
from datetime import timedelta
import random

from fake_useragent import UserAgent
import re

def Random_Headers():
    ua = UserAgent()
    return {'User-Agent': ua.random}

def Wait_A_While():
    random.seed()
    WaitTime = random.randint(5,9)
    time.sleep(WaitTime)

###############################################################################
def GetCode(ThisTime, WhichMarket = "%", WhichStockID = "%"): 
    #允許選擇 上市櫃/指定某個股票代號(可以Like)
    if WhichStockID != "%":
        WhichStockID = WhichStockID + "%" 
    HaveAnyError = "N"
    Result = []
    ROW = namedtuple("ROW", ['chCode', 'dBDate', 'dtRecDate', 'chMarket']) 
# 打开数据库连接
    #db = pymysql.connect("localhost","root","diadem","twstock",charset="UTF8")
    db=MySQLdb.connect(host="127.0.0.1",user="root",passwd="abcd951236",db="stock_db",charset="UTF8")
    #db = pymysql.connect(host="127.0.0.1",port=3306,user="root",passwd="abcd951236",db="stock_db",charset="UTF8")
     
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
     
    # SQL 查询语句
    #sql="SELECT * FROM stockid"
    sql = "SELECT chCode, dBDate, dtRecDate, chMarket FROM stockid WHERE chMarket like '{0}' and chCode like '{1}' and chCollect = 'Y' and (dtRecDate < '{2}' or dtRecDate is null)".format(WhichMarket, WhichStockID, ThisTime.strftime('%Y%m%d'))
            
    try:
       # 执行SQL语句
       cursor.execute(sql)
       # 获取所有记录列表
       results = cursor.fetchall()
       for row in results:
           chCode = row[0]
           dBDate = row[1]
           dtRecDate = row[2]
           chMarket = row[3]
           Result.append(ROW(chCode, dBDate, dtRecDate, chMarket))
    except:
          WriteLog(ThisTime, "GetCode", "錯誤", "在讀取【"+WhichMarket+"】時發生錯誤",sql)
          HaveAnyError = "Y"
     
    db.close()
    
    return (HaveAnyError, Result)

###############################################################################
def TWSE_Daily(ThisTime, YyyyMmDd, StockID):
    # WhichMonth輸入yyyymmdd(其中dd為每月的第一天即可), StockID輸入股票代號
    url_twse = "http://www.tse.com.tw/exchangeReport/STOCK_DAY?response=json&date="+YyyyMmDd+"&stockNo="+StockID
    
    try:
    # 觀察到該網頁適用Get形式取得, 所以寫為
        #res = requests.get(url_twse)
        time.sleep(5)
        res = requests.get(url_twse, headers=Random_Headers())
        #print(res.text)
        stockData = json.loads(res.text)
    except:
        WriteLog(ThisTime, "TWSE_Daily", "錯誤", "無法讀取資料") 
        #print("TWSE_Daily",YyyyMmDd,StockID,"無法抓取,發生錯誤")
        
    return stockData 

###############################################################################
def OTC_Daily(ThisTime, TwYear,TwMonth, StockID):
    # WhichMonth輸入yyyymmdd(其中dd為每月的第一天即可), StockID輸入股票代號
    url_twse = "http://www.tpex.org.tw/web/stock/aftertrading/daily_trading_info/st43_result.php?l=zh-tw&d="+TwYear+"/"+TwMonth+"&stkno="+StockID
    
    try:
    # 觀察到該網頁適用Get形式取得, 所以寫為
        #res = requests.get(url_twse)
        time.sleep(5)
        res = requests.get(url_twse, headers=Random_Headers())
        #print(res.text)
        stockData = json.loads(res.text)
    except:
        WriteLog(ThisTime, "OTC_Daily", "錯誤", "無法讀取資料")  
        #print("OTC_Daily",TwYear+"/"+TwMonth,StockID,"無法抓取,發生錯誤")
        
    return stockData 

###############################################################################   
def WriteDailyDetail(ThisTime, StockID, dTDate, deStockNum, deTAmount, deBPrice, deHPrice, deLPrice, deEPrice, deDiff, chDiffRemark, deCount):
    # 打开数据库连接, 【特別注意】沒有寫charset="UTF8" --> 遇到中文寫不進去
    #db = pymysql.connect("localhost","root","diadem","twstock",charset="UTF8") 
    #db = pymysql.connect(host="hl2170.myds.me",port=3307,user="dolphin",passwd="Sea2170HL",db="twstock",charset="UTF8")
    db = MySQLdb.connect(host="127.0.0.1",user="root",passwd="abcd951236",db="stock_db",charset="UTF8")
    cursor = db.cursor()
     
#    sql = "INSERT INTO dailydetail(chCode, dTDate, deStockNum, deTAmount, deBPrice, deHPrice, deLPrice, deEPrice, deDiff, deCount) \
#            VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}')".format(StockID, dTDate, \
#            deStockNum, deTAmount, deBPrice, deHPrice, deLPrice, deEPrice, deDiff, deCount)
    sql = "INSERT INTO dailydetail(chCode, dTDate, deStockNum, deTAmount, deBPrice, deHPrice, deLPrice, deEPrice, deDiff, chDiffRemark, deCount) VALUES ('{0}','{1}','{2}','{3}',{4},{5},{6},{7},{8},'{9}',{10})".format(StockID, dTDate,deStockNum, deTAmount, deBPrice, deHPrice, deLPrice, deEPrice, deDiff, chDiffRemark, deCount)
    sql2 = "update stockid set dtRecDate = '{0}' where chCode = '{1}'".format(dTDate, StockID)
            
    try:
       # 执行sql语句
       cursor.execute(sql)
       cursor.execute(sql2)
       # 执行sql语句
       db.commit()
    except:
       # 发生错误时回滚
       db.rollback()
       WriteLog(ThisTime, "WriteDailyDetail", "錯誤", StockID+"，"+ str(dTDate) +"，無法寫入資料庫",sql)     
    # 关闭数据库连接
    db.close()
        
###############################################################################
def WriteLog(dRunTime, chFunctionName, chType, vcRemark, YourSQL='None'):
    #YourSQL 可以允許部傳遞該參數，此時系統會帶入'None'
    #today = date.today()  #date只有日期, 需要得到時間則要用datetime.today()

     
    # 打开数据库连接, 【特別注意】沒有寫charset="UTF8" --> 遇到中文寫不進去
    #db = pymysql.connect("localhost","root","diadem","twstock",charset="UTF8")
    #db = pymysql.connect(host="127.0.0.1",port=3306,user="root",passwd="abcd951236",db="stock_db",charset="UTF8")
    db = MySQLdb.connect(host="127.0.0.1",user="root",passwd="abcd951236",db="stock_db",charset="UTF8")
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
     
    # SQL 插入语句
    
    #sql = "INSERT INTO aplog(dRunTime, dErrorTime, chFunctionName, chType, vcRemark) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')".format(ThisTime,datetime.today(),"MyFunction","正確??","別再寫TEST...")
    #sql = "INSERT INTO aplog(dRunTime, dErrorTime, chFunctionName, chType, vcRemark) VALUES ('{0!s}', '{1!s}', '{2!s}', '{3!s}', '{4!s}')".format(ThisTime,datetime.today(),"MyFunctionTT","正確??","別再寫TEST...")
    sql = "INSERT INTO aplog(dRunTime, dErrorTime, chFunctionName, chType, vcRemark, vcErrorScript) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(dRunTime, datetime.today(),chFunctionName, chType,vcRemark,YourSQL.replace("'","*"))

    try:
       # 执行sql语句
       cursor.execute(sql)
       # 执行sql语句
       db.commit()
    except:
       # 发生错误时回滚
       db.rollback()
       print("★★★ 重要訊息：WriteLog本身出現錯誤, 無法記錄錯誤, 必須人工檢視 ★★★")
     
    # 关闭数据库连接
    db.close()
###############################################################################    
def CtoW(CDate):
    # 傳入【民國年 106/07/01】 轉為 【西元年 2017/07/01】
    # 在OTC資料其實為 【106\/07\/03】，為了解決可能隱含其他雜訊問題，
    # 所以用正則表示法取出純數字部分，再來處理
    YourDate = "".join(re.findall(r"\d+",CDate))
    if len(YourDate) == 6:
        YourDate = "0" + YourDate
    #print('YourDate is : ', YourDate)
    return str(int(YourDate[0:3])+1911)+'/'+ YourDate[3:5]+ '/'+YourDate[5:]

###############################################################################
def TransDailyData(chMarket, InList):
    # 傳入【OTC/TWSE的日交量(每次取得一個月的資料】 轉為 【可以寫入 DailyDetail 的格式】
    dTDate = CtoW(InList[0]) #交易日期 (原來格式為 eg.106/07/05, 透過民國轉西元 2017/07/05
    #deStockNum = "".join(InList[1]) #將list內容轉為字串
    #以下正則表示式參考 資料夾 [Python語法 ==>正則表示式==>20171112_0919_只額取....]
    deStockNum = "".join(re.findall(r"[+]?[-]?\d+\.?\d*",InList[1].replace(",","")))
    if deStockNum == "" : deStockNum = "NULL"
    deTAmount = "".join(re.findall(r"[+]?[-]?\d+\.?\d*",InList[2].replace(",","")))
    if deTAmount == "" : deTAmount = "NULL"
    deBPrice = "".join(re.findall(r"[+]?[-]?\d+\.?\d*",InList[3].replace(",","")))
    if deBPrice == "" : deBPrice = "NULL"
    deHPrice = "".join(re.findall(r"[+]?[-]?\d+\.?\d*",InList[4].replace(",","")))
    if deHPrice == "" : deHPrice = "NULL"
    deLPrice = "".join(re.findall(r"[+]?[-]?\d+\.?\d*",InList[5].replace(",","")))
    if deLPrice == "" : deLPrice = "NULL"
    deEPrice = "".join(re.findall(r"[+]?[-]?\d+\.?\d*",InList[6].replace(",","")))
    if deEPrice == "" : deEPrice = "NULL"
    deDiff = "".join(re.findall(r"[+]?[-]?\d+\.?\d*",InList[7].replace(",","")))
    if deDiff == "" : deDiff = "NULL"
    deCount = "".join(re.findall(r"[+]?[-]?\d+\.?\d*",InList[8].replace(",","")))
    if deCount == "" : deCount = "NULL"
    chDiffRemark = "".join(re.findall(r"[+]?[-]?[^0-9.A-Za-z,]?",InList[7]))
    if chDiffRemark == "" : chDiffRemark = ""
    if chDiffRemark == "--" : chDiffRemark = ""
    #-----------------------------------------------
    # 以下針對 chMarket不同而進行特殊調整
    # 2017/11/14 OTC的資料沒有[不比價X]，所以當cHDiffMark空白時要做調整
    if chMarket == "上櫃" and deDiff == "0":
        chDiffRemark = ""
    if chMarket == "上櫃" and float(deDiff) > 0:        
        chDiffRemark = "+"
    #----------------------------------------------- 
    
    return (dTDate, deStockNum, deTAmount, deBPrice, deHPrice, deLPrice, deEPrice, deDiff, chDiffRemark, deCount)

###############################################################################
def parse_ymd(s):
    # 傳入 eg."1997-08-01"字串, 而後回傳為 datetime格式(方便運算)
    year_s, mon_s, day_s = s.split('-')
    return datetime(int(year_s), int(mon_s), int(day_s))
#取得n日中最大的收盤價，從今天往回n-1日
def getMaxClosedPriceOf_nDay(n,stockCode):
    today=datetime.date.today()
    delta=datetime.timedelta(days = -n+1)
    pastDate=today+delta
    
    strDelta=str(pastDate)
    strToday=str(today)

    db = MySQLdb.connect(host="127.0.0.1",user="root",passwd="abcd951236",db="stock_db",charset="UTF8")
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()

    sqlStr="select deEPrice from dailydetail where dTDate between '"+strDelta+"' and '"+strToday +"' and chCode='"+str(stockCode)+"'"
    try:
        # 执行sql语句
        cursor.execute(sqlStr)
        # 执行sql语句
        results = cursor.fetchall()
        tmparary=[]   
        for row in results:
            #print out for testing, datetime need to be converted to str
        #    print(row[0]+"\n")
            tmparary.append(row[0])
       
        db.close() 
    except:
        print("Error: unable to fetch data")
       
    return max(tmparary)

#取得n日中最小的收盤價，從今天往回n-1日
def getMinClosedPriceOf_nDay(n,stockCode):
    today=datetime.date.today()
    delta=datetime.timedelta(days = -n+1)
    pastDate=today+delta
    
    strDelta=str(pastDate)
    strToday=str(today)

    db = MySQLdb.connect(host="127.0.0.1",user="root",passwd="abcd951236",db="stock_db",charset="UTF8")
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()

    sqlStr="select deEPrice from dailydetail where dTDate between '"+strDelta+"' and '"+strToday +"' and chCode='"+str(stockCode)+"'"
    try:
        # 执行sql语句
        cursor.execute(sqlStr)
        # 执行sql语句
        results = cursor.fetchall()
        tmparary=[]   
        for row in results:
            #print out for testing, datetime need to be converted to str
        #    print(row[0]+"\n")
            tmparary.append(row[0])
       
        db.close() 
    except:
        print("Error: unable to fetch data")
       
    return min(tmparary)
