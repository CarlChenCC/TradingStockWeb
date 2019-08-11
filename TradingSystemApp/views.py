from django.shortcuts import render
from django.http import HttpResponse
import json
from TradingSystemApp import main

# Create your views here.
def pylinkweb(request):
    return HttpResponse("Django 讓python 能方便連結網頁")

def goToMainPage(request):
    return render(request,'Default.html',{})

def calTurtleResultMethod(request):
    stockId=str(request.GET['stockIdForTurtle'])
    calculatingDays=str(request.GET['calculatingDays'])
    latestATR1,latestATR2,latestATR3=main.StartTrading(stockId,calculatingDays)

    return HttpResponse(json.dumps({"a":latestATR1,"b":latestATR2,"c":latestATR3}))

def UpdatingStockDbMethod(request):
    stockId=str(request.GET['stockId'])
    market=str(request.GET['market'])
    IsStockDbUpdated=str(main.GetAllDailyData.getDailyData(market,stockId))
    return IsStockDbUpdated
