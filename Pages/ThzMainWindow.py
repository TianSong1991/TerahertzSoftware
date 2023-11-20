import string

from AppData import *
import globalvar as gl
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Entity.models import Role
from Pages.ThzPageDropList import ThzPageDropList
from Pages.ThzPwdEdit import ThzPwdEdit
from Pages.ThzUserInfoEdit import ThzUserInfoEdit
from Ui.UiMainFrame import Ui_UiMainFrame
from Pages.ThzGpPage import ThzGpPage
from Pages.ThzCxPage import ThzCxPage
from Common.MessageBoxEx import MessageBoxEx
from Pages.ThzDevPage import ThzDevPage
from Pages.ThzSystemSetting import ThzSystemSettingPage
from Pages.ThzUserAndRoleMgrPage import ThzUserAndRoleMgrPage


class ThzMainWindow(QMainWindow, Ui_UiMainFrame):
    user = None
    editNotify = pyqtSignal([str])

    def __init__(self, user):
        super(ThzMainWindow, self).__init__(None)
        self.setupUi(self)
        self.retranslateUi(self)
        self.user = user
        #self.setWindowState(Qt.WindowMaximized)
        self.setFixedSize(1920, 1040)
        self.buttonGroup.setExclusive(True)
        # self.buttonGroup.setProperty("per", self.btnGP)
        self.buttonGroup.buttonClicked.connect(lambda data: self.onBtnNavigate(data))
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_AttributeCount)
        self.setWindowModality(Qt.ApplicationModal)
        #desktop = QApplication.desktop()
        #x = (desktop.width() - self.width()) / 2
        #y = (desktop.height() - self.height()) / 2
        #self.move(int(x), int(y))
        self.dropList = ThzPageDropList(self)
        self.dropList.btnEdit.clicked.connect(self.OnDropList_btnEdit_clicked)
        self.dropList.listWidget.itemClicked.connect(self.OnDropList_listWidgetItem_clicked)
        self.dropList.hide()
        self.btnGP.setStyleSheet("font-family:'宋体'; font-size:16pt;")
        self.btnCX.setStyleSheet("font-family:'宋体'; font-size:16pt;")
        self.btnDev.setStyleSheet("font-family:'宋体'; font-size:16pt;")
        self.btnUsr.setStyleSheet("font-family:'宋体'; font-size:16pt;")
        self.btnSys.setStyleSheet("font-family:'宋体'; font-size:16pt;")
        self.btnSetting.setStyleSheet("font-family:'Webdings'; font-size:16pt;")
        self.btnMin.setStyleSheet("font-family:'Webdings'; font-size:16pt;")
        self.btnClose.setStyleSheet("font-family:'Webdings'; font-size:16pt;")
        self.editNotify.connect(self.OnUserInfoEditCallback)
        self.lblPhoto.setStyleSheet(f'border-radius:16px;border-image: url(./Avator/{self.user.Id}.png);'
                                    f'background-color:gray; background-position:center;')

        self.dropList.lblIcon.setStyleSheet(f'border-radius:16px;border-image: url(./Avator/{self.user.Id}.png);'
                                            f'background-color:gray; background-position:center;')

    def LoadUserRights(self, roleId):
        rightStr = Role.get_or_none(Role.Id == roleId).Rights
        rightArr = json.loads(rightStr)
        print(rightArr)
        jMap = {}
        for right in rightArr:
            right['isChecked']=2
            if right['txt'] == '光谱扫描':
                jMap['光谱扫描'] = True if right['isChecked'] == 2 else False

            if right['txt'] == '成像光谱':
                jMap['成像光谱'] = True if right['isChecked'] == 2 else False

            if right['txt'] == '成像扫描':
                jMap['成像扫描'] = True if right['isChecked'] == 2 else False

            if right['txt'] == '硬件管理':
                jMap['硬件管理'] = True if right['isChecked'] == 2 else False

            if right['txt'] == '用户管理':
                jMap['用户管理'] = True if right['isChecked'] == 2 else False

            if right['txt'] == '系统设置':
                jMap['系统设置'] = True if right['isChecked'] == 2 else False

        return jMap

    def OnDropList_listWidgetItem_clicked(self, item):
        widget = self.dropList.listWidget.itemWidget(item)
        _str = widget.lblName.text()
        if _str == "修改密码":
            self.pwdEdit = ThzPwdEdit(self.user.Id)
            gl.INFO("操作",self.user.Id,"用户点击修改密码")
            self.pwdEdit.show()
        elif _str == "皮肤设置":
            print("皮肤设置")
        elif _str == "系统设置":
            print("系统设置")
        elif _str == "文档帮助":
            gl.INFO("操作", self.user.Id, "用户点击文档帮助")
            QDesktopServices.openUrl(QUrl.fromLocalFile("./test.pdf"))
        else:
            gl.INFO("操作", self.user.Id, "用户点击退出系统")
            if MessageBoxEx.show("确认要退出当前系统吗?", "温馨提示", "是", "否") == 0:
                return
            else:
                self.close()

    def OnUserInfoEditCallback(self, txt):
        self.lblPhoto.setStyleSheet(f'border-radius:16px;border-image: url(./Avator/{self.user.Id}.png);'
                                    f'background-color:gray; background-position:center;')
        self.dropList.lblPhone.setText(txt)
        self.dropList.lblIcon.setStyleSheet(f'border-radius:16px;border-image: url(./Avator/{self.user.Id}.png);'
                                            f'background-color:gray; background-position:center;')

    def OnDropList_btnEdit_clicked(self):
        self.userInfoEdit = ThzUserInfoEdit(self.user.Id, self.editNotify)
        self.userInfoEdit.show()

    @pyqtSlot()
    def on_btnSetting_clicked(self):
        if self.dropList.isHidden():
            y = self.btnSetting.pos().y() + self.btnSetting.height()
            self.dropList.moveTo(self.btnSetting.pos().x() - self.dropList.width() + self.btnSetting.width(), y + 2)
            self.dropList.show()
        else:
            self.dropList.hide()

    @pyqtSlot()
    def on_btnMin_clicked(self):
        self.showMinimized()

    @pyqtSlot()
    def on_btnClose_clicked(self):
        if gl.waitOne(1) is False:
            MessageBoxEx.show('正在运行中,请先关闭设备！')
            return

        SysConf.saveConf()
        # view = self.btnGP.property("Tag")
        # view.closeEvent.set()
        # view.exitEvent.wait(50)
        self.close()

    def showEvent(self, event) -> None:
        print(self.mainWidget.width(), self.mainWidget.height())

    def resizeEvent(self, *args, **kwargs):
        print(args[0].oldSize(), args[0].size())

    def onBtnNavigate(self, btn):
        per = self.buttonGroup.property("per")
        if btn == per:
            return None

        if per is not None:
            old = per.property("Tag")
            if old is not None:
                old.setVisible(False)

        self.buttonGroup.setProperty("per", btn)

        temp = btn.property("Tag")
        if temp is not None:
            temp.setVisible(True)
            return None

        if btn is self.btnGP:
            temp = ThzGpPage(self.mainWidget)

        elif btn is self.btnCX:
            temp = ThzCxPage(self.mainWidget)

        elif btn is self.btnDev:
            temp = ThzDevPage(self.mainWidget)
            self.mainWidget.repaint()

        elif btn is self.btnUsr:
            temp = ThzUserAndRoleMgrPage(self.mainWidget)

        else:
            temp = ThzSystemSettingPage(self.mainWidget)

        print(self.width(), self.height(), self.mainWidget.width(), self.mainWidget.height())
        btn.setProperty("Tag", temp)
        temp.setGeometry(0, 0, self.mainWidget.width(), self.mainWidget.height())
        temp.show()
        if btn is self.btnCX:
            temp.contentResize()

    @staticmethod
    def isKeyInMap(jMap, key):
        if jMap is None:
            return False

        if key in jMap.keys():
            return jMap[key]
        else:
            return False

    def Initialize(self):
        jMap = self.LoadUserRights(self.user.RoleId)

        isFirstPage = False
        if ThzMainWindow.isKeyInMap(jMap, '光谱扫描') is False \
                and ThzMainWindow.isKeyInMap(jMap, '成像光谱') is False:
            self.btnGP.setVisible(False)
        else:
            isFirstPage = True
            self.onBtnNavigate(self.btnGP)
            temp = self.btnGP.property("Tag")
            temp.setVisibleModel(ThzMainWindow.isKeyInMap(jMap, '光谱扫描')
                                 , ThzMainWindow.isKeyInMap(jMap, '成像光谱'))

        if ThzMainWindow.isKeyInMap(jMap, '成像扫描') is False:
            self.btnCX.setVisible(False)
        else:
            if isFirstPage is False:
                isFirstPage = True
                self.onBtnNavigate(self.btnCX)
                temp = self.btnCX.property("Tag")

        if ThzMainWindow.isKeyInMap(jMap, '硬件管理') is False:
            self.btnDev.setVisible(False)
        else:
            if isFirstPage is False:
                isFirstPage = True
                self.onBtnNavigate(self.btnDev)
                temp = self.btnDev.property("Tag")

        if ThzMainWindow.isKeyInMap(jMap, '用户管理') is False:
            self.btnUsr.setVisible(False)
        else:
            if isFirstPage is False:
                isFirstPage = True
                self.onBtnNavigate(self.btnUsr)
                temp = self.btnUsr.property("Tag")

        if ThzMainWindow.isKeyInMap(jMap, '系统设置') is False:
            self.btnSys.setVisible(False)
        else:
            if isFirstPage is False:
                isFirstPage = True
                self.onBtnNavigate(self.btnSys)
                temp = self.btnSys.property("Tag")
        #self.onBtnNavigate(self.btnGP)
        #temp = self.btnGP.property("Tag")
        #temp.setGeometry(0, 0, 1360, 820)
        temp.show()

    def turn2GpView(self, mode, data):
        self.onBtnNavigate(self.btnGP)
        view = self.btnGP.property("Tag")
        if mode == 1:
            view.displayCgData(data)
        else:
            view.displayGpData(data)

    def turn2CxView(self, data):
        self.onBtnNavigate(self.btnCX)
        view = self.btnCX.property("Tag")
        view.displayData(data)
