import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from Common.LeftNavigationButton import LeftNavButton, LeftNavSubButton
from Pages.ThzCxDataMgr import ThzCxDataMgr
from Pages.ThzCgDataMgr import ThzCxGpDataMgr
from Pages.ThzDataBaseMgr import ThzDataBaseMgr
from Pages.ThzGpDataMgr import ThzGpDataMgr
from Pages.ThzSampleTypeMgr import ThzSampleTypeMgr
from Pages.ThzSysOptLog import ThzSysOptLogMgr
from Pages.ThzSysParamsSetting import ThzSysParamsSetting
from Pages.ThzSystemSettingCfgMgr import ThzSystemSettingCfgMgr
from Ui.UiSysSettingPage import Ui_Form


def CreateNavButton(p, txt):
    btn = LeftNavButton()
    btn.setObjectName("navBtn")
    btn.setMinimumSize(QtCore.QSize(270, 45))
    btn.setMaximumSize(QtCore.QSize(270, 45))
    btn.setParent(p)
    btn.Text(txt)
    return btn


def CreateNavSubBtn(p, txt):
    btn = LeftNavSubButton()
    btn.setParent(p)
    btn.setObjectName("navSubBtn")
    btn.setMinimumSize(QtCore.QSize(270, 45))
    btn.setMaximumSize(QtCore.QSize(270, 45))
    btn.Text(txt)
    return btn


def CreateNavSubWidget(p):
    dataCfgWidget = QWidget(p)
    dataCfgWidget.setObjectName("navPageWidget")
    # item page
    dataCfgWidgetLayout = QVBoxLayout(dataCfgWidget)
    dataCfgWidgetLayout.setContentsMargins(0, 0, 0, 0)
    dataCfgWidgetLayout.setSpacing(0)
    dataCfgWidget.setVisible(False)
    return dataCfgWidget


