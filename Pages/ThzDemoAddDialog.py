from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from Common.DemoCategoryItem import PreAddItem, AddedItem
from Common.DialogEx import DialogEx


class DemoCategoryAddForm(DialogEx):
    Id = 0

    def __init__(self):
        super(DemoCategoryAddForm, self).__init__(None)
        self.set1BtnMode()
        self.content = QWidget()
        self.content.setStyleSheet('''
            QGroupBox{border:none;background:transparent;}
            QLabel{background-color:transparent;color:#FF4D4D4D;}
            QPushButton{font-size:10pt;background:transparent;color:#FF4D4D4D;}
            QTreeWidget{background-color:transparent;border:none;color:white;}
            #lblFormName{font-size:14pt;}
            #lblTitle{font-size:10pt;}
            #gbxTop{background-color:#FF00A3DA}
            #gbxContent{background-color:#FFFFFF}
            #gbxClose{background-color:transparent;}
            #gbxContent{border:1px solid gray;}
            #btnClose{border-image: url(./Res/叉.png)}
            #btnCancel,#btnDel{color: rgb(255, 61, 55);}
            #txtName{color:#FF4D4D4D;background-color:transparent;}
            #btnTopItemAdd{background-color:#FF00A3DA;border:none;color:white;}
            #btnTopItemAdd:hover{background-color:#8F00A3DA;}
            
            #btnAddDemoCategory{background-color:#FF00A3DA;border:none;}
            #btnAddDemoCategory:hover{background-color:#8F00A3DA;}
            
            #btnOk{background-color:#FF00A3DA;border:none;}
            #btnOk:hover{background-color:#8F00A3DA;}
            QScrollBar{border:none;background:transparent;}
            QScrollBar:vertical{width:5px;background:transparent;margin:0px,0px,0px,0px;padding-top:0px;padding-bottom:0px;}
            QScrollBar::handle:vertical{width:5px;background:rgba(0,0,0,10%);border-radius:4px;min-height:60;}
            QScrollBar::handle:vertical:hover{width:5px;background:rgba(0,0,0,20%);border-radius:4px;min-height:60;}
            QScrollBar::add-line:vertical{height:0px;width:0px;subcontrol-position:bottom;}
            QScrollBar::sub-line:vertical{height:0px;width:0px;subcontrol-position:top;}
            QScrollBar::add-line:vertical:hover{height:0px;width:0px;subcontrol-position:bottom;}
            QScrollBar::sub-line:vertical:hover{height:0px;width:0px;subcontrol-position:top;}
            QScrollBar::sub-page:vertical{background: none;}
            QScrollBar::add-page:vertical{background: none;}
        ''')
        self.verticalLayout_2 = QVBoxLayout(self.content)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QGroupBox(self.content)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_4.setContentsMargins(0, 0, 9, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(20, 6, 6, 6)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lblSecondTitle = QLabel(self.groupBox)
        self.lblSecondTitle.setMinimumSize(QtCore.QSize(110, 0))
        self.lblSecondTitle.setMaximumSize(QtCore.QSize(110, 16777215))
        self.lblSecondTitle.setObjectName("lblSecondTitle")
        self.lblSecondTitle.setText("样品分类列表")
        self.horizontalLayout_3.addWidget(self.lblSecondTitle)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.btnTopItemAdd = QPushButton(self.groupBox)
        self.btnTopItemAdd.setMinimumSize(QtCore.QSize(80, 30))
        self.btnTopItemAdd.setMaximumSize(QtCore.QSize(80, 30))
        self.btnTopItemAdd.setObjectName("btnTopItemAdd")
        self.btnTopItemAdd.setText("添加")
        self.horizontalLayout_3.addWidget(self.btnTopItemAdd)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_3 = QGroupBox(self.content)
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_5 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_5.setContentsMargins(10, -1, 10, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.treeWidget = QTreeWidget(self.groupBox_3)
        self.treeWidget.setHeaderHidden(True)
        self.treeWidget.setExpandsOnDoubleClick(False)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.horizontalLayout_5.addWidget(self.treeWidget)
        self.verticalLayout_2.addWidget(self.groupBox_3)

        self.lblTitle.setText("样品分类")
        self.setContent(self.content)
        self.resize(500, 500)

    def center(self):  # 定义一个函数使得窗口居中显示
        # 获取屏幕坐标系
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        size = self.geometry()
        newLeft = (screen.width() - size.width()) / 2
        newTop = (screen.height() - size.height()) / 2
        self.move(int(newLeft), int(newTop))
        print("newLeft:", newLeft, " newTop:", newTop)
