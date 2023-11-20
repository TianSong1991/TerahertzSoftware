# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UiUserInfoEdit.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EditForm(object):
    def setupUi(self, EditForm):
        EditForm.setObjectName("EditForm")
        EditForm.resize(400, 300)
        EditForm.setStyleSheet("QGroupBox{border:none;}\n"
"QPushButton,QLabel,QLineEdit{background:transparent;color:white;border:none;}\n"
"QLineEdit{background-color:rgb(50,53,66);}\n"
"QPushButton{color:#FFFFFFFF;border:none;}\n"
"QPushButton:hover{background-color:#FFFF0000; color: #FFFFFFFF;}\n"
"#gbxTop{background-color: rgb(50,53,66);border-left:1px solid gray;border-top:1px solid gray;border-right:1px solid gray;}\n"
"#gbxBottom{background-color: rgb(68,71,86);border-left:1px solid gray;border-bottom:1px solid gray;border-right:1px solid gray;}\n"
"#lblIcon{border-radius:40px;background-color:gray;}\n"
"#btnOk{background-color:#FF4463BE;border:none;}\n"
"#btnOk:hover{background-color: rgb(68, 87, 145); color: #FFFFFFFF;}\n"
"")
        self.verticalLayout = QtWidgets.QVBoxLayout(EditForm)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gbxTop = QtWidgets.QGroupBox(EditForm)
        self.gbxTop.setMinimumSize(QtCore.QSize(0, 50))
        self.gbxTop.setMaximumSize(QtCore.QSize(16777215, 50))
        self.gbxTop.setTitle("")
        self.gbxTop.setObjectName("gbxTop")
        self.btnClose = QtWidgets.QPushButton(self.gbxTop)
        self.btnClose.setGeometry(QtCore.QRect(360, 10, 30, 30))
        self.btnClose.setMinimumSize(QtCore.QSize(30, 30))
        self.btnClose.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Webdings")
        self.btnClose.setFont(font)
        self.btnClose.setObjectName("btnClose")
        self.verticalLayout.addWidget(self.gbxTop)
        self.gbxBottom = QtWidgets.QGroupBox(EditForm)
        self.gbxBottom.setTitle("")
        self.gbxBottom.setAlignment(QtCore.Qt.AlignCenter)
        self.gbxBottom.setObjectName("gbxBottom")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.gbxBottom)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.gbxBottom)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gbxBottom)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 1, 1, 1)
        self.txtName = QtWidgets.QLineEdit(self.gbxBottom)
        self.txtName.setMinimumSize(QtCore.QSize(200, 30))
        self.txtName.setMaximumSize(QtCore.QSize(150, 30))
        self.txtName.setObjectName("txtName")
        self.gridLayout.addWidget(self.txtName, 1, 2, 1, 1)
        self.btnOk = QtWidgets.QPushButton(self.gbxBottom)
        self.btnOk.setMinimumSize(QtCore.QSize(80, 40))
        self.btnOk.setMaximumSize(QtCore.QSize(80, 40))
        self.btnOk.setObjectName("btnOk")
        self.gridLayout.addWidget(self.btnOk, 3, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.txtPhone = QtWidgets.QLineEdit(self.gbxBottom)
        self.txtPhone.setMinimumSize(QtCore.QSize(200, 30))
        self.txtPhone.setMaximumSize(QtCore.QSize(150, 30))
        self.txtPhone.setObjectName("txtPhone")
        self.gridLayout.addWidget(self.txtPhone, 2, 2, 1, 1)
        self.lblIcon = QtWidgets.QLabel(self.gbxBottom)
        self.lblIcon.setMinimumSize(QtCore.QSize(80, 80))
        self.lblIcon.setMaximumSize(QtCore.QSize(80, 80))
        self.lblIcon.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblIcon.setText("")
        self.lblIcon.setAlignment(QtCore.Qt.AlignCenter)
        self.lblIcon.setObjectName("lblIcon")
        self.gridLayout.addWidget(self.lblIcon, 0, 2, 1, 1, QtCore.Qt.AlignHCenter)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 3, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addWidget(self.gbxBottom)

        self.retranslateUi(EditForm)
        QtCore.QMetaObject.connectSlotsByName(EditForm)

    def retranslateUi(self, EditForm):
        _translate = QtCore.QCoreApplication.translate
        EditForm.setWindowTitle(_translate("EditForm", "Form"))
        self.btnClose.setText(_translate("EditForm", "r"))
        self.label_2.setText(_translate("EditForm", "姓    名:"))
        self.label_3.setText(_translate("EditForm", "手机号码:"))
        self.btnOk.setText(_translate("EditForm", "确 定"))