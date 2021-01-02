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


# 爬取每月股價的目標網站並包裝成函式
def craw_one_month(stock_number,date):
    url = (
        "http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date="+
        date.strftime('%Y%m%d')+
        "&stockNo="+
        str(stock_number)
    )
    data = json.loads(urlopen(url).read())
    print(data)
    print(data['stat'])
    json_string = json.dumps(data['stat'])
    print(json_string)
    if "OK" in json_string:
        print('Yes')
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
        time.sleep(10000.0 / 1000.0);

    return result

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

if __name__ == '__main__':
    # 讀取INI檔案
    InitFile = IniTool()

    DataPath = InitFile.Read('Infomation', 'DataPath')
    Date = InitFile.Read('Infomation', 'StartDate')
    print(Date)
    print(DataPath)


    #取得股票清單
    df_StockList = pd.read_csv('StockList.csv', index_col = 0)
    # print(df_StockList)

    for index, row in df_StockList.iterrows():
        print(row['代號'])
        Code = row['代號']
        fullpath = DataPath + Code + '.csv'
        # 確認是否有舊資料
        if os.path.isfile(fullpath):
            # 檔案存在的處理
            print("檔案存在。")
        else:
            # 檔案不存在的處理
            print("檔案不存在。")
            NoHistory = True

        df_History = pd.DataFrame()
        if NoHistory is True:
            print(Code)
            df_History = craw_stock(Code, Date)
            ConvertType_NewData(df_History)
            df_History.to_csv(fullpath, encoding='utf_8_sig')
        else:
            df_History = pd.read_csv(fullpath, index_col = 0)
            # 轉換日期格式.
            df_History['日期'] = pd.to_datetime(df_History['日期'].astype(str), format='%Y/%m/%d')
            # 取得今天日期
            today = date.today()


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