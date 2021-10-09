# # step1. import package
# import requests
# import pandas as pd
# import numpy as np
# from io import StringIO
#
# # step2. 進入目標網站,爬取盤後資訊
# date = '20210401'
# r = requests.post('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + date + '&type=ALL')
#
# # step3. 篩選出個股盤後資訊
# str_list = []
# for i in r.text.split('\n'):
#     if len(i.split('",')) == 17 and i[0] != '=':
#         i = i.strip(",\r\n")
#         str_list.append(i)
#
# # step4. 印出選股資訊
# df = pd.read_csv(StringIO("\n".join(str_list)))
# pd.set_option('display.max_rows', None)
# df.head(150)

# import bimpy
# import dearpygui.dearpygui as dpg
#
# class App(bimpy.App):
#     def __init__(self):
#         super(App, self).__init__(title='Test')
#         self.s = bimpy.String()
#         self.f = bimpy.Float()
#
#     def on_update(self):
#         bimpy.text("Hello, world!")
#         if bimpy.button("OK"):
#             print(self.s.value)
#
#         bimpy.input_text('string', self.s, 256)
#
#         bimpy.slider_float("float", self.f, 0, 1)


# ctx = bimpy.Context()
#
# ctx.init(600, 600, "Hello1")
#
# string = bimpy.String()
# f = bimpy.Float();
# count = 0
# while(not ctx.should_close()):
#         count += 1
#
#         with ctx:
#                 bimpy.text("Hello, world!")
#
#                 if bimpy.button("OK"):
#                         print(string.value)
#
#                 bimpy.input_text('string', string, 256)
#
#                 bimpy.slider_float("float", f, 0.0, 1.0)
from Tools import *
import dearpygui.dearpygui as dpg
from dearpygui.logger import mvLogger
import time
from dearpygui.demo import show_demo
# show_demo()

UIID = {
    'DateBegin': 1001,
    'DateEnd': 1002,
    'BtnSave': 1003,
    'InText1': 1004,
    'BtnDate': 1005
}

# class iDate(object):
#     def __init__(self, year = 1970, month = 1, day = 1):
#         self.Year = year
#         self.Month = month
#         self.Day = day
#
#     def SetDate(self, year, month, day):
#         self.Year = year
#         self.Month = month
#         self.Day = day
#
#     def GetDate(self, year, month, day):
#         year = self.Year
#         month = self.Month
#         day = self.Day
#
#     def GetDateStr(self):
#         datestr = str(self.Year).zfill(4) + "-" + str(self.Month).zfill(2) + "-" + str(self.Day).zfill(2)
#         return datestr
#
# class App1:
#     def __init__(self):
#         self._f = float()
#         self.Window()
#         self.count = 0
#         self.time = float()
#         self.BeginDate = iDate()
#         self.EndDate = iDate()
#         self.index = 0
#
#     def save_callback(self,Sender,Data):
#         # print(self.BeginDate.GetDateStr())
#         print(dpg.get_value(UIID['InText1']))
#
#         # print(self.time)
#         # print(Sender)
#         # print(Data)
#
#     def Callback_BeginDate(self, sender, data):
#         print("Callback_BeginDate")
#
#     def GetDate(self,Sender,Data):
#         print(Sender)
#         print(Data)
#         # print(dpg.get_value("datepicker"))
#         # print(dpg.get_value("datepicker"))
#
#     def Run(self):
#         while (dpg.is_dearpygui_running()):
#             # do something.
#             self.Update()
#             dpg.render_dearpygui_frame()
#
#     def Update(self):
#         self.count += 1
#         # print(self.count)
#
#     def NewProcessCall(self):
#         # process = multiprocessing.Process(target=NewProcess)
#         print('ok')
#
#     def Window(self):
#         with dpg.window(label="Example Window", height=256, width=256) as window_id:
#             print(window_id)
#             dpg.set_primary_window(window_id, True)
#             # dpg.add_text("Hello world")
#             dpg.add_button(label="Save", callback=self.save_callback)
#             dpg.add_button(label="BeginDate", callback=self.Callback_BeginDate)
#             dpg.add_same_line()
#             self.index = dpg.add_input_text(label="TestString", id=UIID['InText1'])
#             print(self.index)
#             dpg.add_slider_float(label="float")
#             # dpg.add_date_picker(label="datepicker", default_value={'month_day': 1, 'year': 50, 'month': 1}, callback=self.GetDate)
#             # dpg.add_date_picker(label="datepicker", level=dpg.mvDatePickerLevel_Day,
#             #                                 default_value={'month_day': 8, 'year': 120, 'month': 5},
#             #                                 callback=self.GetDate)
#         if not dpg.is_viewport_created():
#             # dpg.add_button(label='Read screen')
#             dpg.setup_viewport()
#             # vp = dpg.create_viewport(title="Window", width=430, height=750)
#             # dpg.setup_dearpygui(viewport=vp)
#             # dpg.show_viewport(vp)
#
#             dpg.set_viewport_height(480)
#             dpg.set_viewport_width(640)

# show_demo()

