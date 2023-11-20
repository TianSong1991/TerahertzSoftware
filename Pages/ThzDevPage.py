from AppData import *
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from Pages.ThzDevCxPage import ThzDevCxPage
from Pages.ThzDevGpPage import ThzDevGpPage
from Ui.UiThzDev import Ui_ThzDevMainForm


class ThzDevPage(QWidget, Ui_ThzDevMainForm):
    def __init__(self, parent=None):
        super(ThzDevPage, self).__init__(parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.cbxSwitch.setIconSize(QSize(20, 20))
        self.cbxSwitch.addItem(QIcon('./Res/search.png'), "光谱模式")
        self.cbxSwitch.addItem(QIcon('./Res/search.png'), "成像模式")
        self.cbxSwitch.setStyleSheet('QComboBox QAbstractItemView::item { height: 50px; }')
        self.cbxSwitch.setView(QListView())
        self.GpPage = ThzDevGpPage()
        self.CxPage = ThzDevCxPage()

        self.stackedWidget.addWidget(self.GpPage)
        self.stackedWidget.addWidget(self.CxPage)
        self.btnSave.clicked.connect(self.onBtnSave)

        self.cbxSwitch.currentIndexChanged.connect(self.OnCbxSwitch_Current_Index_Changed)

    def OnCbxSwitch_Current_Index_Changed(self):
        if self.cbxSwitch.currentText() == "光谱模式":
            self.stackedWidget.setCurrentIndex(0)
        else:
            self.stackedWidget.setCurrentIndex(1)
        self.lblInfo.setText("")

    def onBtnSave(self):
        if self.cbxSwitch.currentIndex() == 0:
            SysConf.saveDevGp()
            self.lblInfo.setText("光谱设备参数保存成功！")
        else:
            SysConf.saveDevCx()
            self.lblInfo.setText("成像设备参数保存成功！")


