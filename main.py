
# import package
from datetime import datetime as dtime
from datetime import date,timedelta
from urllib.request import urlopen
from dateutil import rrule
import matplotlib.pyplot as plt
import datetime
import pandas as pd
import numpy as np
import json
import time
import psycopg2

# 爬取每月股價的目標網站並包裝成函式
def craw_one_month(stock_number,date):
    url = (
        "http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date="+
        date.strftime('%Y%m%d')+
        "&stockNo="+
        str(stock_number)
    )
    data = json.loads(urlopen(url).read())
    return pd.DataFrame(data['data'],columns=data['fields'])


# 根據使用者輸入的日期，以月為單位，重複呼叫爬取月股價的函式
def craw_stock(stock_number, start_month):
    b_month = date(*[int(x) for x in start_month.split('-')])
    now = dtime.now().strftime("%Y-%m-%d")  # 取得現在時間
    e_month = date(*[int(x) for x in now.split('-')])

    result = pd.DataFrame()
    for dt in rrule.rrule(rrule.MONTHLY, dtstart=b_month, until=e_month):
        result = pd.concat([result, craw_one_month(stock_number, dt)], ignore_index=True)
        time.sleep(2000.0 / 1000.0);

    return result



if __name__ == '__main__':
    # df = craw_stock(3034,"2020-10-18")
    # df.to_csv('3034.csv', encoding='utf_8_sig')

    # Update connection string information
    # host = "127.0.0.1"
    # dbname = "Stock001"
    # user = "postgres"
    # password = "roger0"
    # sslmode = "require"
    #
    # conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
    # conn = psycopg2.connect(conn_string)

    conn = psycopg2.connect(database="Stock001", user="postgres", password="roger0", host="127.0.0.1", port="5432")
    print("Connect DB success.")
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS COMPANY;")
    print("Finished dropping table (if existed)")

    cur.execute('''CREATE TABLE COMPANY
               (ID INT PRIMARY KEY     NOT NULL,
               NAME           TEXT    NOT NULL,
               AGE            INT     NOT NULL,
               ADDRESS        CHAR(50),
               SALARY         REAL);''')
    print("Create table success.")



    conn.commit()
    cur.close()
    conn.close()