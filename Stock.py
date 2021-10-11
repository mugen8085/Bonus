import pandas as pd
from datetime import date,timedelta
from io import StringIO

class StockTool:
    #建構式
    def __init__(self, datapath):
        self.Path = datapath
        self.df_HS = pd.read_csv('holidaySchedule.csv', index_col=0)

    def GetDataFrame(self,date):
        file = self.Path + date + '.csv'
        datas = pd.DataFrame()
        f = open(file, 'r')
        text = f.read()
        f.close()
        df = pd.read_csv(StringIO(text.replace("=", "")), thousands=",",
                         header=["證券代號" in l for l in text.split("\n")].index(True) - 1)
        df.insert(0, 'Date', date)
        return df

    def GetDayList(self, begin, end):
        # 建立搜索清單
        DayList = []
        for i in range((end - begin).days + 1):
            day = begin + timedelta(days=i)
            w_day = day.weekday()
            c_day = day.strftime("%Y%m%d")
            NotInList = True
            for index, row in self.df_HS.iterrows():
                if str(c_day) == str(row['Date']):
                    NotInList = False
            if (w_day != 5 and w_day != 6 and NotInList):
                DayList.append(c_day)
        return DayList

    # def DownloadData(self, daylist):
    #     for idx, val in enumerate(daylist):
    #         CurrentTime = dtime.now()
    #         if val == CurrentTime.strftime("%Y%m%d") and CurrentTime.hour < 14:
    #             break;
    #
    #         fullpath = DataPath + val + '.csv'
    #         # 確認是否有舊資料
    #         NoHistory = False
    #         if os.path.isfile(fullpath):
    #             # 檔案存在的處理
    #             print("\r 檔案存在。" + str(idx), end="")
    #         else:
    #             # 檔案不存在的處理
    #             print("\n檔案不存在。")
    #             NoHistory = True
    #         if NoHistory is True:
    #             url = 'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + val + '&type=ALL'
    #             print("\r Loading... " + str(round((idx + 1) / ListLen * 100, 2)) + "% " + val + " ", end="")
    #             r = requests.get(url, allow_redirects=True)
    #             open(fullpath, 'wb').write(r.content)
    #             time.sleep(15)