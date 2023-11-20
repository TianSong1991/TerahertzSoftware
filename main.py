import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Entity.models import DbInit
from Core.WorkFlow import *
from Core.MotorHelper import *
from Core.UsbBoardHelper import *
from Pages.Login import Login
from Pages.ThzMainWindow import ThzMainWindow
import pandas
import shelve
if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)

    with open("Res/sys.style", "r", encoding='utf-8') as f:
        style = f.read()
    app.setStyleSheet(style)

    DbInit()

    gl.init()  # 初始化全局变量
    SysConf.load()  # 加载配置文件

    login = Login()
    if login.showDialog():
        usb = UsbBoardHelper()
        motor = MotorHelper()
        SysConf.usb = usb
        SysConf.motor = motor
        SysConf.gpFlow = GpWorkFlow()
        SysConf.cgFlow = CgWorkFlow(usb)
        SysConf.cxFlow = CxWorkFlow(usb, motor)

        if usb.isUsbEnable() is True:
            print('A')
        else:
            print('B')

        wnd = ThzMainWindow(login.user)
        wnd.show()
        wnd.Initialize()
        gl.appMainWnd = wnd
        sys.exit(app.exec_())
