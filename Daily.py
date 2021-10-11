from Tools import *
from Stock import *
import dearpygui.dearpygui as dpg
from dearpygui.logger import mvLogger
import time
from dearpygui.demo import show_demo
# show_demo()

# 讀取INI檔案
InitFile = IniTool(Path='D:\\Projects\\Bonus\\Initialization.ini')
logger = mvLogger()
logger.log_level = 0


class App:
    def __init__(self, parent=None):
        self.DataPath = None
        self.DataStartDate = None
        self.StartDate = None
        self.WindowPositionX = None
        self.WindowPositionY = None

        self.nBeginYear = 2019
        self.nBeginMonth = 1
        self.nBeginDay = 1
        self.nEndYear = 1970
        self.nEndMonth = 1
        self.nEndDay = 1

        self.LoadInitFile()

        self.ExecuteTime = time.localtime()
        # TimeStr = str(self.ExecuteTime.tm_year) + "-" + str(self.ExecuteTime.tm_mon).zfill(2) + "-" + str(self.ExecuteTime.tm_mday).zfill(
        #     2) + " " + str(self.ExecuteTime.tm_hour).zfill(2) + ":" + str(self.ExecuteTime.tm_min).zfill(2) + ":" + str(
        #     self.ExecuteTime.tm_sec).zfill(2)
        #================= UI =================.
        self.count = 0
        if parent:
            self.window_id = parent
        else:
            self.window_id = dpg.add_window(label="MyApp")
        # print(self.window_id)
        dpg.set_primary_window(self.window_id, True)
        # window_id = dpg.window(label="MyApp")

        if not dpg.is_viewport_created():
            vp = dpg.create_viewport(title="MyApp", width=430, height=750, x_pos=int(self.WindowPositionX), y_pos=int(self.WindowPositionY))
            dpg.setup_dearpygui(viewport=vp)
            dpg.show_viewport(vp)
            dpg.set_viewport_height(950)
            dpg.set_viewport_width(950)

        # self.slider_float = dpg.add_slider_float(label="float", parent=self.window_id, width=100)

        # self.ID_GetWinSize = dpg.add_button(parent=self.window_id, label="GetWinSize", callback=self.callback_getwinsize )
        # dpg.add_same_line(parent=self.window_id)
        dpg.add_text(parent=self.window_id, default_value="Time:")
        dpg.add_same_line(parent=self.window_id)
        self.ID_TimeText = dpg.add_button(parent=self.window_id, label="0", callback=self.callback_update_enddate)
        self.ID_BtnBeginDate = 0
        self.ID_BeginDate = None
        self.ID_BeginDatePicker= None
        self.ID_BeginYear = None
        self.ID_BeginMonth = None
        self.ID_BeginDay = None


        self.ID_BtnEndDate = 0
        self.ID_EndDate = None
        self.ID_EndDatePicker = None
        self.ID_EndYear = None
        self.ID_EndMonth = None
        self.ID_EndDay = None

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
        self.WindowPositionX = InitFile.Read('Information', 'WindowPositionX')
        self.WindowPositionY = InitFile.Read('Information', 'WindowPositionY')
        print('WindowPositionX:'+str(self.WindowPositionX))
        print('WindowPositionY:'+str(self.WindowPositionY))

    def Update(self):
        self.count += 1
        LocalTime = time.localtime()
        TimeStr = str(LocalTime.tm_year) + "-" + str(LocalTime.tm_mon).zfill(2) + "-" + str(LocalTime.tm_mday).zfill(2) + " " + str(LocalTime.tm_hour).zfill(2) + ":" + str(LocalTime.tm_min).zfill(2) + ":" + str(LocalTime.tm_sec).zfill(2)
        # print(LocalTime)
        # dpg.set_value(self.ID_TimeText,TimeStr)
        dpg.set_item_label(self.ID_TimeText, TimeStr)

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
        # 取得當前時間.
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
        dpg.set_value(self.ID_EndYear, self.ExecuteTime.tm_year)
        dpg.set_value(self.ID_EndMonth, self.ExecuteTime.tm_mon)
        dpg.set_value(self.ID_EndDay, self.ExecuteTime.tm_mday)

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
                                default_value={'month_day': self.ExecuteTime.tm_mon, 'year': self.ExecuteTime.tm_year-1900, 'month': self.ExecuteTime.tm_mday}, callback=self.GetDate)
        # with dpg.window(label="EndDate", width=180, height=210, pos=(60, 50)):
        #     dpg.add_date_picker(label="datepicker", level=dpg.mvDatePickerLevel_Day,
        #                         default_value={'month_day': 8, 'year': 120, 'month': 5})

    def callback_update_enddate(self):
        LocalTime = time.localtime()
        dpg.set_value(self.ID_EndYear, str(LocalTime.tm_year))
        dpg.set_value(self.ID_EndMonth, str(LocalTime.tm_mon))
        dpg.set_value(self.ID_EndDay, str(LocalTime.tm_mday))

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
    app = App()
    app.Run()
    app = None


