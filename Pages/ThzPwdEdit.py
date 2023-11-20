from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Common.DialogEx import DialogEx
from Common.MessageBoxEx import MessageBoxEx
from Entity.models import User


class ThzPwdEdit(DialogEx):
    Id = 0

    def __init__(self, Id=0):
        super(ThzPwdEdit, self).__init__(None)
        self.content = QWidget()
        self.content.setStyleSheet('''
            QGroupBox{border:none;}
        ''')
        self.Id = Id
        self.set1BtnMode()
        self.verticalLayout = QVBoxLayout(self.content)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gbxBottom = QtWidgets.QGroupBox(self.content)
        self.gbxBottom.setTitle("")
        self.gbxBottom.setAlignment(QtCore.Qt.AlignCenter)
        self.gbxBottom.setObjectName("gbxBottom")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.gbxBottom)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.txtConfirmPwd = QtWidgets.QLineEdit(self.gbxBottom)
        self.txtConfirmPwd.setMinimumSize(QtCore.QSize(200, 30))
        self.txtConfirmPwd.setMaximumSize(QtCore.QSize(150, 30))
        self.txtConfirmPwd.setEchoMode(QLineEdit.Password)
        self.txtConfirmPwd.setObjectName("txtConfirmPwd")
        self.gridLayout.addWidget(self.txtConfirmPwd, 2, 3, 1, 1)
        self.label = QtWidgets.QLabel(self.gbxBottom)
        self.label.setObjectName("label")
        self.label.setText("旧密码:")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.txtNewPwd = QtWidgets.QLineEdit(self.gbxBottom)
        self.txtNewPwd.setMinimumSize(QtCore.QSize(200, 30))
        self.txtNewPwd.setMaximumSize(QtCore.QSize(150, 30))
        self.txtNewPwd.setEchoMode(QLineEdit.Password)
        self.txtNewPwd.setObjectName("txtNewPwd")
        self.gridLayout.addWidget(self.txtNewPwd, 1, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gbxBottom)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("新密码:")
        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gbxBottom)
        self.label_3.setObjectName("label_3")
        self.label_3.setText("确认密码:")
        self.gridLayout.addWidget(self.label_3, 2, 1, 1, 1)
        self.txtOldPwd = QtWidgets.QLineEdit(self.gbxBottom)
        self.txtOldPwd.setEchoMode(QLineEdit.Password)
        self.txtOldPwd.setMinimumSize(QtCore.QSize(200, 30))
        self.txtOldPwd.setMaximumSize(QtCore.QSize(200, 30))
        self.txtOldPwd.setObjectName("txtOldPwd")
        self.gridLayout.addWidget(self.txtOldPwd, 0, 3, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.gbxBottom)

        self.lblTitle.setText("修改密码")
        self.setContent(self.content)
        self.resize(297, 210)

        self.btnOk.clicked.connect(self.OnBtnOkClicked)

    def OnBtnOkClicked(self):
        user = User.select().where(User.Id == self.Id)
        if len(user) <= 0:
            MessageBoxEx.show("请先登录!", "提示", "确定")
            return
        if user[0].Pwd != self.txtOldPwd.text():
            MessageBoxEx.show("请先登录!", "提示", "确定")
            return
        if self.txtNewPwd.text() == self.txtConfirmPwd.text():
            User.update({User.Pwd: self.txtNewPwd.text()}).where(User.Id == self.Id)
            MessageBoxEx.show("修改密码成功", "提示", "确定")
        else:
            MessageBoxEx.show("新密码与确认密码不一致!")
