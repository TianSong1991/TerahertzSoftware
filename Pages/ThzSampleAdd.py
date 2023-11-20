from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from Common.DialogEx import DialogEx


class ThzSampleAdd(DialogEx):
    def __init__(self):
        super(ThzSampleAdd, self).__init__(None)
        self.content = QWidget()
        self.content.setStyleSheet('''
            QGroupBox{border:none;}
            QPushButton{background:transparent;}
            QLineEdit,QPlainTextEdit{background-color: rgb(50, 53, 66);color:white;border:none;}
        ''')
        self.set1BtnMode()
        self.horizontalLayout_6 = QHBoxLayout(self.content)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.gbxContent = QGroupBox(self.content)
        self.gbxContent.setTitle("")
        self.gbxContent.setObjectName("gbxContent")
        self.verticalLayout = QVBoxLayout(self.gbxContent)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gbxBottom = QGroupBox(self.gbxContent)
        self.gbxBottom.setTitle("")
        self.gbxBottom.setObjectName("gbxBottom")
        self.verticalLayout_2 = QVBoxLayout(self.gbxBottom)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_3 = QGroupBox(self.gbxBottom)
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setContentsMargins(-1, 0, -1, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QLabel(self.groupBox_3)
        self.label.setMaximumSize(QtCore.QSize(80, 32))
        self.label.setObjectName("label")
        self.label.setText("样品编号:")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.txtSampleNo = QLineEdit(self.groupBox_3)
        self.txtSampleNo.setMinimumSize(QtCore.QSize(230, 30))
        self.txtSampleNo.setMaximumSize(QtCore.QSize(230, 32))
        self.txtSampleNo.setObjectName("txtSampleNo")
        self.gridLayout.addWidget(self.txtSampleNo, 0, 1, 1, 1)
        self.label_2 = QLabel(self.groupBox_3)
        self.label_2.setMaximumSize(QtCore.QSize(80, 32))
        self.label_2.setObjectName("label_2")
        self.label_2.setText("样品名称:")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.txtSampleName = QLineEdit(self.groupBox_3)
        self.txtSampleName.setMinimumSize(QtCore.QSize(230, 30))
        self.txtSampleName.setMaximumSize(QtCore.QSize(230, 32))
        self.txtSampleName.setObjectName("txtSampleName")
        self.gridLayout.addWidget(self.txtSampleName, 1, 1, 1, 1)
        self.label_3 = QLabel(self.groupBox_3)
        self.label_3.setMaximumSize(QtCore.QSize(80, 32))
        self.label_3.setObjectName("label_3")
        self.label_3.setText("样品文件:")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.txtSampleFile = QLineEdit(self.groupBox_3)
        self.txtSampleFile.setMinimumSize(QtCore.QSize(230, 30))
        self.txtSampleFile.setMaximumSize(QtCore.QSize(230, 32))
        self.txtSampleFile.setObjectName("txtSampleFile")
        self.gridLayout.addWidget(self.txtSampleFile, 2, 1, 1, 1)
        self.label_4 = QLabel(self.groupBox_3)
        self.label_4.setMaximumSize(QtCore.QSize(80, 32))
        self.label_4.setObjectName("label_4")
        self.label_4.setText("备     注:")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.txtSampleComment = QPlainTextEdit(self.groupBox_3)
        self.txtSampleComment.setMinimumSize(QtCore.QSize(230, 120))
        self.txtSampleComment.setMaximumSize(QtCore.QSize(230, 120))

        self.txtSampleComment.setObjectName("txtSampleComment")
        self.gridLayout.addWidget(self.txtSampleComment, 3, 1, 1, 1)
        self.btnOpenFile = QPushButton(self.groupBox_3)
        self.btnOpenFile.setMinimumSize(QtCore.QSize(20, 17))
        self.btnOpenFile.setMaximumSize(QtCore.QSize(20, 17))
        self.btnOpenFile.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Image/folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnOpenFile.setIcon(icon)
        self.btnOpenFile.setObjectName("btnOpenFile")
        self.gridLayout.addWidget(self.btnOpenFile, 2, 2, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.verticalLayout_2.addWidget(self.groupBox_3)
        self.verticalLayout.addWidget(self.gbxBottom)
        self.horizontalLayout_6.addWidget(self.gbxContent)

        self.lblTitle.setText("添加样品")
        self.setContent(self.content)
        self.resize(450, 350)

    def OnClose(self):
        self.close()

    def center(self):  # 定义一个函数使得窗口居中显示
        # 获取屏幕坐标系
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        size = self.geometry()
        newLeft = (screen.width() - size.width()) / 2
        newTop = (screen.height() - size.height()) / 2
        self.move(int(newLeft), int(newTop))
        print("newLeft:", newLeft, " newTop:", newTop)
