# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UiThzUserMgr.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ThzUserMgrCtx(object):
    def setupUi(self, ThzUserMgrCtx):
        ThzUserMgrCtx.setObjectName("ThzUserMgrCtx")
        ThzUserMgrCtx.resize(1359, 834)
        ThzUserMgrCtx.setStyleSheet("QGroupBox{background-color:#FFF4F5FA;border:none;}\n"
"QListWidget,QStackedWidget{border:none;}\n"
"QListWidget::item:hover{background-color:#8F00A3DA;color:white;}\n"
"QListWidget::item:selected{background-color:#FF00A3DA;color:white;color:white;}\n"
"QListWidget::item:selected:!active{background-color:#FF00A3DA;color:white;}\n"
"\n"
"\n"
"\n"
"")
        self.horizontalLayout = QtWidgets.QHBoxLayout(ThzUserMgrCtx)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtWidgets.QGroupBox(ThzUserMgrCtx)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(7)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.groupBox_15 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_15.setMaximumSize(QtCore.QSize(285, 16777215))
        self.groupBox_15.setStyleSheet("")
        self.groupBox_15.setTitle("")
        self.groupBox_15.setObjectName("groupBox_15")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_15)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.listWidget = QtWidgets.QListWidget(self.groupBox_15)
        self.listWidget.setMinimumSize(QtCore.QSize(270, 0))
        self.listWidget.setMaximumSize(QtCore.QSize(270, 16777215))
        self.listWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.listWidget.setStyleSheet("")
        self.listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.listWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.listWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_2.addWidget(self.listWidget)
        self.horizontalLayout_10.addWidget(self.groupBox_15)
        self.groupBox_16 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_16.setStyleSheet("")
        self.groupBox_16.setTitle("")
        self.groupBox_16.setObjectName("groupBox_16")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_16)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.stackedWidgetUser = QtWidgets.QStackedWidget(self.groupBox_16)
        self.stackedWidgetUser.setObjectName("stackedWidgetUser")
        self.horizontalLayout_3.addWidget(self.stackedWidgetUser)
        self.horizontalLayout_10.addWidget(self.groupBox_16)
        self.horizontalLayout_2.addLayout(self.horizontalLayout_10)
        self.horizontalLayout.addWidget(self.groupBox)

        self.retranslateUi(ThzUserMgrCtx)
        self.listWidget.setCurrentRow(-1)
        self.stackedWidgetUser.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(ThzUserMgrCtx)

    def retranslateUi(self, ThzUserMgrCtx):
        _translate = QtCore.QCoreApplication.translate
        ThzUserMgrCtx.setWindowTitle(_translate("ThzUserMgrCtx", "Form"))
