# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UiSystemSettingCfgMgr.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1269, 704)
        Form.setStyleSheet(".QGroupBox{border:none;color:white;background-color:#FFFFFF;}\n"
".QPushButton{font-family:\"宋体\";font-size:11pt;color:white;background:transparent;}\n"
".QLabel{color:white;background:transparent;}\n"
".QCheckBox{background:transparent;}\n"
".QListWidget{border:none;background:transparent;}\n"
"#btnCfgImport{background-color: rgb(68,99,190);}\n"
"#btnCfgExport{background-color: rgb(255,62,62);}\n"
"#gbxSysCfgTableHeader{background-color: #323542;}\n"
"#gbxSysCfgTableHeader QLabel{qproperty-alignment: \'AlignHCenter|AlignVCenter\';font-size:9pt;text-align:left}\n"
"\n"
"QListWidget{border:none;background:transparent;}\n"
"QListWidget::item{border-bottom:1px solid black;}\n"
"QListWidget::item .QLabel{qproperty-alignment: \'AlignHCenter|AlignVCenter\';font-size:9pt;text-align:left;}\n"
"QListWidget::item .QPushButton{qproperty-alignment: \' AlignHCenter|AlignVCenter\'; font-size:9pt;}\n"
"QScrollBar{border:none;background:transparent;}\n"
"QScrollBar:vertical {width: 5px;}\n"
"QScrollBar:vertical{width:5px;background:#FFFFFF; margin:0px,0px,0px,0px;padding-top:0px;padding-bottom:0px;}\n"
"QScrollBar::handle:vertical{width:5px;background:transparent;border-radius:4px;min-height:60;}\n"
"QScrollBar::handle:vertical:hover{width:5px;background:rgba(0,0,0,20%);border-radius:4px;min-height:60;}\n"
"QScrollBar::add-line:vertical{height:0px;width:0px;subcontrol-position:bottom;}\n"
"QScrollBar::sub-line:vertical{height:0px;width:0px;subcontrol-position:top;}\n"
"QScrollBar::add-line:vertical:hover{height:0px;width:0px;subcontrol-position:bottom;}\n"
"QScrollBar::sub-line:vertical:hover{height:0px;width:0px;subcontrol-position:top;}\n"
"QScrollBar::sub-page:vertical{background: none;}\n"
"QScrollBar::add-page:vertical{background: none;}\n"
"\n"
"QCheckBox{background:transparent;}\n"
"QCheckBox::indicator { width: 20px;height: 20px;}\n"
"QCheckBox::indicator:checked { image: url(./Res/checkbox-checked.png); } \n"
"QCheckBox::indicator:unchecked {image: url(./Res/checkbox-unchecked.png);}\n"
"#optExport{color:#0ab363;}\n"
"\n"
"")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_12 = QtWidgets.QGroupBox(Form)
        self.groupBox_12.setMinimumSize(QtCore.QSize(0, 80))
        self.groupBox_12.setMaximumSize(QtCore.QSize(16777215, 80))
        self.groupBox_12.setTitle("")
        self.groupBox_12.setObjectName("groupBox_12")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout(self.groupBox_12)
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_15.setSpacing(0)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setContentsMargins(9, -1, 30, 10)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_4 = QtWidgets.QLabel(self.groupBox_12)
        self.label_4.setMinimumSize(QtCore.QSize(0, 40))
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("")
        self.label_4.setObjectName("label_4")
        self.gridLayout_4.addWidget(self.label_4, 0, 0, 1, 1)
        self.btnCfgImport = QtWidgets.QPushButton(self.groupBox_12)
        self.btnCfgImport.setMinimumSize(QtCore.QSize(80, 30))
        self.btnCfgImport.setMaximumSize(QtCore.QSize(80, 30))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.btnCfgImport.setFont(font)
        self.btnCfgImport.setStyleSheet("")
        self.btnCfgImport.setObjectName("btnCfgImport")
        self.gridLayout_4.addWidget(self.btnCfgImport, 1, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 1, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox_12)
        self.label_6.setMinimumSize(QtCore.QSize(15, 0))
        self.label_6.setMaximumSize(QtCore.QSize(15, 16777215))
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.gridLayout_4.addWidget(self.label_6, 1, 3, 1, 1)
        self.btnCfgExport = QtWidgets.QPushButton(self.groupBox_12)
        self.btnCfgExport.setMinimumSize(QtCore.QSize(80, 30))
        self.btnCfgExport.setMaximumSize(QtCore.QSize(80, 30))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.btnCfgExport.setFont(font)
        self.btnCfgExport.setStyleSheet("")
        self.btnCfgExport.setObjectName("btnCfgExport")
        self.gridLayout_4.addWidget(self.btnCfgExport, 1, 4, 1, 1)
        self.horizontalLayout_15.addLayout(self.gridLayout_4)
        self.verticalLayout.addWidget(self.groupBox_12)
        self.groupBox_11 = QtWidgets.QGroupBox(Form)
        self.groupBox_11.setStyleSheet("")
        self.groupBox_11.setTitle("")
        self.groupBox_11.setObjectName("groupBox_11")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.groupBox_11)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.gbxContent = QtWidgets.QGroupBox(self.groupBox_11)
        self.gbxContent.setStyleSheet("")
        self.gbxContent.setTitle("")
        self.gbxContent.setObjectName("gbxContent")
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout(self.gbxContent)
        self.horizontalLayout_19.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_19.setSpacing(0)
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.gbxSysCfgTableHeader = QtWidgets.QGroupBox(self.gbxContent)
        self.gbxSysCfgTableHeader.setMinimumSize(QtCore.QSize(0, 30))
        self.gbxSysCfgTableHeader.setMaximumSize(QtCore.QSize(16777215, 30))
        self.gbxSysCfgTableHeader.setStyleSheet("")
        self.gbxSysCfgTableHeader.setTitle("")
        self.gbxSysCfgTableHeader.setObjectName("gbxSysCfgTableHeader")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.gbxSysCfgTableHeader)
        self.horizontalLayout.setContentsMargins(0, 0, 5, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.chkAll = QtWidgets.QCheckBox(self.gbxSysCfgTableHeader)
        self.chkAll.setMinimumSize(QtCore.QSize(40, 20))
        self.chkAll.setMaximumSize(QtCore.QSize(40, 20))
        self.chkAll.setSizeIncrement(QtCore.QSize(0, 0))
        self.chkAll.setBaseSize(QtCore.QSize(0, 0))
        self.chkAll.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.chkAll.setStyleSheet("")
        self.chkAll.setText("")
        self.chkAll.setObjectName("chkAll")
        self.horizontalLayout.addWidget(self.chkAll, 0, QtCore.Qt.AlignVCenter)
        self.label_5 = QtWidgets.QLabel(self.gbxSysCfgTableHeader)
        self.label_5.setMinimumSize(QtCore.QSize(200, 0))
        self.label_5.setMaximumSize(QtCore.QSize(200, 16777215))
        self.label_5.setStyleSheet("")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.label_9 = QtWidgets.QLabel(self.gbxSysCfgTableHeader)
        self.label_9.setMinimumSize(QtCore.QSize(100, 0))
        self.label_9.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_9.setStyleSheet("")
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout.addWidget(self.label_9)
        self.label_13 = QtWidgets.QLabel(self.gbxSysCfgTableHeader)
        self.label_13.setMinimumSize(QtCore.QSize(400, 0))
        self.label_13.setMaximumSize(QtCore.QSize(400, 16777215))
        self.label_13.setStyleSheet("")
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout.addWidget(self.label_13)
        self.lblOpt = QtWidgets.QLabel(self.gbxSysCfgTableHeader)
        self.lblOpt.setMinimumSize(QtCore.QSize(180, 0))
        self.lblOpt.setMaximumSize(QtCore.QSize(180, 16777215))
        self.lblOpt.setSizeIncrement(QtCore.QSize(0, 0))
        self.lblOpt.setAlignment(QtCore.Qt.AlignCenter)
        self.lblOpt.setObjectName("lblOpt")
        self.horizontalLayout.addWidget(self.lblOpt)
        self.verticalLayout_7.addWidget(self.gbxSysCfgTableHeader)
        self.listWidgetSysCfg = QtWidgets.QListWidget(self.gbxContent)
        self.listWidgetSysCfg.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.listWidgetSysCfg.setStyleSheet("")
        self.listWidgetSysCfg.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.listWidgetSysCfg.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listWidgetSysCfg.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.listWidgetSysCfg.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.listWidgetSysCfg.setObjectName("listWidgetSysCfg")
        self.verticalLayout_7.addWidget(self.listWidgetSysCfg)
        self.horizontalLayout_19.addLayout(self.verticalLayout_7)
        self.horizontalLayout_9.addWidget(self.gbxContent)
        self.verticalLayout.addWidget(self.groupBox_11)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_4.setText(_translate("Form", "系统配置文件管理"))
        self.btnCfgImport.setText(_translate("Form", "导入"))
        self.btnCfgExport.setText(_translate("Form", "批量导出"))
        self.label_5.setText(_translate("Form", "名称"))
        self.label_9.setText(_translate("Form", "文件类型"))
        self.label_13.setText(_translate("Form", "备注"))
        self.lblOpt.setText(_translate("Form", "操作"))
