# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UiSysSettingPage.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1197, 781)
        Form.setStyleSheet("QGroupBox,QListWidget,QStackedWidget{background-color: #FFF4F5FA;border:none;}\n"
"LeftNavButton{background-color: #FFFFFF;border:none;}\n"
"LeftNavButton>QLabel{color:#FF4D4D4D;font-family:\"宋体\";margin-left:10px;font-size:12pt;}\n"
"LeftNavSubButton{background-color: #FFFFFF;border:none;}\n"
"LeftNavSubButton>QLabel{color:#FF4D4D4D;font-family:\"宋体\";margin-left:10px;font-size:12pt;}\n"
"QLabel,QPushButton{color:#FF4D4D4D;border:none;}\n"
"\n"
"QPushButton:hover{background-color:#8F00A3DA;}\n"
"QPushButton:pressed{background-color:#FF00A3DA;}\n"
"QPushButton:checked{background-color:#FF00A3DA;}\n"
"\n"
"/*背景*/\n"
"#gbxBackGround{background-color: #FFF4FAF5;}\n"
"#gbxLeft,#gbxRight{background-color: #FFFFFF;}\n"
"#gbxPg1,#gbxPg2{background-color: #FFFFFF;}\n"
"\n"
"\n"
"\n"
"")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gbxBackGround = QtWidgets.QGroupBox(Form)
        self.gbxBackGround.setTitle("")
        self.gbxBackGround.setObjectName("gbxBackGround")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.gbxBackGround)
        self.horizontalLayout_3.setContentsMargins(9, 9, 9, 9)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(15)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gbxLeft = QtWidgets.QWidget(self.gbxBackGround)
        self.gbxLeft.setMinimumSize(QtCore.QSize(270, 0))
        self.gbxLeft.setMaximumSize(QtCore.QSize(270, 16777215))
        self.gbxLeft.setObjectName("gbxLeft")
        self.horizontalLayout_2.addWidget(self.gbxLeft)
        self.gbxRight = QtWidgets.QGroupBox(self.gbxBackGround)
        self.gbxRight.setTitle("")
        self.gbxRight.setObjectName("gbxRight")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.gbxRight)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.stackedWidget = QtWidgets.QStackedWidget(self.gbxRight)
        self.stackedWidget.setObjectName("stackedWidget")
        self.horizontalLayout_4.addWidget(self.stackedWidget)
        self.horizontalLayout_2.addWidget(self.gbxRight)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addWidget(self.gbxBackGround)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
