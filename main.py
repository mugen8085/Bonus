<<<<<<< HEAD
# import package
from datetime import datetime as dtime
from datetime import date,timedelta
from urllib.request import urlopen
import requests
from dateutil import rrule
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import numpy as np
import json
import time
import os
from io import StringIO
from Tools import *

DataPath = ''
DataStartDate = ''
DataStopDate = ''

#轉換日期民國到西元
def date_convert(strDate):
    arydate = strDate.split("/")
    return date(int(arydate[0]) + 1911, int(arydate[1]), int(arydate[2])).strftime('%Y/%m/%d')

def ConvertType_NewData(df):
    #轉換日期民國到西元.
    df['日期'] = [date_convert(x) for x in df['日期']]
    df['日期'] = pd.to_datetime(df['日期'].astype(str), format='%Y/%m/%d')
    #轉換型態.
    if df['成交筆數'].dtype != 'float64':
        df['成交筆數'] = df['成交筆數'].str.replace(',','').astype(float)
    if df['成交股數'].dtype != 'float64':
        df['成交股數'] = df['成交股數'].str.replace(',','').astype(float)
    if df['成交金額'].dtype != 'float64':
        df['成交金額'] = df['成交金額'].str.replace(',','').astype(float)

def ConvertType(df):
    #轉換日期民國到西元.
    df['日期'] = pd.to_datetime(df['日期'].astype(str), format='%Y/%m/%d')
    #轉換型態.
    if df['成交筆數'].dtype != 'float64':
        df['成交筆數'] = df['成交筆數'].str.replace(',','').astype(float)
    if df['成交股數'].dtype != 'float64':
        df['成交股數'] = df['成交股數'].str.replace(',','').astype(float)
    if df['成交金額'].dtype != 'float64':
        df['成交金額'] = df['成交金額'].str.replace(',','').astype(float)

def GetMonthStart(date):
    result = date - timedelta(days=date.day-1)
    return result

# 爬取每月股價的目標網站並包裝成函式
def craw_one_month(stock_number,date):
    url = (
        "http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date="+
        date.strftime('%Y%m%d')+
        "&stockNo="+
        str(stock_number)
    )
    data = json.loads(urlopen(url).read())
    # print(data)
    # print(data['stat'])
    json_string = json.dumps(data['stat'])
    # print(json_string)
    if "OK" in json_string:
        # print('Yes')
        return pd.DataFrame(data['data'], columns=data['fields'])
    else:
        return ''

# 根據使用者輸入的日期，以月為單位，重複呼叫爬取月股價的函式
def craw_stock(stock_number, start_month):
    b_month = date(*[int(x) for x in start_month.split('-')])
    now = dtime.now().strftime("%Y-%m-%d")  # 取得現在時間
    e_month = date(*[int(x) for x in now.split('-')])
    
    result = pd.DataFrame()
    for dt in rrule.rrule(rrule.MONTHLY, dtstart=b_month, until=e_month):
        print(dt)
        data = craw_one_month(stock_number, dt)
        if data is not '':
            result = pd.concat([result, data], ignore_index=True)
        time.sleep(10000.0 / 1000.0)

    return result

def CrawStock(old_dt, stock_number, start_month):
    global DataStartDate
    global DataStopDate

    now = dtime.now().strftime("%Y-%m-%d")  # 取得現在時間

    result = pd.DataFrame()

    fullpath = DataPath + Code + '.csv'
    #找到前面缺少的
    OldStartDay = date.today().strftime("%Y-%m-%d")
    OldStopDay = date.today().strftime("%Y-%m-%d")
    if old_dt.empty is True:
        old_dt = pd.DataFrame()
        print("No old data.")
    else:
        OldStartDay = old_dt.loc[:,'日期'].min().strftime("%Y-%m-%d")
        OldStopDay = old_dt.loc[:,'日期'].max().strftime("%Y-%m-%d")

    # if date(*[int(x) for x in OldStartDay.split('-')]) == DataStartDate:
    #     return
    # if date(*[int(x) for x in OldStopDay.split('-')]) == DataStopDate:
    #     return

    print("Old start day:", OldStartDay)
    print("Old stop day: ", OldStopDay)

    #起始日
    b_month = date(*[int(x) for x in start_month.split('-')])
    #結束日
    e_month = date(*[int(x) for x in now.split('-')])

    if start_month < OldStartDay and DataStartDate < date(*[int(x) for x in OldStartDay.split('-')]):
        print("Get data before ",OldStartDay)
        BeginMonth = b_month
        EndMonth = date(*[int(x) for x in OldStartDay.split('-')])

        dts = rrule.rrule(rrule.MONTHLY, dtstart=BeginMonth, until=EndMonth)

        list = []
        for dt in dts:
            list.append(dt)

        for i in range(len(list)):
            dt = list[len(list)-i-1]
            print(dt)
            data = craw_one_month(stock_number, dt)
            if data is not '':
                ConvertType_NewData(data)
                old_dt = pd.concat([old_dt, data.loc[data['日期'] < OldStartDay]], ignore_index=True)

                old_dt = old_dt.sort_values(by=['日期'])

                old_dt.to_csv(fullpath, encoding='utf_8_sig')
                time.sleep(10000.0 / 1000.0)

    BeginMonth = GetMonthStart(date(*[int(x) for x in OldStopDay.split('-')]))
    LastDay = date(*[int(x) for x in OldStopDay.split('-')])

    if date(*[int(x) for x in OldStopDay.split('-')]) == DataStopDate:
        return

    for dt in rrule.rrule(rrule.MONTHLY, dtstart=BeginMonth, until=e_month):
        print(dt)
        data = craw_one_month(stock_number, dt)
        if data is not '':
            ConvertType_NewData(data)
            old_dt = pd.concat([old_dt, data.loc[data['日期'] > OldStopDay]], ignore_index=True)
            old_dt = old_dt.sort_values(by=['日期'])
            old_dt.to_csv(fullpath, encoding='utf_8_sig')
            time.sleep(10000.0 / 1000.0)