class ThzSystemSettingPage(QWidget, Ui_Form):
    currBtn = None

    def __init__(self, parent=None):
        super(ThzSystemSettingPage, self).__init__(parent)
        self.setupUi(self)
        self.retranslateUi(self)

        self.sysParamsCfgWidget = None
        self.dataCfgWidget = None
        self.btnSysParamsCfg = None
        self.scanDataWidget = None
        self.btnLogMgr = None
        self.btnScanData = None
        self.btnDataCfg = None
        self.btnCxGp = None
        self.btnCxData = None
        self.btnGpData = None
        self.btnDataPack = None
        self.btnSysCfg = None
        self.btnDatabaseMgr = None
        self.pageDataBaseMgr = ThzDataBaseMgr()
        self.stackedWidget.addWidget(self.pageDataBaseMgr)
        self.ThzSampleTypeMgr = ThzSampleTypeMgr()
        self.stackedWidget.addWidget(self.ThzSampleTypeMgr)
        self.pageGpData = ThzGpDataMgr()
        self.stackedWidget.addWidget(self.pageGpData)
        self.pageCxGpDataMgr = ThzCxGpDataMgr()
        self.stackedWidget.addWidget(self.pageCxGpDataMgr)
        self.pageCxDataMgr = ThzCxDataMgr()
        self.stackedWidget.addWidget(self.pageCxDataMgr)
        self.sysOptLogMgr = ThzSysOptLogMgr()
        self.stackedWidget.addWidget(self.sysOptLogMgr)
        # self.sysParamsSetting= ThzSysParamsSetting()
        # self.stackedWidget.addWidget(self.sysParamsSetting)
        # 初始化导航栏
        self.CreateLeftNavigation()
        # 注册按钮事件
        self.ButtonsEventRegister()

    # 创建导航菜单
    def CreateLeftNavigation(self):
        hgbx = QtWidgets.QGroupBox(self.gbxLeft)
        hgbx.setContentsMargins(0, 0, 0, 0)
        hl = QHBoxLayout()
        hl.setSpacing(0)
        hl.setContentsMargins(0, 0, 0, 0)
        hl.setObjectName("horizontalGroupBox")
        vl = QVBoxLayout(hgbx)
        vl.setSpacing(0)
        vl.setContentsMargins(0, 0, 0, 0)
        self.btnDataCfg = CreateNavButton(hgbx, "数据配置")
        self.btnDataCfg.LeftIcon("./Res/folder.png")
        self.btnDataCfg.setCheckable(True)
        vl.addWidget(self.btnDataCfg)
        self.dataCfgWidget = CreateNavSubWidget(hgbx)
        self.btnDatabaseMgr = CreateNavSubBtn(hgbx, "样品分类")
        self.btnDatabaseMgr.LeftIcon("./Res/folder.png")
        self.btnDatabaseMgr.setCheckable(True)
        # self.btnSampleType = CreateNavSubBtn(hgbx, "样品分类")
        # self.btnSampleType.LeftIcon("./Res/folder.png")
        self.dataCfgWidget.layout().addWidget(self.btnDatabaseMgr)
        self.dataCfgWidget.layout().addWidget(self.btnDataPack)
        # self.dataCfgWidget.layout().addWidget(self.btnSampleType)
        vl.addWidget(self.dataCfgWidget)

        self.btnScanData = CreateNavButton(hgbx, "扫描数据")
        self.btnScanData.LeftIcon("./Res/folder.png")
        self.btnScanData.setCheckable(True)
        vl.addWidget(self.btnScanData)
        self.scanDataWidget = CreateNavSubWidget(hgbx)
        self.btnGpData = CreateNavSubBtn(hgbx, "光谱数据")
        self.btnGpData.LeftIcon("./Res/folder.png")
        self.btnGpData.setCheckable(True)
        self.btnCxGp = CreateNavSubBtn(hgbx, "成像光谱数据")
        self.btnCxGp.LeftIcon("./Res/folder.png")
        self.btnCxGp.setCheckable(True)
        self.btnCxData = CreateNavSubBtn(hgbx, "成像数据")
        self.btnCxData.LeftIcon("./Res/folder.png")
        self.btnCxData.setCheckable(True)
        self.scanDataWidget.layout().addWidget(self.btnGpData)
        self.scanDataWidget.layout().addWidget(self.btnCxGp)
        self.scanDataWidget.layout().addWidget(self.btnCxData)
        vl.addWidget(self.scanDataWidget)

        self.btnLogMgr = CreateNavButton(hgbx, "日志管理")
        self.btnLogMgr.LeftIcon("./Res/folder.png")
        self.btnLogMgr.setCheckable(True)
        vl.addWidget(self.btnLogMgr)
        self.sysParamsCfgWidget = CreateNavSubWidget(hgbx)
        vl.addWidget(self.sysParamsCfgWidget)

        hl.addWidget(hgbx, 0, QtCore.Qt.AlignTop)
        self.gbxLeft.setLayout(hl)

    def ResetBtnChecked(self, btn):
        if self.currBtn is None:
            btn.setStyleSheet('''color:white;''')
            self.currBtn = btn
            return
        if btn.isChecked():
            btn.setStyleSheet('''color:white;''')
        self.currBtn.setStyleSheet('''color:#FF4D4D4D;''')
        self.currBtn.setChecked(not self.currBtn.isChecked())
        if self.currBtn.isChecked():
            self.currBtn.setStyleSheet('''color:white;''')
        self.currBtn = btn

    def ButtonsEventRegister(self):
        self.btnDataCfg.clicked.connect(self.OnBtnDataCfgClicked)
        self.btnDatabaseMgr.clicked.connect(self.OnBtnDataBaseMgrClicked)
        # self.btnDataPack.clicked.connect(self.OnBtnDataPackClicked)
        # self.btnSampleType.clicked.connect(self.OnBtnSampleTypeClicked)
        self.btnScanData.clicked.connect(self.OnBtnScanDataClicked)
        self.btnGpData.clicked.connect(self.OnBtnGpDataClicked)
        self.btnCxGp.clicked.connect(self.OnBtnCxGpClicked)
        self.btnCxData.clicked.connect(self.OnBtnCxDataClicked)
        # self.btnSysParamsCfg.clicked.connect(self.OnBtnSysParamsCfgClicked)
        self.btnLogMgr.clicked.connect(self.OnBtnLogMgrClicked)

    def OnBtnDataCfgClicked(self):
        self.dataCfgWidget.setVisible(not self.dataCfgWidget.isVisible())
        self.stackedWidget.setCurrentIndex(0)
        self.ResetBtnChecked(self.btnDataCfg)

    def OnBtnDataBaseMgrClicked(self):
        print("点击数据库管理")
        self.stackedWidget.setCurrentIndex(0)
        self.ResetBtnChecked(self.btnDatabaseMgr)

    def OnBtnDataPackClicked(self):
        print("点击数据功能包")
        self.stackedWidget.setCurrentIndex(1)
        self.ResetBtnChecked(self.btnDataPack)

    def OnBtnSampleTypeClicked(self):
        print("点击系统配置文件")
        # self.stackedWidget.setCurrentIndex(1)
        # self.ResetBtnChecked(self.btn)

    def OnBtnGpDataClicked(self):
        print("点击光谱数据")
        self.stackedWidget.setCurrentIndex(2)
        self.ResetBtnChecked(self.btnGpData)

    def OnBtnCxGpClicked(self):
        print("点击成像光谱数据")
        self.stackedWidget.setCurrentIndex(3)
        self.ResetBtnChecked(self.btnCxGp)

    def OnBtnCxDataClicked(self):
        print("点击成像数据")
        self.stackedWidget.setCurrentIndex(4)
        self.ResetBtnChecked(self.btnCxData)

    def OnBtnLogMgrClicked(self):
        print("点击日志管理")
        self.stackedWidget.setCurrentIndex(5)
        self.ResetBtnChecked(self.btnLogMgr)

    def OnBtnScanDataClicked(self):
        print("点击扫描数据")
        self.scanDataWidget.setVisible(not self.scanDataWidget.isVisible())
        self.stackedWidget.setCurrentIndex(2)
        self.ResetBtnChecked(self.btnScanData)

    def OnBtnSysParamsCfgClicked(self):
        print("点击系统参数配置")
        self.sysParamsCfgWidget.setVisible(not self.sysParamsCfgWidget.isVisible())
        self.stackedWidget.setCurrentIndex(6)
        self.ResetBtnChecked(self.btnSysParamsCfg)
