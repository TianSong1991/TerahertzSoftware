from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import QEnterEvent
from PyQt5.QtWidgets import *

from Common.SettingDropListItem import SettingDropListItem
from Ui.UiDropList import Ui_DropBoxForm


class ThzPageDropList(QWidget, Ui_DropBoxForm):
    def __init__(self, parent=None):
        super(ThzPageDropList, self).__init__(parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.InitMenu()
        self.gbxContent.installEventFilter(self)  # 初始化事件过滤器

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Leave or event.type == QEvent.HoverLeave:
            self.setHidden(True)
        return super(ThzPageDropList, self).eventFilter(obj, event)

    def InitMenu(self):
        widget = SettingDropListItem()
        widget.lblName.setText("修改密码")
        widget.lblIcon.setPixmap(QtGui.QPixmap(":/Image/edit.png"))
        widget.lblIcon.setScaledContents(True)
        item = QListWidgetItem()
        item.setSizeHint(widget.sizeHint())
        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item, widget)

        widget = SettingDropListItem()
        widget.lblName.setText("文档帮助")
        widget.lblIcon.setPixmap(QtGui.QPixmap(":/Image/file.png"))
        widget.lblIcon.setScaledContents(True)
        item = QListWidgetItem()
        item.setSizeHint(widget.sizeHint())
        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item, widget)

        widget = SettingDropListItem()
        widget.lblName.setText("退出登录")
        widget.lblIcon.setPixmap(QtGui.QPixmap(":/Image/sign-out.png"))
        widget.lblIcon.setScaledContents(True)
        item = QListWidgetItem()
        item.setSizeHint(widget.sizeHint())
        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item, widget)

    def moveTo(self, x, y):  # 定义一个函数使得窗口居中显示
        self.move(int(x), int(y))
