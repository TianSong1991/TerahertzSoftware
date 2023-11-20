import shutil
import string

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath
from PyQt5.QtWidgets import *
from Common.DialogEx import DialogEx
from Common.MessageBoxEx import MessageBoxEx
from Core.WorkFlow import *
from Entity.models import User


class LabelEx(QLabel):
    clicked = pyqtSignal()

    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.clicked.emit()


class ThzUserInfoEdit(DialogEx):
    Uid = 0
    fileName = ""
    notify = pyqtSignal([str])

    def __init__(self, Uid=0, notify=None):
        super(ThzUserInfoEdit, self).__init__(None)
        user = User.get_or_none(User.Id == Uid)
        if user is None:
            return
        self.content = QWidget(self)
        self.content.setStyleSheet('''
                    QGroupBox,QLineEdit{border:none;}
                    QLabel{color:#FF4D4D4D;}
                ''')
        self.notify = notify
        self.set1BtnMode()
        self.Uid = Uid
        self.verticalLayout = QtWidgets.QVBoxLayout(self.content)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(self.content)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblIcon = LabelEx(self.groupBox_2)
        self.lblIcon.setMinimumSize(QtCore.QSize(80, 80))
        self.lblIcon.setMaximumSize(QtCore.QSize(80, 80))
        self.lblIcon.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblIcon.setText("")
        self.lblIcon.setAlignment(QtCore.Qt.AlignCenter)
        self.lblIcon.setObjectName("lblIcon")
        self.lblIcon.setStyleSheet(
            '''border-radius:40px;border-image: url(./Avator/{}.png);background-color:gray;background-position:center;'''.format(
                self.Uid))
        self.horizontalLayout.addWidget(self.lblIcon)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(self.content)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("姓 名:")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.txtName = QtWidgets.QLineEdit(self.groupBox)
        self.txtName.setMinimumSize(QtCore.QSize(200, 30))
        self.txtName.setMaximumSize(QtCore.QSize(150, 30))
        self.txtName.setObjectName("txtName")
        self.txtName.setText(user.Name)
        self.txtName.setReadOnly(True)
        self.gridLayout.addWidget(self.txtName, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.label_3.setText("手 机:")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.txtPhone = QtWidgets.QLineEdit(self.groupBox)
        self.txtPhone.setMinimumSize(QtCore.QSize(200, 30))
        self.txtPhone.setMaximumSize(QtCore.QSize(150, 30))
        self.txtPhone.setObjectName("txtPhone")
        self.txtPhone.setText(user.Phone)
        self.gridLayout.addWidget(self.txtPhone, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.lblTitle.setText("修改用户信息")
        self.setContent(self.content)
        self.resize(280, 180)
        self.lblIcon.clicked.connect(self.OnLblIcon_clicked)
        p = "./Avator/{}.png".format(str(self.Uid))
        self.btnOk.clicked.connect(self.OnBtnOkClicked)

    def OnBtnOkClicked(self):
        if self.fileName != "":
            dst = "./Avator/{}.png".format(str(self.Uid))
            shutil.copy(self.fileName, dst)
        User.update({User.Name: self.txtName.text(), User.Phone: self.txtPhone.text()}).where(
            User.Id == self.Uid).execute()
        MessageBoxEx.show("修改成功", "温馨提示", "确认")
        self.notify.emit(self.txtPhone.text())

    def OnLblIcon_clicked(self):
        print(os.path.abspath('.'))
        self.fileName, type = QFileDialog.getOpenFileName(caption='选择头像', filter='(*.png);;All Files (*)')
        if gl.isFileExist(self.fileName) is False:
            return
        self.lblIcon.setStyleSheet(
            '''border-radius:40px;border-image: url({});background-color:gray; background-position:center;'''.format(
                self.fileName))
