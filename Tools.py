import os
import configparser

#檔案目錄工具
class DirTool:
    # 建構式
    def __init__(self, Path = ".\\"):
        self.Path = Path

    def GetPath(self):
        return self.Path

    def GetList(self):
        dirlist = []
        filelist = []
        for dirPath, dirNames, fileNames in os.walk(self.Path):
           for f in dirNames:
               dirlist.append(f)
           for f in fileNames:
               filelist.append(os.path.join(dirPath, f))
        return dirlist, filelist

    def GetExtension(self, Path):
        return os.path.splitext(Path)[-1]

#讀取ini檔案工具
class IniTool:
    #建構式
    def __init__(self, Path = ".\\Initialization.ini"):
        self.Path = Path
        self.conf = []
        self.LoadIni()

    def LoadIni(self):
        print('Load init file: '+self.Path)
        #創建對象
        self.conf = configparser.ConfigParser()
        self.conf.read(self.Path)

    #取得當前檔案位置
    def GetPath(self):
        return self.Path

    #重設檔案位置
    def SetPath(self, Path):
        self.Path = Path

    def Read(self, title, item):
        return self.conf.get(title, item)