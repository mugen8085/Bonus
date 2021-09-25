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

import dearpygui.dearpygui as dpg
from dearpygui.demo import show_demo
show_demo()

class iDate(object):
    def __init__(self, year = 1970, month = 1, day = 1):
        self.Year = year
        self.Month = month
        self.Day = day

    def SetDate(self, year, month, day):
        self.Year = year
        self.Month = month
        self.Day = day

    def GetDate(self, year, month, day):
        year = self.Year
        month = self.Month
        day = self.Day

    def GetDateStr(self):
        datestr = str(self.Year).zfill(4) + "-" + str(self.Month).zfill(2) + "-" + str(self.Day).zfill(2)
        return datestr

class App:
    def __init__(self):
        self._f = float()
        self.Window()
        self.count = 0
        self.time = float()
        self.BeginDate = iDate()
        self.EndDate = iDate()

    def save_callback(self,Sender,Data):
        # print(self.BeginDate.GetDateStr())
        print(dpg.get_value("string123"))
        # print(self.time)
        # print(Sender)
        # print(Data)

    def GetDate(self,Sender,Data):
        print(Sender)
        print(Data)
        # print(dpg.get_value("datepicker"))
        # print(dpg.get_value("datepicker"))

    def Run(self):
        while (dpg.is_dearpygui_running()):
            # do something.
            self.Update()
            dpg.render_dearpygui_frame()

    def Update(self):
        self.count += 1
        # print(self.count)

    def Window(self):
        with dpg.window(label="Example Window", height=256, width=256):
            # dpg.add_text("Hello world")
            dpg.add_button(label="Save", callback=self.save_callback)
            dpg.add_input_text(label="string123", callback=self.save_callback)
            dpg.add_slider_float(label="float")
            # dpg.add_date_picker(label="datepicker", default_value={'month_day': 1, 'year': 50, 'month': 1}, callback=self.GetDate)
            self.time = dpg.add_date_picker(label="datepicker", level=dpg.mvDatePickerLevel_Day,
                                            default_value={'month_day': 8, 'year': 120, 'month': 5},
                                            callback=self.GetDate)
        if not dpg.is_viewport_created():
            dpg.setup_viewport()
            dpg.set_viewport_height(900)
            dpg.set_viewport_width(1600)

if __name__ == '__main__':
    print("go")
    app = App()
    app.Run()





    # dpg.start_dearpygui()
    # dpg.cleanup_dearpygui()

