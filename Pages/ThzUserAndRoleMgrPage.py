from PyQt5.QtWidgets import *
from Common.UserMgrMenu import MenuQListWidgetItem
from Pages.ThzRoleMgr import ThzRoleMgr
from Pages.ThzUserMgr import ThzUserMgr
from Ui.UiThzUserMgr import Ui_ThzUserMgrCtx


class ThzUserAndRoleMgrPage(QWidget, Ui_ThzUserMgrCtx):
    oldItem = None

    def __init__(self, parent=None):

        super(ThzUserAndRoleMgrPage, self).__init__(parent)
        self.setupUi(self)
        self.retranslateUi(self)

        self.userPage = ThzUserMgr()
        self.rolePage = ThzRoleMgr()
        self.stackedWidgetUser.addWidget(self.userPage)
        self.stackedWidgetUser.addWidget(self.rolePage)
        # 左侧列表切换
        self.listWidget.itemClicked.connect(self.OnListItemClick)

        # 用户管理左侧选择栏
        widget = MenuQListWidgetItem(self)
        widget.setTextUp("用户管理")
        widget.setIcon("./Res/用户角色分配.png")
        item1 = QListWidgetItem()
        item1.setSizeHint(widget.sizeHint())
        self.listWidget.addItem(item1)
        self.listWidget.setItemWidget(item1, widget)
        widget = MenuQListWidgetItem(self)
        widget.setTextUp("角色管理")
        widget.setIcon("./Res/用户角色分配.png")
        item2 = QListWidgetItem()
        item2.setSizeHint(widget.sizeHint())
        self.listWidget.addItem(item2)
        self.listWidget.setItemWidget(item2, widget)

    # 列表点击事件
    def OnListItemClick(self, item):
        t = self.listWidget.itemWidget(item)
        if self.oldItem is not None and self.oldItem is not t:
            t.nameLabel.setStyleSheet('''color:white;''')
            self.oldItem.nameLabel.setStyleSheet('''color:#FF4D4D4D;''')
        else:
            t.nameLabel.setStyleSheet('''color:white;''')
        self.oldItem = t
        if t.nameLabel.text() == "用户管理":
            self.stackedWidgetUser.setCurrentIndex(0)
        else:
            self.stackedWidgetUser.setCurrentIndex(1)
