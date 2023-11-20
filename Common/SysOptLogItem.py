# 左侧
from PyQt5.Qt import *
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QCheckBox, QGroupBox
from PyQt5 import QtCore


# 设置自定义table表头
class SysOptLogItem(QWidget):
    Id = 0

    def __init__(self, controls, parent=None):
        super(SysOptLogItem, self).__init__(parent)
        self.horizontalLayout = QHBoxLayout()

        # 设置布局用来对nameLabel和avatorLabel进行布局
        self.hbox = QHBoxLayout()
        self.hbox.setContentsMargins(0, 3, 0, 3)
        self.hbox.setSpacing(0)

        self.checkBox = QCheckBox()
        self.checkBox.setLayoutDirection(QtCore.Qt.LeftToRight)

        self.checkBox.setMaximumWidth(controls[1].maximumWidth())
        self.checkBox.setMinimumWidth(controls[1].minimumWidth())
        self.checkBox.setMinimumHeight(controls[1].minimumHeight())
        self.hbox.addWidget(self.checkBox)
        # 名称
        self.lblName = QLabel()
        self.lblName.setMaximumWidth(controls[2].maximumWidth())
        self.lblName.setMinimumWidth(controls[2].minimumWidth())
        self.hbox.addWidget(self.lblName)
        # 类型
        self.lblType = QLabel()
        self.lblType.setMaximumWidth(controls[3].maximumWidth())
        self.lblType.setMinimumWidth(controls[3].minimumWidth())
        self.hbox.addWidget(self.lblType)
        # 日期
        self.lblDate = QLabel()
        self.lblDate.setMaximumWidth(controls[4].maximumWidth())
        self.lblDate.setMinimumWidth(controls[4].minimumWidth())
        self.hbox.addWidget(self.lblDate)
        # 内容
        self.lblContex = QLabel()
        self.lblContex.setMaximumWidth(controls[5].maximumWidth())
        self.lblContex.setMinimumWidth(controls[5].minimumWidth())
        self.hbox.addWidget(self.lblContex)
        self.setLayout(self.hbox)
