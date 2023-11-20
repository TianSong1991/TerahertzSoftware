import datetime
from AppData import *
import globalvar as gl
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Entity.models import User
from Common.DialogEx import DialogEx
from Common.SwitchButton import SwitchButton


class Login(DialogEx):
    user = None

    def __init__(self):
        super(Login, self).__init__(None)

        self.set2BtnMode()
        self.content = QWidget()
        self.content.setStyleSheet('font-weight:bold; font-size:11pt;')
        self.vLayout = QVBoxLayout(self.content)
        self.vLayout.setSpacing(0)
        self.vLayout.setContentsMargins(0, 40, 0, 0)
        self.hLayout1 = QHBoxLayout()
        self.label1 = QLabel('用户名：', self.content)
        self.hLayout1.addWidget(self.label1)

        self.txtUser = QLineEdit(self.content)
        self.hLayout1.addWidget(self.txtUser)
        self.vLayout.addLayout(self.hLayout1)
        self.vSpacer = QSpacerItem(20, 30, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.vLayout.addItem(self.vSpacer)

        self.hLayout2 = QHBoxLayout()
        self.label2 = QLabel('密　码：', self.content)
        self.hLayout2.addWidget(self.label2)

        self.txtPwd = QLineEdit(self.content)
        self.txtPwd.setEchoMode(QLineEdit.Password)
        self.hLayout2.addWidget(self.txtPwd)
        self.vLayout.addLayout(self.hLayout2)

        self.hLayout4 = QHBoxLayout()
        self.hLayout4.setContentsMargins(0, 5, 0, 5)
        self.spacer1 = QSpacerItem(65, 10, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.hLayout4.addItem(self.spacer1)
        self.label3 = QLabel('记住密码', self.content)
        self.label3.setStyleSheet('font-size:12px; color:#FF475D')
        self.hLayout4.addWidget(self.label3)

        self.spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hLayout4.addItem(self.spacer)

        self.btnAuto = SwitchButton(self.content)
        self.btnAuto.setFixedSize(60, 22)
        self.hLayout4.addWidget(self.btnAuto)
        self.vLayout.addLayout(self.hLayout4)

        self.hLayout3 = QHBoxLayout()
        self.hSpacer = QSpacerItem(66, 8, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.hLayout3.addItem(self.hSpacer)

        self.lblInfo = QLabel(self.content)
        self.lblInfo.setStyleSheet('color: #FFFF475D; font-size:10pt')
        self.hLayout3.addWidget(self.lblInfo)
        self.vLayout.addLayout(self.hLayout3)

        self.setContent(self.content)
        self.setTitle('太赫兹时域光谱系统')
        self.resize(380, 180)
        if len(SysConf.appData.loginCode) == 0 \
                or SysConf.appData.loginCode[0] == 48:
            return
        tem = bytes(SysConf.appData.loginCode).decode('utf8')
        arr = tem.split('#')
        self.btnAuto.setChecked(True)
        self.txtUser.setText(arr[1])
        self.txtPwd.setText(arr[2])


    @pyqtSlot()
    def on_btnOk_clicked(self):
        if gl.isStrNoneOrEmpty(self.txtUser.text()) \
                or gl.isStrNoneOrEmpty(self.txtPwd.text()):
            self.lblInfo.setText('账号和密码不能为空，请输入！')
            return

        u = User.get_or_none(User.Name == self.txtUser.text() and User.Pwd == self.txtPwd.text())
        if u is None:
            self.lblInfo.setText('账号或密码不正确，请正确输入！')
            return
        if self.btnAuto.isChecked():
            SysConf.appData.loginCode = list((f'1#{u.Name}#{u.Pwd}').encode('utf8'))
        else:
            SysConf.appData.loginCode = list(('0##').encode('utf8'))


        self.user = u
        SysConf.appData.loginUser = u.Name
        self.done(QDialog.Accepted)
