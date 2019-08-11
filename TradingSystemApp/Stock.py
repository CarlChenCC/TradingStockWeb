#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scipy as sp
from TradingSystemApp import TWStockFuntion as TWS

import time
import datetime
import MySQLdb

#TR需取絕對值
def getTR(H,L,PDC):
    tmpArray=[]
    tmpArray.append(H-L)
    tmpArray.append(abs(H-PDC))
    tmpArray.append(abs(PDC-L))
    return max(tmpArray)


class Stock:
    def __init__(self,id,date,B,H,L,C,pdc):
        self.ID=id
        self.DATE=date
        self.Begin=B
        self.H=H
        self.L=L
        self.Closed=C
        self.PDC=pdc
        self.TR=getTR(H,L,pdc)

    


"""

url="http://www.tse.com.tw/exchangeReport/MI_INDEX?response=csv&date=20180223&type=ALLBUT0999"
data=urlRequest.urlretrieve(url,'MI_INDEX.csv')
f=open('MI_INDEX.csv','r')
for row in csv.reader(f):
    print(row)
f.close
"""


"""
testArray=[]
testArray.append(Stock(3,2,1))
testArray.append(Stock(6,5,4))
testArray.append(Stock(9,8,7))
print(getFirstATR(testArray))
"""


"""
studentArray=[]
studentArray.append(Student(11,'carl'))
studentArray.append(Student(22,'jack'))

for i in studentArray:
    print (i.id,i.name)

studentArray[0].setName('carlcc')
for i in studentArray:
    print(i.id,i.name)

my_list=[]
my_list.append(1)
my_list.append(22)
my_list.append(33)
my_list.append(444)
my_list.append(555)
numOfItme=len(my_list)
sumOfAll=sum(my_list)

print(my_list[1:3])
print(numOfItme)
print(sumOfAll)

sumInFunc=sumInterval(5,8)
print(sumInFunc)
"""
        