if __name__ == '__main__':
    # 讀取INI檔案
    InitFile = IniTool()
    global Datapath
    # global DataStartDate
    # global DataStopDate

    DataPath = InitFile.Read('Infomation', 'DataPath')
    DataStartDate = InitFile.Read('Infomation', 'DataStartDate')
    DataStopDate = InitFile.Read('Infomation', 'DataStopDate')
    Date = InitFile.Read('Infomation', 'StartDate')

    print(Date)
    print(DataPath)

    DataStartDate = date(*[int(x) for x in DataStartDate.split('-')])
    DataStopDate = date(*[int(x) for x in DataStopDate.split('-')])

    #取得股票清單
    df_StockList = pd.read_csv('StockList.csv', index_col = 0)
    # print(df_StockList)

    # Code = '3034'
    # fullpath = DataPath + Code + '.csv'
    # df_History = pd.read_csv(fullpath, index_col=0)
    # ConvertType(df_History)
    # CrawStock(df_History, Code, Date)

    for index, row in df_StockList.iterrows():
        print(row['代號'])
        Code = row['代號']
        fullpath = DataPath + Code + '.csv'
        # 確認是否有舊資料
        NoHistory = False
        if os.path.isfile(fullpath):
            # 檔案存在的處理
            print("檔案存在。")
        else:
            # 檔案不存在的處理
            print("檔案不存在。")
            NoHistory = True

        df_History = pd.DataFrame()
        if NoHistory is False:
            df_History = pd.read_csv(fullpath, index_col=0)
            # 轉換日期格式.
            ConvertType(df_History)
        CrawStock(df_History, Code, Date)



        # if NoHistory is True:
        #     print(Code)
        #     df_History = craw_stock(Code, Date)
        #     ConvertType_NewData(df_History)
        #     df_History.to_csv(fullpath, encoding='utf_8_sig')
        # else:
        #     df_History = pd.read_csv(fullpath, index_col = 0)
        #     # 轉換日期格式.
        #     df_History['日期'] = pd.to_datetime(df_History['日期'].astype(str), format='%Y/%m/%d')
        #     # 取得今天日期
        #     today = date.today()


    # code = 2303
    # df = craw_stock(code,"2020-01-01")
    # filename = str(code) + '.csv'
    # df.to_csv(filename, encoding='utf_8_sig')

    # Update connection string information
    # host = "127.0.0.1"
    # dbname = "Stock001"
    # user = "postgres"
    # password = "roger0"
    # sslmode = "require"
    #
    # conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
    # conn = psycopg2.connect(conn_string)

    # conn = psycopg2.connect(database="Stock001", user="postgres", password="roger0", host="127.0.0.1", port="5432")
    # print("Connect DB success.")
    # cur = conn.cursor()
    #
    # cur.execute("DROP TABLE IF EXISTS COMPANY;")
    # print("Finished dropping table (if existed)")
    #
    # cur.execute('''CREATE TABLE COMPANY
    #            (ID INT PRIMARY KEY     NOT NULL,
    #            NAME           TEXT    NOT NULL,
    #            AGE            INT     NOT NULL,
    #            ADDRESS        CHAR(50),
    #            SALARY         REAL);''')
    # print("Create table success.")
    #
    # conn.commit()
    # cur.close()
    # conn.close()
=======
if __name__ == '__main__':
  print('Hi')
>>>>>>> a8f4dd5d00f6b659c3dfb63d6bb096810c9effa7