# class SDate:
#     def __init__(self):

# 讀取INI檔案
InitFile = IniTool(Path='D:\\Projects\\Bonus\\Initialization.ini')
logger = mvLogger()
logger.log_level = 0


class App:
    def __init__(self, parent=None):
        self.DataPath = None
        self.DataStartDate = None
        self.StartDate = None


        #================= UI =================.
        self.count = 0
        if parent:
            self.window_id = parent
        else:
            self.window_id = dpg.add_window(label="MyApp")
        print(self.window_id)
        dpg.set_primary_window(self.window_id, True)
        # window_id = dpg.window(label="MyApp")

        if not dpg.is_viewport_created():
            vp = dpg.create_viewport(title="MyApp", width=430, height=750, x_pos=1930, y_pos=200)
            dpg.setup_dearpygui(viewport=vp)
            dpg.show_viewport(vp)
            dpg.set_viewport_height(950)
            dpg.set_viewport_width(950)

        # self.slider_float = dpg.add_slider_float(label="float", parent=self.window_id, width=100)

        self.ID_GetWinSize = dpg.add_button(parent=self.window_id, label="GetWinSize", callback=self.callback_getwinsize )
        dpg.add_same_line(parent=self.window_id)
        dpg.add_text(parent=self.window_id, default_value="           Time:")
        dpg.add_same_line(parent=self.window_id)
        self.ID_TimeText = dpg.add_text(parent=self.window_id,default_value="0")

        self.ID_BtnBeginDate = 0
        self.ID_BeginDate = None
        self.ID_BeginDatePicker= None
        self.ID_BeginYear = None
        self.ID_BeginMonth = None
        self.ID_BeginDay = None
        self.nBeginYear = 2019
        self.nBeginMonth = 1
        self.nBeginDay = 1
        self.LoadInitFile()

        self.ID_BtnEndDate = 0
        self.ID_EndDate = None
        self.ID_EndDatePicker = None
        self.ID_EndYear = None
        self.ID_EndMonth = None
        self.ID_EndDay = None
        self.nEndYear = 1970
        self.nEndMonth = 1
        self.nEndDay = 1
        self.ShowInfo()
        self.UIBeginDate()
        self.UIEndDate()

        # dpg.add_same_line(parent=self.window_id)
        # self.ID_BeginDate = dpg.add_button(label="BeginDate", parent=self.window_id, callback=self.callback_begindate)

    def LoadInitFile(self):
        logger.log("LoadInitFile")
        # 讀取路徑
        self.DataPath = InitFile.Read('Information', 'DataPath')
        # 總資料開始日期
        self.DataStartDate = InitFile.Read('Information', 'DataStartDate')
        # 開始統計的日期
        self.StartDate = InitFile.Read('Information', 'StartDate')
        date = self.StartDate.split('-')
        self.nBeginYear = int(date[0])
        self.nBeginMonth = int(date[1])
        self.nBeginDay = int(date[2])

    def Update(self):
        self.count += 1
        print(time.localtime())

    def Run(self):
        while (dpg.is_dearpygui_running()):
            # do something.
            self.Update()
            dpg.render_dearpygui_frame()

    def ShowInfo(self):
        with dpg.group(parent=self.window_id):
            dpg.add_text(f'DataPath: {self.DataPath}')
            dpg.add_text(f'DataStartDate: {self.DataStartDate}')

    def UIBeginDate(self):
        # dpg.add_text("BeginDate(yyyy/mm/dd):", parent=self.window_id )
        self.ID_BtnBeginDate = dpg.add_button(parent=self.window_id, label="BeginDate(yyyy/mm/dd):", callback=self.callback_begindate)
        dpg.add_same_line(parent=self.window_id)
        dpg.add_text("   ", parent=self.window_id)
        dpg.add_same_line(parent=self.window_id)
        self.ID_BeginYear = dpg.add_input_text(parent=self.window_id, label="", decimal=True, width=40, callback=self.callback_inputtext)
        dpg.add_same_line(parent=self.window_id)
        dpg.add_text("/", parent=self.window_id)
        dpg.add_same_line(parent=self.window_id)
        self.ID_BeginMonth = dpg.add_input_text(parent=self.window_id, label="", decimal=True, width=20, callback=self.callback_inputtext)
        dpg.add_same_line(parent=self.window_id)
        dpg.add_text("/", parent=self.window_id)
        dpg.add_same_line(parent=self.window_id)
        self.ID_BeginDay = dpg.add_input_text(parent=self.window_id, label="", decimal=True, width=20, callback=self.callback_inputtext)
        dpg.set_value(self.ID_BeginYear, self.nBeginYear)
        dpg.set_value(self.ID_BeginMonth, self.nBeginMonth)
        dpg.set_value(self.ID_BeginDay, self.nBeginDay)

    def UIEndDate(self):
        # dpg.add_text("EndDate(yyyy/mm/dd):  ", parent=self.window_id )
        self.ID_BtnEndDate = dpg.add_button(parent=self.window_id, label="EndDate  (yyyy/mm/dd):", callback=self.callback_enddate)
        dpg.add_same_line(parent=self.window_id)
        dpg.add_text("   ", parent=self.window_id)
        dpg.add_same_line(parent=self.window_id)
        self.ID_EndYear = dpg.add_input_text(parent=self.window_id, label="", decimal=True, width=40, callback=self.callback_inputtext)
        dpg.add_same_line(parent=self.window_id)
        dpg.add_text("/", parent=self.window_id)
        dpg.add_same_line(parent=self.window_id)
        self.ID_EndMonth = dpg.add_input_text(parent=self.window_id, label="", decimal=True, width=20, callback=self.callback_inputtext)
        dpg.add_same_line(parent=self.window_id)
        dpg.add_text("/", parent=self.window_id)
        dpg.add_same_line(parent=self.window_id)
        self.ID_EndDay = dpg.add_input_text(parent=self.window_id, label="", decimal=True, width=20, callback=self.callback_inputtext)

    def GetDate(self,Sender,Data):
        # print(Sender)
        # print(Data)
        if Sender == self.ID_BeginDatePicker:
            dpg.set_value(self.ID_BeginYear, Data['year'] + 1900)
            dpg.set_value(self.ID_BeginMonth, Data['month'])
            dpg.set_value(self.ID_BeginDay, Data['month_day'])
        if Sender == self.ID_EndDatePicker:
            dpg.set_value(self.ID_EndYear, Data['year'] + 1900)
            dpg.set_value(self.ID_EndMonth, Data['month'])
            dpg.set_value(self.ID_EndDay, Data['month_day'])

    def callback_getwinsize(self):
        print(dpg.get_item_rect_size(self.window_id))
        print(dpg.get_viewport_pos())

    def callback_begindate(self):
        if self.ID_BeginDate:
            if dpg.is_item_shown(self.ID_BeginDate):
                dpg.hide_item(self.ID_BeginDate)
            else:
                dpg.show_item(self.ID_BeginDate)
            dpg.focus_item(self.ID_BeginDate)
        else:
            logger.log("BeginDatePicker")
            logger.log(str(self.nBeginYear))
            logger.log(str(self.nBeginMonth))
            logger.log(str(self.nBeginDay))
            self.ID_BeginDate = dpg.add_window(label="BeginDate", pos=(60, 50))
            self.ID_BeginDatePicker = dpg.add_date_picker(parent=self.ID_BeginDate, label="datepicker", level=dpg.mvDatePickerLevel_Day,
                                default_value={'month_day': self.nBeginDay, 'year': self.nBeginYear-1900, 'month': self.nBeginMonth}, callback=self.GetDate)
        # with dpg.window(label="BeginDate", width=180, height=210, pos=(60, 30)):
        #     dpg.add_date_picker(label="datepicker", level=dpg.mvDatePickerLevel_Day,
        #         default_value={'month_day': 8, 'year': 120, 'month': 5})

    def callback_enddate(self):
        if self.ID_EndDate:
            if dpg.is_item_shown(self.ID_EndDate):
                dpg.hide_item(self.ID_EndDate)
            else:
                dpg.show_item(self.ID_EndDate)
            dpg.focus_item(self.ID_EndDate)
        else:
            self.ID_EndDate = dpg.add_window(label="EndDate", pos=(60, 70))
            self.ID_EndDatePicker = dpg.add_date_picker(parent=self.ID_EndDate, label="datepicker", level=dpg.mvDatePickerLevel_Day,
                                default_value={'month_day': 8, 'year': 120, 'month': 5}, callback=self.GetDate)
        # with dpg.window(label="EndDate", width=180, height=210, pos=(60, 50)):
        #     dpg.add_date_picker(label="datepicker", level=dpg.mvDatePickerLevel_Day,
        #                         default_value={'month_day': 8, 'year': 120, 'month': 5})

    def callback_inputtext(self):
        isChange = False
        # if self.nBeginYear != dpg.get_value(self.ID_BeginYear):
        #     self.nBeginYear = int(dpg.get_value(self.ID_BeginYear))
        #     isChange = True
        # if self.nBeginMonth != int(dpg.get_value(self.ID_BeginMonth)):
        #     self.nBeginMonth = int(dpg.get_value(self.ID_BeginMonth))
        #     isChange = True
        # if self.nBeginDay != int(dpg.get_value(self.ID_BeginDay)):
        #     self.nBeginDay = int(dpg.get_value(self.ID_BeginDay))
        #     isChange = True
        #
        # if isChange:
        #     # print(str(self.nBeginYear) + " " + str(self.nBeginMonth) + " " + str(self.nBeginDay))
        #     print("test")
        # print(self.nBeginMonth)
        # print(self.nBeginDay)

    def __del__(self):
        print("App close.")


if __name__ == '__main__':
    print("go")
    app = App()
    app.Run()
    app = None




    # dpg.setup_viewport()
    # dpg.set_viewport_height(480)
    # dpg.set_viewport_width(640)
    # dpg.start_dearpygui(primary_window="test")




    # dpg.start_dearpygui()
    # dpg.cleanup_dearpygui()

