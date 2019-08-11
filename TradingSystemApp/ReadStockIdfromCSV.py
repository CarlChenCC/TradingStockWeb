import csv
#import pymysql
import MySQLdb
from datetime import datetime

def parse_ymd(s):
    # 傳入 eg."1997-08-01"字串, 而後回傳為 datetime格式(方便運算)
    #date_s=s.split(' ')
    year_s, mon_s, day_s = s.split('/')
    #hour_s,min_s=date_s[1].split(':')
    return datetime(int(year_s), int(mon_s), int(day_s))

with open('C:\\Users\\carl\\Desktop\\Book2.csv',mode='r',encoding='utf-8')as f:

    reader=csv.reader(f)
    next(reader)
    for row in reader:
        db = MySQLdb.connect(host="127.0.0.1",port=3306,user="root",passwd="abcd951236",db="stock_db",charset="UTF8")
        cursor = db.cursor()
        sql = "INSERT INTO stockid (chCode, dBDate, dtRecDate, chMarket, chCollect, stockname) VALUES ('{0}',{1},{2},'{3}','{4}','{5}')".format(row[0], row[1],row[2],row[3],row[4],row[5])
        try:
            # 执行sql语句
            cursor.execute(sql)
    
            # 执行sql语句
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()
        # 关闭数据库连接
        db.close()
    
