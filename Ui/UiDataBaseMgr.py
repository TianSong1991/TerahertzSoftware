# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UiDataBaseMgr.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1269, 703)
        Form.setStyleSheet("QGroupBox{border:none;color:#FF4D4D4D;background-color:#FFFFFF;}\n"
"QListWidget{border:none;background:transparent;}\n"
"QLabel{background:transparent; color:#FF4D4D4D;}\n"
"QCheckBox{background:transparent;margin-left:5px;}\n"
"#gbxLeft{border-right:1px solid gray;}\n"
"#lblTitle{color:#FF4D4D4D;font-size:14pt;}\n"
"#lineSearch{background-color:#FFEBEBEB;color:#FF4D4D4D;border-radius: 15px; border: 2px; padding:0 0 0 10;}\n"
"#btnDemoBatchDel{background-color: rgb(255,62,62);color:white}\n"
"#gbxDemoMgrTableHeader {background-color: #FF00A3DA;}\n"
"#gbxDemoMgrTableHeader QLabel{qproperty-alignment: \'AlignHCenter|AlignVCenter\';font-size:9pt;text-align:left}\n"
"\n"
"QTreeWidget{border:none;background:transparent;color:#FF4D4D4D;}\n"
"QTreeWidget::item {height:32px;}\n"
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
"QListWidget{border:none;background:transparent;}\n"
"QListWidget::item{border-bottom:1px solid black;}\n"
"QListWidget::item .QLabel{qproperty-alignment: \'AlignHCenter|AlignVCenter\';font-size:9pt;text-align:left;}\n"
"QListWidget::item .QPushButton{qproperty-alignment: \' AlignHCenter|AlignVCenter\'; font-size:9pt;}\n"
"\n"
"QCheckBox{background:transparent;}\n"
"QCheckBox::indicator { width: 20px;height: 20px;}\n"
"QCheckBox::indicator:checked { image: url(./Res/checkbox-checked.png); } \n"
"QCheckBox::indicator:unchecked {image: url(./Res/checkbox-unchecked.png);}\n"
"#optView{color:#4454a6;}\n"
"#optExport{color:#0ab363;}\n"
"#optDel{color:#e54356;}\n"
"#optView{background-color: rgb(68,99,190);}\n"
"\n"
"#btnAddDemoCategory{background-color:#FF00A3DA;border:none;color:white}\n"
"#btnAddDemoCategory:hover{background-color:#8F00A3DA;color:white}\n"
"#btnDemoAdd{background-color:#FF00A3DA;border:none;;color:white}\n"
"#btnDemoAdd:hover{background-color:#8F00A3DA;}\n"
"#btnDemoBatchDel{background-color: rgb(255, 2, 2);border:none;color:white;}\n"
"#btnDemoBatchDel:hover{background-color:rgb(255, 111, 92);color:white;}\n"
"\n"
"\n"
"")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 40))
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(14)
        self.groupBox.setFont(font)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setContentsMargins(9, 0, -1, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblTitle = QtWidgets.QLabel(self.groupBox)
        self.lblTitle.setObjectName("lblTitle")
        self.horizontalLayout.addWidget(self.lblTitle)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setContentsMargins(9, 0, 0, -1)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gbxLeft = QtWidgets.QGroupBox(self.groupBox_2)
        self.gbxLeft.setMinimumSize(QtCore.QSize(250, 0))
        self.gbxLeft.setMaximumSize(QtCore.QSize(250, 16777215))
        self.gbxLeft.setStyleSheet("")
        self.gbxLeft.setTitle("")
        self.gbxLeft.setObjectName("gbxLeft")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.gbxLeft)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btnAddDemoCategory = QtWidgets.QPushButton(self.gbxLeft)
        self.btnAddDemoCategory.setMinimumSize(QtCore.QSize(80, 30))
        self.btnAddDemoCategory.setMaximumSize(QtCore.QSize(80, 30))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.btnAddDemoCategory.setFont(font)
        self.btnAddDemoCategory.setObjectName("btnAddDemoCategory")
        self.verticalLayout_2.addWidget(self.btnAddDemoCategory)
        self.treeWidgetDemoCategory = QtWidgets.QTreeWidget(self.gbxLeft)
        self.treeWidgetDemoCategory.setRootIsDecorated(True)
        self.treeWidgetDemoCategory.setHeaderHidden(True)
        self.treeWidgetDemoCategory.setExpandsOnDoubleClick(False)
        self.treeWidgetDemoCategory.setObjectName("treeWidgetDemoCategory")
        self.verticalLayout_2.addWidget(self.treeWidgetDemoCategory)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2.addWidget(self.gbxLeft, 0, QtCore.Qt.AlignLeft)
        self.gbxRight = QtWidgets.QGroupBox(self.groupBox_2)
        self.gbxRight.setEnabled(True)
        self.gbxRight.setStyleSheet("")
        self.gbxRight.setTitle("")
        self.gbxRight.setObjectName("gbxRight")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.gbxRight)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox_12 = QtWidgets.QGroupBox(self.gbxRight)
        self.groupBox_12.setMinimumSize(QtCore.QSize(0, 35))
        self.groupBox_12.setMaximumSize(QtCore.QSize(16777215, 80))
        self.groupBox_12.setTitle("")
        self.groupBox_12.setObjectName("groupBox_12")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout(self.groupBox_12)
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_15.setSpacing(0)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setContentsMargins(9, -1, 30, -1)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_6 = QtWidgets.QLabel(self.groupBox_12)
        self.label_6.setMinimumSize(QtCore.QSize(15, 0))
        self.label_6.setMaximumSize(QtCore.QSize(15, 16777215))
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.gridLayout_4.addWidget(self.label_6, 0, 3, 1, 1)
        self.btnDemoBatchDel = QtWidgets.QPushButton(self.groupBox_12)
        self.btnDemoBatchDel.setMinimumSize(QtCore.QSize(80, 30))
        self.btnDemoBatchDel.setMaximumSize(QtCore.QSize(80, 30))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.btnDemoBatchDel.setFont(font)
        self.btnDemoBatchDel.setStyleSheet("")
        self.btnDemoBatchDel.setObjectName("btnDemoBatchDel")
        self.gridLayout_4.addWidget(self.btnDemoBatchDel, 0, 4, 1, 1)
        self.lineSearch = QtWidgets.QLineEdit(self.groupBox_12)
        self.lineSearch.setMinimumSize(QtCore.QSize(280, 30))
        self.lineSearch.setMaximumSize(QtCore.QSize(280, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lineSearch.setFont(font)
        self.lineSearch.setTabletTracking(False)
        self.lineSearch.setInputMask("")
        self.lineSearch.setMaxLength(32767)
        self.lineSearch.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineSearch.setCursorPosition(0)
        self.lineSearch.setClearButtonEnabled(False)
        self.lineSearch.setObjectName("lineSearch")
        self.gridLayout_4.addWidget(self.lineSearch, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 0, 1, 1, 1)
        self.btnDemoAdd = QtWidgets.QPushButton(self.groupBox_12)
        self.btnDemoAdd.setMinimumSize(QtCore.QSize(80, 30))
        self.btnDemoAdd.setMaximumSize(QtCore.QSize(80, 30))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.btnDemoAdd.setFont(font)
        self.btnDemoAdd.setStyleSheet("")
        self.btnDemoAdd.setObjectName("btnDemoAdd")
        self.gridLayout_4.addWidget(self.btnDemoAdd, 0, 2, 1, 1)
        self.horizontalLayout_15.addLayout(self.gridLayout_4)
        self.verticalLayout_3.addWidget(self.groupBox_12)
        self.groupBox_11 = QtWidgets.QGroupBox(self.gbxRight)
        self.groupBox_11.setStyleSheet("")
        self.groupBox_11.setTitle("")
        self.groupBox_11.setObjectName("groupBox_11")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.groupBox_11)
        self.horizontalLayout_9.setContentsMargins(0, 9, 0, 0)
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
        self.gbxDemoMgrTableHeader = QtWidgets.QGroupBox(self.gbxContent)
        self.gbxDemoMgrTableHeader.setMinimumSize(QtCore.QSize(0, 30))
        self.gbxDemoMgrTableHeader.setMaximumSize(QtCore.QSize(16777215, 30))
        self.gbxDemoMgrTableHeader.setStyleSheet("")
        self.gbxDemoMgrTableHeader.setTitle("")
        self.gbxDemoMgrTableHeader.setObjectName("gbxDemoMgrTableHeader")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.gbxDemoMgrTableHeader)
        self.horizontalLayout_4.setContentsMargins(0, 0, 5, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.chkAll = QtWidgets.QCheckBox(self.gbxDemoMgrTableHeader)
        self.chkAll.setMinimumSize(QtCore.QSize(40, 20))
        self.chkAll.setMaximumSize(QtCore.QSize(40, 20))
        self.chkAll.setSizeIncrement(QtCore.QSize(0, 0))
        self.chkAll.setBaseSize(QtCore.QSize(0, 0))
        self.chkAll.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.chkAll.setStyleSheet("QCheckBox::indicator { width: 20px;height: 20px;}\n"
"QCheckBox::indicator:checked { image: url(./Res/checkbox-checked.png); } QCheckBox::indicator:unchecked {image: url(./Res/checkbox-unchecked.png);}")
        self.chkAll.setText("")
        self.chkAll.setObjectName("chkAll")
        self.horizontalLayout_4.addWidget(self.chkAll)
        self.label_5 = QtWidgets.QLabel(self.gbxDemoMgrTableHeader)
        self.label_5.setMinimumSize(QtCore.QSize(100, 0))
        self.label_5.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_5.setStyleSheet("")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.label_9 = QtWidgets.QLabel(self.gbxDemoMgrTableHeader)
        self.label_9.setMinimumSize(QtCore.QSize(100, 0))
        self.label_9.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_9.setStyleSheet("")
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_4.addWidget(self.label_9)
        self.label_12 = QtWidgets.QLabel(self.gbxDemoMgrTableHeader)
        self.label_12.setMinimumSize(QtCore.QSize(180, 0))
        self.label_12.setMaximumSize(QtCore.QSize(180, 16777215))
        self.label_12.setStyleSheet("")
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_4.addWidget(self.label_12)
        self.label_13 = QtWidgets.QLabel(self.gbxDemoMgrTableHeader)
        self.label_13.setMinimumSize(QtCore.QSize(100, 0))
        self.label_13.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_13.setStyleSheet("")
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_4.addWidget(self.label_13)
        self.lblOpt = QtWidgets.QLabel(self.gbxDemoMgrTableHeader)
        self.lblOpt.setMinimumSize(QtCore.QSize(120, 0))
        self.lblOpt.setMaximumSize(QtCore.QSize(120, 16777215))
        self.lblOpt.setSizeIncrement(QtCore.QSize(0, 0))
        self.lblOpt.setAlignment(QtCore.Qt.AlignCenter)
        self.lblOpt.setObjectName("lblOpt")
        self.horizontalLayout_4.addWidget(self.lblOpt)
        self.verticalLayout_7.addWidget(self.gbxDemoMgrTableHeader)
        self.listWidgetDemo = QtWidgets.QListWidget(self.gbxContent)
        self.listWidgetDemo.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.listWidgetDemo.setStyleSheet("")
        self.listWidgetDemo.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.listWidgetDemo.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listWidgetDemo.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.listWidgetDemo.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.listWidgetDemo.setObjectName("listWidgetDemo")
        self.verticalLayout_7.addWidget(self.listWidgetDemo)
        self.horizontalLayout_19.addLayout(self.verticalLayout_7)
        self.horizontalLayout_9.addWidget(self.gbxContent)
        self.verticalLayout_3.addWidget(self.groupBox_11)
        self.horizontalLayout_2.addWidget(self.gbxRight)
        self.verticalLayout.addWidget(self.groupBox_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lblTitle.setText(_translate("Form", "样品管理"))
        self.btnAddDemoCategory.setText(_translate("Form", "添 加"))
        self.treeWidgetDemoCategory.headerItem().setText(0, _translate("Form", "新建列"))
        self.btnDemoBatchDel.setText(_translate("Form", "批量删除"))
        self.lineSearch.setPlaceholderText(_translate("Form", "搜索条件 "))
        self.btnDemoAdd.setText(_translate("Form", "添加"))
        self.label_5.setText(_translate("Form", "样品号"))
        self.label_9.setText(_translate("Form", "样品名称"))
        self.label_12.setText(_translate("Form", "创建时间"))
        self.label_13.setText(_translate("Form", "备注"))
        self.lblOpt.setText(_translate("Form", "操作"))