from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from peewee import SQL

from Common.RoleTableItem import RoleTableItem
from Core.StringHelper import FixString
from Entity.models import Role, User
from Pages.ThzRightEditPage import RightEditForm
from Pages.ThzRoleAddDialog import RoleAddDialogForm
from Ui.UiRoleMgr import Ui_UiRoleMgr


class ThzRoleMgr(QWidget, Ui_UiRoleMgr):
    def __init__(self, parent=None):
        super(ThzRoleMgr, self).__init__(parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.LoadRoleInfo()

        self.roleAddDialog = RoleAddDialogForm()
        self.roleAddDialog.hide()

        self.rightEditDialog = RightEditForm()
        self.rightEditDialog.hide()

        self.searchAction = QAction(self.lineSearch)
        self.searchAction.setIcon(QIcon('./Res/search.png'))
        self.searchAction.triggered.connect(self.OnSearch)
        self.lineSearch.addAction(self.searchAction, QLineEdit.TrailingPosition)
        self.lineSearch.textChanged.connect(self.OnSearch)
        # 角色管理添加删除功能
        self.btnRoleAdd.clicked.connect(self.OnBtnRoleAddClicked)
        # 批量删除按钮
        self.btnRoleDel.clicked.connect(self.OnDelManyClick)
        # 选择全部
        self.chkAll.clicked.connect(lambda: self.OnCheckAllClicked(self.chkAll.isChecked()))
        self.roleAddDialog.btnOk.clicked.connect(self.OnRoleAddDialogBtnRoleAddClicked)

    def OnSearch(self):
        result = Role.select().where(SQL("Name like '%{}%'".format(self.lineSearch.text())))
        self.listWidgetRole.clear()
        for role in result:
            self.AddRoleInfoItem(role)

    def OnRoleAddDialogBtnRoleAddClicked(self):
        if self.roleAddDialog.lblTitle.text() == "角色添加":
            u = Role()
            u.Id = u.create(Name=self.roleAddDialog.txtRoleName.text(),
                            Comment=self.roleAddDialog.txtComment.toPlainText())
            u.Name = self.roleAddDialog.txtRoleName.text()
            u.Comment = self.roleAddDialog.txtComment.toPlainText()
            self.AddRoleInfoItem(u)
        else:
            Role.update({Role.Name: self.roleAddDialog.txtRoleName.text(),
                         Role.Comment: self.roleAddDialog.txtComment.toPlainText()}).where(
                Role.Id == self.roleAddDialog.Id).execute()
            widget = self.listWidgetRole.itemWidget(self.listWidgetRole.item(self.roleAddDialog.Row))
            widget.roleLabel.setText(self.roleAddDialog.txtRoleName.text())
            widget.commentLabel.setText(self.roleAddDialog.txtComment.toPlainText())
            FixString(widget.roleLabel)
            FixString(widget.commentLabel)
        self.roleAddDialog.close()

    def OnDelManyClick(self):
        count = self.listWidgetRole.count()
        items = []
        for i in range(count):
            item = self.listWidgetRole.item(i)
            widget = self.listWidgetRole.itemWidget(item)
            if widget.checkBox.isChecked():
                u = User()
                u.delete_by_id(widget.Id)
                items.append(item)

        for it in items:
            self.listWidgetRole.takeItem(self.listWidgetRole.row(it))
            self.listWidgetRole.removeItemWidget(it)

    def OnCheckAllClicked(self, isChecked):
        count = self.listWidgetRole.count()
        # 遍历listwidget中的内容
        for i in range(count):
            widget = self.listWidgetRole.itemWidget(self.listWidgetRole.item(i))
            widget.checkBox.setChecked(isChecked)

    #
    def OnBtnRoleAddClicked(self):
        self.roleAddDialog.show()

        # 添加角色信息

    def AddRoleInfoItem(self, role):
        widget = RoleTableItem(self.gbxRoleTableHeader.children())
        widget.roleLabel.setText(role.Name)
        FixString(widget.roleLabel)
        widget.commentLabel.setText(role.Comment)
        FixString(widget.commentLabel)
        widget.Id = role.Id
        item = QListWidgetItem()
        item.setSizeHint(widget.sizeHint())
        widget.deleteClicked.connect(lambda: self.OnRoleAddListItemDeletedBtnClicked(item))
        widget.editClicked.connect(lambda: self.OnRoleAddListItemEditBtnClicked(item))
        widget.rightClicked.connect(lambda: self.OnRoleEditListItemRightBtnClicked(item))
        self.listWidgetRole.addItem(item)
        self.listWidgetRole.setItemWidget(item, widget)

        # 加载角色信息

    def LoadRoleInfo(self):
        roles = Role().select()
        for role in roles:
            self.AddRoleInfoItem(role)

        # 定义listview自定义控件item中删除按钮点击事件

    def OnRoleAddListItemDeletedBtnClicked(self, item):
        widget = self.listWidgetRole.itemWidget(item)
        u = Role()
        u.delete_by_id(widget.Id)
        print(widget.roleLabel.text(), widget.Id)
        self.listWidgetRole.takeItem(self.listWidgetRole.row(item))
        self.listWidgetRole.removeItemWidget(item)

        # 定义listview自定义控件item中删除按钮点击事件

    def OnRoleAddListItemEditBtnClicked(self, item):
        widget = self.listWidgetRole.itemWidget(item)
        self.roleAddDialog.lblTitle.setText("角色修改")
        u = Role.get(Role.Id == widget.Id)
        self.roleAddDialog.Row = self.listWidgetRole.row(item)
        print(widget.Id)
        self.roleAddDialog.txtRoleName.setText(u.Name)
        self.roleAddDialog.txtComment.setPlainText(u.Comment)
        self.roleAddDialog.show()

    def OnRoleEditListItemRightBtnClicked(self, item):
        widget = self.listWidgetRole.itemWidget(item)
        self.rightEditDialog = RightEditForm()
        self.rightEditDialog.RoleId = widget.Id
        self.rightEditDialog.InitUserRights()
        self.rightEditDialog.show()
