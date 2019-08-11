# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 22:08:35 2017

@author: dufah
"""

import sys
from TradingSystemApp import TWStockFuntion as TWSF
from datetime import datetime

from collections import namedtuple



def getDailyData(market,stockId):
    
#   if len(sys.argv) >= 2:
#        if sys.argv[1] == "/?":
#            print("使用方式:")
#            print("         GetAllDailyData                 【不帶任何參數，執行所有的上市櫃公司資料抓取!】")
#            print("         GetAllDailyData  上市/上櫃/all  【第一個參數，執行所有上市/上櫃(二選一)公司資料抓取!】" )
#            print("         GetAllDailyData  上市/上櫃/all   股票代號【第二個參數，配合參數一，可為1個數字以上!】" )
#            sys.exit(1)
#    #intValue = int(sys.argv[1])#如果要將變數搞成數字的話可以使用 int()來轉
#    #print(sys.argv[1])
 
#if __name__ == "__main__":
#    main()

    ThisTime = datetime.today() #這是系統啟動時的固定值, 一次執行所有程式時, 此一紀錄值均相同

    if market=="" and stockId=="":
        HaveError, MyResult = TWSF.GetCode(ThisTime)
    if market!="" and stockId=="":
        if str.upper(market) == "ALL":
            HaveError, MyResult = TWSF.GetCode(ThisTime)
        else:
            HaveError, MyResult = TWSF.GetCode(ThisTime, market)
    if market!="" and stockId!="":
        if str.upper(market) == "ALL":
            HaveError, MyResult = TWSF.GetCode(ThisTime, "%",stockId)
        else:
            HaveError, MyResult = TWSF.GetCode(ThisTime, market, stockId)

    if HaveError == "Y":
        print("上市資料無法取得，程式結束!")
        sys.exit()

    MyCount = 0
    #以下4行可以指定只抓取某stockId 和抓取期間，for... in MyResult需改成MyResult1
    #settingDate=datetime.strptime('2018-01-01','%Y-%m-%d')
    #rrow=('3630',settingDate,settingDate,'上櫃')
    #MyResult1=[]
    #MyResult1.append(rrow)

    for chCode, dBDate, dtRecDate, chMarket in MyResult:
        #print('1 : ', type(dBDate.strftime('%Y%m01')),dBDate.strftime('%Y%m01'))
        if dBDate.strftime('%Y%m01') <= '20070101':  #因為上市資料自81年04月開始
            dBDate = TWSF.parse_ymd('2007-01-01')   #改抓2007/1/1日後，因為後面會+1個月
        if dtRecDate is not None:  #若已經有抓資料了，應該自該日期後再抓
            dBDate = dtRecDate
            dtRecDateExistMonth = True
        else:
            dtRecDateExistMonth = False
    
        #print('2 : ', type(dBDate.strftime('%Y%m01')), type(ThisTime.strftime('%Y%m%d')))
    
        while dBDate.strftime('%Y%m01') <= ThisTime.strftime('%Y%m%d'):   #抓到現在
        
            print(chMarket, 'StockID:',chCode,dBDate, 'Use dBDate : ', dBDate.strftime('%Y%m01'))
        
            if chMarket == '上市':    
                A = TWSF.TWSE_Daily(ThisTime, dBDate.strftime('%Y%m01'), chCode)
                if A['stat'] == 'OK':
                    for mydata in (A['data']):
                        dTDate, deStockNum, deTAmount, deBPrice, deHPrice, deLPrice, deEPrice, deDiff, chDiffRemark, deCount = TWSF.TransDailyData(chMarket, mydata)
                        #print(type(dTDate), dTDate, type(dBDate), dBDate)
                        if dtRecDateExistMonth is True:
                            if dTDate.replace("/","") >= format(dBDate.strftime('%Y%m%d')):
                                if dTDate.replace("/","") == format(dtRecDate.strftime('%Y%m%d')):
                                    print('dBDate:',dBDate, 'dTDate', dtRecDate, '(當月)已經存在，不寫入(=dtRecDate)')
                                else:
                                    #print('dBDate:',dBDate, 'dTDate', dTDate, '(當月)不存在，寫入')
                                    TWSF.WriteDailyDetail(ThisTime, chCode, dTDate, deStockNum, deTAmount, deBPrice, deHPrice, deLPrice, deEPrice, deDiff, chDiffRemark, deCount)
                        else:
                            #print('dBDate:',dBDate, 'dTDate', dTDate, '(非當月)寫入')
                            TWSF.WriteDailyDetail(ThisTime, chCode, dTDate, deStockNum, deTAmount, deBPrice, deHPrice, deLPrice, deEPrice, deDiff, chDiffRemark, deCount)
                else:
                    #print("Stock ID : " + chCode + "   "+ dBDate.strftime('%Y%m01') + "無資料!!!")
                    TWSF.WriteLog(ThisTime, "GetCode", "錯誤", "TWStockFunction.py中，利用TWSE_Daily在讀取網頁資料時發生【無資料", (dBDate.strftime('%Y%m01') + "無資料!!!"))

            if chMarket == '上櫃':    
                #print(chMarket, dBDate.year, dBDate.month, dBDate.year - 1911)
                #print(chMarket, 'StockID:',chCode,dBDate, 'Use dBDate : ', dBDate.strftime('%Y%m01'))
                A = TWSF.OTC_Daily(ThisTime, str(dBDate.year - 1911),str(dBDate.month), chCode)
                for mydata in (A['aaData']):
                    dTDate, deStockNum, deTAmount, deBPrice, deHPrice, deLPrice, deEPrice, deDiff, chDiffRemark, deCount = TWSF.TransDailyData(chMarket, mydata)
                    #print(type(dTDate), dTDate, type(dBDate), dBDate)
                    if dtRecDateExistMonth is True:
                        if dTDate.replace("/","") >= format(dBDate.strftime('%Y%m%d')):
                            if dTDate.replace("/","") == format(dtRecDate.strftime('%Y%m%d')):
                                print('dBDate:',dBDate, 'dTDate', dtRecDate, '(當月)已經存在，不寫入(=dtRecDate)')
                            else:
                                #print('dBDate:',dBDate, 'dTDate', dTDate, '(當月)不存在，寫入')
                                TWSF.WriteDailyDetail(ThisTime, chCode, dTDate, deStockNum, deTAmount, deBPrice, deHPrice, deLPrice, deEPrice, deDiff, chDiffRemark, deCount)
                    else:
                        #print('dBDate:',dBDate, 'dTDate', dTDate, '(非當月)寫入')
                        TWSF.WriteDailyDetail(ThisTime, chCode, dTDate, deStockNum, deTAmount, deBPrice, deHPrice, deLPrice, deEPrice, deDiff, chDiffRemark, deCount)


            TWSF.Wait_A_While()
        
            if dBDate.month == 12:
                dBDate = dBDate.replace(month= 1, year = dBDate.year + 1)    
            else:
                dBDate = dBDate.replace(day = 1, month=dBDate.month + 1) 
            
            dtRecDateExistMonth = False #已經不是有資料那個月了
        return 0
        
        
            
