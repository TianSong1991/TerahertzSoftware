# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UiDevGp.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1164, 722)
        Form.setStyleSheet("QGroupBox,QLabel{background-color: #FFFFFFFF;    border:none;}\n"
".QLabel{ color:#FF4D4D4D; background-color: transparent;}\n"
".QComboBox{    background-color: #FFEBEBEB; color:#FF4D4D4D;    border:none;}\n"
".QLineEdit{background-color:#FFEBEBEB;border:none;}\n"
"#gbxJgq QLabel{ font-family:\"宋体\"; font-size:11pt; }\n"
"#gbxPyy QLabel{ font-family:\"宋体\"; font-size:11pt; }\n"
"#gbxSxfdq QLabel{ font-family:\"宋体\"; font-size:11pt; }")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(15)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_5 = QtWidgets.QGroupBox(Form)
        self.groupBox_5.setMinimumSize(QtCore.QSize(250, 300))
        self.groupBox_5.setStyleSheet("")
        self.groupBox_5.setTitle("")
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_9 = QtWidgets.QLabel(self.groupBox_5)
        self.label_9.setMinimumSize(QtCore.QSize(0, 35))
        self.label_9.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(14)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_6.addWidget(self.label_9)
        self.gbxPi = QtWidgets.QGroupBox(self.groupBox_5)
        self.gbxPi.setTitle("")
        self.gbxPi.setObjectName("gbxPi")
        self.verticalLayout_6.addWidget(self.gbxPi)
        self.gridLayout.addWidget(self.groupBox_5, 1, 1, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setMinimumSize(QtCore.QSize(250, 300))
        self.groupBox_2.setStyleSheet("")
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setMinimumSize(QtCore.QSize(0, 35))
        self.label_7.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(14)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_3.addWidget(self.label_7)
        self.gbxPyy = QtWidgets.QGroupBox(self.groupBox_2)
        self.gbxPyy.setTitle("")
        self.gbxPyy.setObjectName("gbxPyy")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gbxPyy)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_15 = QtWidgets.QLabel(self.gbxPyy)
        self.label_15.setObjectName("label_15")
        self.gridLayout_3.addWidget(self.label_15, 0, 0, 1, 1)
        self.btnBaisSrc = QtWidgets.QPushButton(self.gbxPyy)
        self.btnBaisSrc.setEnabled(False)
        self.btnBaisSrc.setMinimumSize(QtCore.QSize(166, 0))
        self.btnBaisSrc.setMaximumSize(QtCore.QSize(166, 40))
        self.btnBaisSrc.setStyleSheet("")
        self.btnBaisSrc.setCheckable(True)
        self.btnBaisSrc.setObjectName("btnBaisSrc")
        self.gridLayout_3.addWidget(self.btnBaisSrc, 0, 1, 1, 1)
        self.verticalLayout_3.addWidget(self.gbxPyy, 0, QtCore.Qt.AlignHCenter)
        self.gridLayout.addWidget(self.groupBox_2, 0, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setMinimumSize(QtCore.QSize(250, 300))
        self.groupBox.setStyleSheet("")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setMinimumSize(QtCore.QSize(0, 35))
        self.label_8.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(14)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_2.addWidget(self.label_8)
        self.gbxJgq = QtWidgets.QGroupBox(self.groupBox)
        self.gbxJgq.setMaximumSize(QtCore.QSize(300, 16777215))
        self.gbxJgq.setTitle("")
        self.gbxJgq.setObjectName("gbxJgq")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gbxJgq)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.gbxJgq)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.txtPort = QtWidgets.QLineEdit(self.gbxJgq)
        self.txtPort.setMaximumSize(QtCore.QSize(16777215, 35))
        self.txtPort.setObjectName("txtPort")
        self.gridLayout_2.addWidget(self.txtPort, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gbxJgq)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 1, 0, 1, 1)
        self.txtHz = QtWidgets.QLineEdit(self.gbxJgq)
        self.txtHz.setMaximumSize(QtCore.QSize(16777215, 35))
        self.txtHz.setObjectName("txtHz")
        self.gridLayout_2.addWidget(self.txtHz, 1, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.gbxJgq)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 2, 0, 1, 1)
        self.btnLaser = QtWidgets.QPushButton(self.gbxJgq)
        self.btnLaser.setMaximumSize(QtCore.QSize(16777215, 40))
        self.btnLaser.setCheckable(True)
        self.btnLaser.setObjectName("btnLaser")
        self.gridLayout_2.addWidget(self.btnLaser, 2, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.gbxJgq, 0, QtCore.Qt.AlignHCenter)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_4 = QtWidgets.QGroupBox(Form)
        self.groupBox_4.setMinimumSize(QtCore.QSize(250, 300))
        self.groupBox_4.setStyleSheet("")
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_5 = QtWidgets.QLabel(self.groupBox_4)
        self.label_5.setMinimumSize(QtCore.QSize(0, 35))
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_5.addWidget(self.label_5)
        self.gbxYcx = QtWidgets.QGroupBox(self.groupBox_4)
        self.gbxYcx.setTitle("")
        self.gbxYcx.setObjectName("gbxYcx")
        self.verticalLayout_5.addWidget(self.gbxYcx)
        self.gridLayout.addWidget(self.groupBox_4, 1, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setMinimumSize(QtCore.QSize(400, 300))
        self.groupBox_3.setMaximumSize(QtCore.QSize(16777215, 300))
        self.groupBox_3.setStyleSheet("")
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_6 = QtWidgets.QLabel(self.groupBox_3)
        self.label_6.setMinimumSize(QtCore.QSize(0, 35))
        self.label_6.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(14)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_4.addWidget(self.label_6)
        self.gbxSxfdq = QtWidgets.QGroupBox(self.groupBox_3)
        self.gbxSxfdq.setTitle("")
        self.gbxSxfdq.setObjectName("gbxSxfdq")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.gbxSxfdq)
        self.gridLayout_5.setHorizontalSpacing(15)
        self.gridLayout_5.setVerticalSpacing(20)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.txtTime = QtWidgets.QLineEdit(self.gbxSxfdq)
        self.txtTime.setMinimumSize(QtCore.QSize(150, 35))
        self.txtTime.setMaximumSize(QtCore.QSize(150, 35))
        self.txtTime.setObjectName("txtTime")
        self.gridLayout_5.addWidget(self.txtTime, 0, 1, 1, 1)
        self.lblMin = QtWidgets.QLabel(self.gbxSxfdq)
        self.lblMin.setObjectName("lblMin")
        self.gridLayout_5.addWidget(self.lblMin, 1, 2, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.gbxSxfdq)
        self.label_16.setObjectName("label_16")
        self.gridLayout_5.addWidget(self.label_16, 0, 0, 1, 1)
        self.lblXw = QtWidgets.QLabel(self.gbxSxfdq)
        self.lblXw.setObjectName("lblXw")
        self.gridLayout_5.addWidget(self.lblXw, 1, 0, 1, 1)
        self.txtPhase = QtWidgets.QLineEdit(self.gbxSxfdq)
        self.txtPhase.setMinimumSize(QtCore.QSize(150, 35))
        self.txtPhase.setMaximumSize(QtCore.QSize(150, 35))
        self.txtPhase.setObjectName("txtPhase")
        self.gridLayout_5.addWidget(self.txtPhase, 1, 1, 1, 1)
        self.slider = QtWidgets.QSlider(self.gbxSxfdq)
        self.slider.setMinimumSize(QtCore.QSize(150, 0))
        self.slider.setMaximumSize(QtCore.QSize(150, 16777215))
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setObjectName("slider")
        self.gridLayout_5.addWidget(self.slider, 1, 3, 1, 1)
        self.lblMax = QtWidgets.QLabel(self.gbxSxfdq)
        self.lblMax.setObjectName("lblMax")
        self.gridLayout_5.addWidget(self.lblMax, 1, 4, 1, 1)
        self.verticalLayout_4.addWidget(self.gbxSxfdq, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.gridLayout.addWidget(self.groupBox_3, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_9.setText(_translate("Form", "PI高精度延迟线"))
        self.label_7.setText(_translate("Form", "偏压源"))
        self.label_15.setText(_translate("Form", "偏 压 源:"))
        self.btnBaisSrc.setText(_translate("Form", "开  启"))
        self.label_8.setText(_translate("Form", "激光器"))
        self.label.setText(_translate("Form", "串        口:"))
        self.label_4.setText(_translate("Form", "频率(Hz):"))
        self.label_10.setText(_translate("Form", "硬件开关:"))
        self.btnLaser.setText(_translate("Form", "开  启"))
        self.label_5.setText(_translate("Form", "GP延迟线"))
        self.label_6.setText(_translate("Form", "锁相放大器"))
        self.lblMin.setText(_translate("Form", "0"))
        self.label_16.setText(_translate("Form", "积分时间:"))
        self.lblXw.setText(_translate("Form", "相    位:"))
        self.lblMax.setText(_translate("Form", "360"))