# 左侧
from PyQt5 import QtCore
from PyQt5.Qt import *
from PyQt5.QtWidgets import QLabel, QHBoxLayout


class LeftNavButton(QPushButton):
    def __init__(self, parent=None):
        super(LeftNavButton, self).__init__(parent)
        self.lblImgLeft = QLabel()
        self.lblImgLeft.setObjectName("LeftNavButtonLeftIcon")
        self.lblImgLeft.setMaximumWidth(25)
        self.lblImgLeft.setMinimumWidth(25)
        self.lblImgLeft.setMaximumHeight(25)
        self.lblImgLeft.setMinimumHeight(25)
        self.lblImgLeft.setScaledContents(True)
        self.lblText = QLabel()
        self.lblText.setObjectName("LeftNavButtonText")
        self.lblImgRight = QLabel()
        self.lblImgRight.setObjectName("LeftNavButtonRightIcon")
        self.lblImgRight.setMaximumWidth(25)
        self.lblImgRight.setMinimumWidth(25)
        self.lblImgRight.setMaximumHeight(25)
        self.lblImgRight.setMinimumHeight(25)
        self.lblImgRight.setScaledContents(True)
        # self.lblImgLeft.setStyleSheet('''background:transparent;''')
        # self.lblImgRight.setStyleSheet('''background:transparent;''')
        # self.lblText.setStyleSheet('''background:transparent;''')
        self.hlayout = QHBoxLayout()
        self.hlayout.setSpacing(0)
        self.hlayout.setContentsMargins(10, 0, 0, 0)
        self.hlayout.addWidget(self.lblImgLeft)
        self.hlayout.addWidget(self.lblText)
        self.hlayout.addWidget(self.lblImgRight)
        self.setLayoutDirection(Qt.LeftToRight)
        self.setLayout(self.hlayout)

    # 设置左边icon属性
    def LeftIcon(self, iconPath):
        self.lblImgLeft.setPixmap(QPixmap(iconPath))
        self.lblImgLeft.setMinimumWidth(35)
        self.lblImgLeft.setScaledContents(True)

    def RightIcon(self, iconPath):
        self.lblImgRight.setPixmap(QPixmap(iconPath))
        self.lblImgRight.setMinimumWidth(35)
        self.lblImgRight.setScaledContents(True)

    def Text(self, txt):
        self.lblText.setText(txt)


class LeftNavSubButton(QPushButton):
    def __init__(self, parent=None):
        super(LeftNavSubButton, self).__init__(parent)
        self.lblImgLeft = QLabel()
        self.lblImgLeft.setObjectName("LeftNavSubButtonLeftIcon")
        self.lblImgLeft.setMaximumWidth(25)
        self.lblImgLeft.setMinimumWidth(25)
        self.lblImgLeft.setMaximumHeight(25)
        self.lblImgLeft.setMinimumHeight(25)
        self.lblImgLeft.setScaledContents(True)
        self.lblText = QLabel()
        self.lblText.setObjectName("LeftNavSubButtonText")
        self.lblImgRight = QLabel()
        self.lblImgRight.setMaximumWidth(25)
        self.lblImgRight.setMinimumWidth(25)
        self.lblImgRight.setMaximumHeight(25)
        self.lblImgRight.setMinimumHeight(25)
        self.lblImgRight.setScaledContents(True)
        self.lblImgRight.setObjectName("LeftNavSubButtonRightIcon")
        # self.lblImgLeft.setStyleSheet('''background:transparent;''')
        # self.lblImgRight.setStyleSheet('''background:transparent;''')
        # self.lblText.setStyleSheet('''background:transparent;''')
        self.hlayout = QHBoxLayout()
        self.hlayout.setSpacing(0)
        self.hlayout.setContentsMargins(40, 0, 0, 0)
        self.hlayout.addWidget(self.lblImgLeft)
        self.hlayout.addWidget(self.lblText)
        self.hlayout.addWidget(self.lblImgRight)
        self.setLayout(self.hlayout)

        # 设置左边icon属性

    def LeftIcon(self, iconPath):
        self.lblImgLeft.setPixmap(QPixmap(iconPath))
        self.lblImgLeft.setMinimumWidth(35)
        self.lblImgLeft.setScaledContents(True)

    def RightIcon(self, iconPath):
        self.lblImgRight.setPixmap(QPixmap(iconPath))
        self.lblImgRight.setMinimumWidth(35)
        self.lblImgRight.setScaledContents(True)

    def Text(self, txt):
        self.lblText.setText(txt)
