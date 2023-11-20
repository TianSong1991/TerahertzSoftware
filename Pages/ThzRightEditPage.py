import json

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDesktopWidget, QTreeWidgetItem, QTreeWidgetItemIterator, QWidget, QTreeWidget, \
    QHBoxLayout

from Common.DialogEx import DialogEx
from Entity.models import Role, User
from Ui.UiRightEdit import Ui_RightEditForm

# 权限修改界面

rights = {
    "光谱扫描": True,
    "成像光谱": True,
    "成像扫描": True,
    "硬件管理": True,
    "用户管理": True,
    "系统设置": True
}


class RightEditForm(DialogEx):
    RoleId = -1
    RightDetail = []

    def __init__(self):
        super(RightEditForm, self).__init__(None)
        self.set1BtnMode()
        self.content = QWidget()
        self.content.setStyleSheet('''
            QTreeWidget{border:none;}
        ''')
        self.horizontalLayout = QHBoxLayout(self.content)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.treeRights = QTreeWidget(self.content)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.treeRights.setFont(font)
        self.treeRights.setStyleSheet("")
        self.treeRights.setHeaderHidden(True)
        self.treeRights.setColumnCount(2)
        self.treeRights.setObjectName("treeRights")
        self.treeRights.headerItem().setText(0, "1")
        self.treeRights.headerItem().setText(1, "2")
        self.treeRights.setColumnCount(2)
        self.treeRights.setColumnWidth(0, 210)
        self.treeRights.setColumnWidth(1, 20)
        self.treeRights.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.treeRights.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.horizontalLayout.addWidget(self.treeRights)

        self.LoadData()
        self.btnOk.clicked.connect(self.OnBtnOKClicked)
        self.lblTitle.setText("权限管理")
        self.setContent(self.content)
        self.resize(300, 350)

    def LoadTopLevel(self, name):
        child = QTreeWidgetItem()
        child.setText(0, name)
        child.setText(1, "")
        child.setCheckState(1, Qt.Unchecked)
        self.treeRights.addTopLevelItem(child)
        return child

    def LoadSubLevel(self, pNode, subName, data):
        child = QTreeWidgetItem(pNode)
        child.setText(0, subName)
        child.setText(1, "")
        child.setCheckState(1, Qt.Unchecked)
        if type(data) is dict:
            for k, v in data.items():
                self.LoadSubLevel(child, k, v)

    def LoadData(self):
        for k, v in rights.items():
            node = self.LoadTopLevel(k)
            # for kk, vv in v.items():
            #     self.LoadSubLevel(node, kk, vv)
        # self.treeRights.expandAll()

    def GetNodes(self, node, txt):
        if node is None:
            res = self.treeRights.findItems(txt, Qt.MatchExactly, 0)
            if len(res) > 0:
                return res[0]
        else:
            c = node.childCount()
            for i in range(0, c):
                if node.child(i).text(0) == txt:
                    return node.child(i)
        return None

    def SetChecked(self, node):
        p = node.parent()
        while p:
            p.setCheckState(1, Qt.Checked)
            p = p.parent()

    # 初始化个人权限信息
    def InitUserRights(self):
        if self.RoleId == -1:
            return
        r = Role.get(Role.Id == self.RoleId)
        print("====>r.right:", r.Rights)
        if r.Rights != "" and r.Rights is not None:
            roleRights = json.loads(r.Rights)
            # print(roleRights)
            # 处理QTreeWidget选中状态
            ns = []
            for i in range(0, len(roleRights)):
                item = roleRights[i]
                arr = (item.get('key') + "," + item.get('txt')).split(',')
                node = None
                for k in range(0, len(arr)):
                    node = self.GetNodes(node, arr[k])
                    if node is not None:
                        node.setCheckState(1, item.get('isChecked'))
                        if item.get('isChecked') == Qt.Checked:
                            ns.append(node)
            for n in ns:
                self.SetChecked(n)

    def RangeSubNode(self, item, key):
        key = key.strip(',')
        # 有子节点
        c = item.childCount()
        if c > 0:
            if key != "":
                self.RightDetail.append({"txt": item.text(0), "isChecked": item.checkState(1), "key": key})
            for i in range(0, c):
                self.RangeSubNode(item.child(i), key + "," + item.text(0))
        else:
            if key != "":
                self.RightDetail.append({"txt": item.text(0), "isChecked": item.checkState(1), "key": key})

    # 获取设置的角色权限信息
    # def GetRights(self):
    #     self.RightDetail = []
    #     tc = self.treeRights.topLevelItemCount()
    #     for i in range(0, tc):
    #         # 遍历头部节点
    #         self.RangeSubNode(self.treeRights.topLevelItem(i), "")
    #     r = json.dumps(self.RightDetail)
    #     print("roleId:", self.RoleId, " ", r)
    #     Role.update({Role.Rights: r}).where(Role.Id == self.RoleId).execute()

    def GetRights(self):
        self.RightDetail = []
        tc = self.treeRights.topLevelItemCount()
        for i in range(0, tc):
            item = self.treeRights.topLevelItem(i)
            self.RightDetail.append({"txt": item.text(0), "isChecked": item.checkState(1), "key": ""})
        r = json.dumps(self.RightDetail)
        print("roleId:", self.RoleId, " ", r)
        Role.update({Role.Rights: r}).where(Role.Id == self.RoleId).execute()

    # 确定按钮点击事件
    def OnBtnOKClicked(self):
        self.GetRights()
        self.close()
