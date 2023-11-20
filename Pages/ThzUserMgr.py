from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from peewee import SQL

from Common.MessageBoxEx import MessageBoxEx
from Common.UserTableItem import UserTableItem
from Core.StringHelper import FixString
from Entity.models import Role, User
from Pages.ThzUserAddDialog import UserAddDialogForm
from Ui.UiUserMgr import Ui_UiUserMgrForm


class ThzUserMgr(QWidget, Ui_UiUserMgrForm):
    def __init__(self, parent=None):
        super(ThzUserMgr, self).__init__(parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.userAddDialog = UserAddDialogForm()
        self.userAddDialog.hide()
        # 加载数据
        self.LoadUserInfo()
        self.searchAction = QAction(self.lineSearch)
        self.searchAction.setIcon(QIcon('./Res/search.png'))
        self.searchAction.triggered.connect(self.OnSearch)
        self.lineSearch.addAction(self.searchAction, QLineEdit.TrailingPosition)
        self.lineSearch.textChanged.connect(self.OnSearch)
        # 选择全部
        self.chkAll.clicked.connect(lambda: self.OnCheckAllClicked(self.chkAll.isChecked()))
        # 批量删除
        self.btnUserDel.clicked.connect(self.OnDelManyClick)
        # 用户管理添加删除功能
        self.btnUserAdd.clicked.connect(self.OnBtnUserAddClicked)
        # 用户增加弹出窗口事件绑定
        self.userAddDialog.btnOk.clicked.connect(self.OnUserAddDialogBtnUserAddClicked)

    def OnSearch(self):
        print("search:", self.lineSearch.text())
        result = User.select().where(SQL("Name like '%{}%'".format(self.lineSearch.text())))
        self.listWidgetUser.clear()
        for user in result:
            print(user)
            self.AddUserInfoItem(user)

    # 用户管理添加按钮响应
    def OnBtnUserAddClicked(self):
        self.userAddDialog.Clear()
        self.userAddDialog.show()

    def OnDelManyClick(self):
        count = self.listWidgetUser.count()
        items = []
        for i in range(count):
            item = self.listWidgetUser.item(i)
            widget = self.listWidgetUser.itemWidget(item)
            if widget.checkBox.isChecked():
                u = User()
                u.delete_by_id(widget.Id)
                items.append(item)

        for it in items:
            self.listWidgetUser.takeItem(self.listWidgetUser.row(it))
            self.listWidgetUser.removeItemWidget(it)

    def OnCheckAllClicked(self, isChecked):
        count = self.listWidgetUser.count()
        # 遍历listwidget中的内容
        for i in range(count):
            widget = self.listWidgetUser.itemWidget(self.listWidgetUser.item(i))
            widget.checkBox.setChecked(isChecked)

    def OnUserAddDialogBtnUserAddClicked(self):
        if self.userAddDialog.lblTitle.text() == "添加用户":
            u = User()
            idx = self.userAddDialog.cbxRole.currentIndex()
            r = self.userAddDialog.cbxRole.itemData(idx)
            u.Id = u.create(Name=self.userAddDialog.txtUserName.text(),
                            Phone=self.userAddDialog.txtPhone.text(),
                            Role=r.Name,
                            RoleId=r.Id,
                            Comment=self.userAddDialog.txtComment.toPlainText())
            u.Name = self.userAddDialog.txtUserName.text()
            u.Phone = self.userAddDialog.txtPhone.text()
            u.Role = self.userAddDialog.cbxRole.itemData(idx).Name
            u.Comment = self.userAddDialog.txtComment.toPlainText()
            u.RoleId = r.Id
            self.AddUserInfoItem(u)
        else:
            idx = self.userAddDialog.cbxRole.currentIndex()
            User.update({User.Name: self.userAddDialog.txtUserName.text(),
                         User.Comment: self.userAddDialog.txtComment.toPlainText()}).where(
                User.Id == self.userAddDialog.Id).execute()
            widget = self.listWidgetUser.itemWidget(self.listWidgetUser.item(self.userAddDialog.Row))
            widget.nameLabel.setText(self.userAddDialog.txtUserName.text())
            widget.commentLabel.setText(self.userAddDialog.txtComment.toPlainText())
            widget.roleLabel.setText(self.userAddDialog.cbxRole.currentText())
            widget.phoneLabel.setText(self.userAddDialog.txtPhone.text())
            FixString(widget.nameLabel)

        self.userAddDialog.close()

    def AddUserInfoItem(self, user):
        widget = UserTableItem(self.gbxUserTableHeader.children())
        widget.nameLabel.setText(user.Name)
        FixString(widget.nameLabel)
        widget.phoneLabel.setText(user.Phone)
        FixString(widget.phoneLabel)
        widget.roleLabel.setText(user.Role)
        FixString(widget.roleLabel)
        widget.commentLabel.setText(user.Comment)
        FixString(widget.commentLabel)
        widget.Id = user.Id
        widget.RoleId = user.RoleId
        item = QListWidgetItem()
        item.setSizeHint(widget.sizeHint())
        widget.deleteClicked.connect(lambda: self.OnUserAddListItemDeletedBtnClicked(item))
        widget.editClicked.connect(lambda: self.OnUserAddListItemEditBtnClicked(item))
        widget.resetClicked.connect(lambda: self.OnUserAddListItemResetBtnClicked(item))
        self.listWidgetUser.addItem(item)
        self.listWidgetUser.setItemWidget(item, widget)

    # 删除
    def OnUserAddListItemDeletedBtnClicked(self, item):
        widget = self.listWidgetUser.itemWidget(item)
        u = User()
        u.delete_by_id(widget.Id)
        self.listWidgetUser.takeItem(self.listWidgetUser.row(item))
        self.listWidgetUser.removeItemWidget(item)

    # 修改
    def OnUserAddListItemEditBtnClicked(self, item):
        widget = self.listWidgetUser.itemWidget(item)
        self.userAddDialog.lblTitle.setText("用户信息")
        self.userAddDialog.btnOk.setText("保存")
        self.userAddDialog.Row = self.listWidgetUser.row(item)
        u = User.get(User.Id == widget.Id)
        self.userAddDialog.Id = u.Id
        self.userAddDialog.txtUserName.setText(u.Name)
        self.userAddDialog.txtPhone.setText(u.Phone)
        self.userAddDialog.txtComment.setPlainText(u.Comment)
        self.userAddDialog.cbxRole.setCurrentText(u.Role)
        self.userAddDialog.show()

    # 重置密码
    def OnUserAddListItemResetBtnClicked(self, item):
        self.messagebox = MessageBoxEx()
        widget = self.listWidgetUser.itemWidget(item)
        self.messagebox.show("重置[" + widget.nameLabel.text() + "]密码成功！", "温馨提示", "确认", "取消")

    # 加载用户信息
    def LoadUserInfo(self):
        users = User().select()
        for user in users:
            self.AddUserInfoItem(user)
