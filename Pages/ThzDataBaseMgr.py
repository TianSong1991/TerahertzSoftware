import time
from datetime import datetime

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from peewee import SQL

from Common.DemoCategoryItem import PreAddItem, AddedItem
from Common.MessageBoxEx import MessageBoxEx
from Common.SampleItem import SampleItem
from Core.StringHelper import FixString
from Entity.models import SampleType, Sample
from Pages.ThzDemoAddDialog import DemoCategoryAddForm
from Pages.ThzSampleAdd import ThzSampleAdd
from Ui.UiDataBaseMgr import Ui_Form


class ThzDataBaseMgr(QWidget, Ui_Form):
    SampleTypeId = 0

    def __init__(self, parent=None):
        super(ThzDataBaseMgr, self).__init__(parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.demoAddDialog = DemoCategoryAddForm()
        self.sampleAddDialog = ThzSampleAdd()
        self.sampleAddDialog.btnOk.clicked.connect(self.OnSampleAddDialog_BtnOkClicked)
        self.btnAddDemoCategory.clicked.connect(self.OnBtnAddDemoCategoryClicked)
        self.btnDemoAdd.clicked.connect(self.OnSampleAdd)
        self.searchAction = QAction(self.lineSearch)
        self.searchAction.setIcon(QIcon('./Res/search.png'))
        self.searchAction.triggered.connect(self.OnSearch)
        self.lineSearch.addAction(self.searchAction, QLineEdit.TrailingPosition)
        self.lineSearch.textChanged.connect(self.OnSearch)
        self.demoAddDialog.btnTopItemAdd.clicked.connect(self.OnBtnTopItemAddClicked)
        self.demoAddDialog.btnClose.clicked.connect(self.OnDemoAddDialog_BtnCloseClicked)
        self.demoAddDialog.btnOk.clicked.connect(self.OnDemoAddDialog_BtnOkClicked)
        self.treeWidgetDemoCategory.clicked.connect(self.OnTreeWidgetDemoCategoryClicked)
        self.chkAll.clicked.connect(lambda: self.OnCheckAllClicked(self.chkAll.isChecked()))
        self.btnDemoBatchDel.clicked.connect(self.OnBtnBatchDel)
        self.gbxRight.setVisible(False)

        self.RefreshData()
        self.DemoAddDialog_RefreshData()
        item = self.treeWidgetDemoCategory.topLevelItem(0)
        if item is not None:
            data = item.data(0, QtCore.Qt.UserRole)
            self.SampleTypeId = data.Id
            self.LoadData(data.Id)

    def OnBtnBatchDel(self):
        count = self.listWidgetDemo.count()
        items = []
        for i in range(count):
            item = self.listWidgetDemo.item(i)
            widget = self.listWidgetDemo.itemWidget(item)
            if widget.checkBox.isChecked():
                u = Sample()
                u.delete_by_id(widget.Id)
                items.append(item)

        for it in items:
            self.listWidgetDemo.takeItem(self.listWidgetDemo.row(it))
            self.listWidgetDemo.removeItemWidget(it)

    def OnCheckAllClicked(self, isChecked):
        count = self.listWidgetDemo.count()
        for i in range(count):
            widget = self.listWidgetDemo.itemWidget(self.listWidgetDemo.item(i))
            widget.checkBox.setChecked(isChecked)

    def OnSampleAdd(self):
        self.sampleAddDialog.show()

    def OnTreeWidgetDemoCategoryClicked(self):
        data = self.treeWidgetDemoCategory.currentItem().data(0, QtCore.Qt.UserRole)
        self.SampleTypeId = data.Id
        self.LoadData(data.Id)

    def OnSampleAddDialog_BtnOkClicked(self):
        Sample.create(No=self.sampleAddDialog.txtSampleNo.text(),
                      TypeId=self.SampleTypeId,
                      Name=self.sampleAddDialog.txtSampleName.text(),
                      AddDate=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
                      Note=self.sampleAddDialog.txtSampleComment.toPlainText())
        self.LoadData(self.SampleTypeId)

    def AddSampleItem(self, sample):
        widget = SampleItem(self.gbxDemoMgrTableHeader.children())
        widget.lblNo.setText(str(sample.No))
        FixString(widget.lblNo)
        widget.lblName.setText(str(sample.Name))
        FixString(widget.lblName)
        widget.lblAddDate.setText(str(sample.AddDate))
        FixString(widget.lblAddDate)
        widget.lblComment.setText(sample.Note)
        FixString(widget.lblComment)
        widget.Id = sample.Id
        item = QListWidgetItem()
        item.setSizeHint(widget.sizeHint())
        widget.deleteClicked.connect(lambda: self.OnSampleListItemBtnDelClicked(item))
        widget.viewClicked.connect(lambda: self.OnSampleListItemBtnViewClicked(item))
        self.listWidgetDemo.addItem(item)
        self.listWidgetDemo.setItemWidget(item, widget)

    def OnSampleListItemBtnDelClicked(self, item):
        widget = self.listWidgetDemo.itemWidget(item)
        Sample.delete_by_id(widget.Id)
        self.listWidgetDemo.removeItemWidget(item)
        self.listWidgetDemo.takeItem(self.listWidgetDemo.row(item))

    def OnSampleListItemBtnViewClicked(self, item):
        print("view")

    def LoadData(self, typeId):
        self.listWidgetDemo.clear()
        items = Sample.select(Sample.Id, Sample.No, Sample.TypeId, Sample.Name, Sample.AddDate, Sample.Note).where(
            Sample.TypeId == typeId)

        def InitList(data):
            self.AddSampleItem(data)

        for d in items:
            InitList(d)

    def OnDemoAddDialog_BtnOkClicked(self):
        self.RefreshData()
        self.demoAddDialog.treeWidget.clear()
        self.demoAddDialog.close()

    def OnDemoAddDialog_BtnCloseClicked(self):
        self.RefreshData()
        self.demoAddDialog.treeWidget.clear()
        self.demoAddDialog.close()

    def DemoAddDialog_AddPreItem(self, pNode=None):
        widget = PreAddItem()
        item = QTreeWidgetItem()
        widget.txtName.setPlaceholderText("请输入样品分类名称")
        if pNode is None:
            self.demoAddDialog.treeWidget.addTopLevelItem(item)
        else:
            pNode.addChild(item)
            self.demoAddDialog.treeWidget.expandAll()
        self.demoAddDialog.treeWidget.setItemWidget(item, 0, widget)
        widget.btnSave.clicked.connect(lambda w: self.OnTreeWidgetItem_BtnSaveClicked(item))
        widget.btnCancel.clicked.connect(lambda w: self.OnTreeWidgetItem_BtnCancelClicked(item))
        return item, widget

    def DemoAddDialog_AddedItem(self, item):
        preWidget = self.demoAddDialog.treeWidget.itemWidget(item, 0)
        widget = AddedItem()
        widget.lblName.setText(preWidget.txtName.text())
        widget.Id = preWidget.Id
        self.demoAddDialog.treeWidget.removeItemWidget(item, 0)
        self.demoAddDialog.treeWidget.setItemWidget(item, 0, widget)
        widget.btnAdd.clicked.connect(lambda w: self.OnTreeWidgetItem_BtnAddClicked(item))
        widget.btnDel.clicked.connect(lambda w: self.OnTreeWidgetItem_BtnDelClicked(item))

    def OnBtnTopItemAddClicked(self):
        self.DemoAddDialog_AddPreItem()

    # 获取节点path
    def DemoAddDialog_GetNodePath(self, item):
        path = ""
        ids = []
        while self.demoAddDialog.treeWidget.indexOfTopLevelItem(item) == -1:
            widget = self.demoAddDialog.treeWidget.itemWidget(item, 0)
            ids.append(widget.Id)
            item = item.parent()
        widget = self.demoAddDialog.treeWidget.itemWidget(item, 0)
        ids.append(widget.Id)
        tmp = list(reversed(ids))
        for tid in tmp:
            path = path + "|" + str(tid)
        return path.lstrip("|")

    def DemoAddDialog_FindItemById(self, id):
        item = QTreeWidgetItemIterator(self.demoAddDialog.treeWidget)
        while item.value():
            widget = self.demoAddDialog.treeWidget.itemWidget(item.value(), 0)
            if widget.Id == id:
                return item.value()
            item = item.__iadd__(1)
        return None

    def DemoAddDialog_RefreshData(self):
        self.demoAddDialog.treeWidget.clear()
        items = SampleType.select()
        c = len(items)

        #
        def InitItem(data):
            if data.ParentId > 0:
                item = self.DemoAddDialog_FindItemById(data.ParentId)
                if item is not None:
                    node = QTreeWidgetItem()
                    tmpWidget = AddedItem()
                    tmpWidget.lblName.setText(data.Name)
                    tmpWidget.Id = data.Id
                    tmpWidget.btnAdd.clicked.connect(lambda x: self.OnTreeWidgetItem_BtnAddClicked(node))
                    tmpWidget.btnDel.clicked.connect(lambda x: self.OnTreeWidgetItem_BtnDelClicked(node))
                    item.addChild(node)
                    self.demoAddDialog.treeWidget.setItemWidget(node, 0, tmpWidget)
            else:
                widget = AddedItem()
                item = QTreeWidgetItem()
                widget.lblName.setText(data.Name)
                widget.Id = data.Id
                widget.btnAdd.clicked.connect(lambda x: self.OnTreeWidgetItem_BtnAddClicked(item))
                widget.btnDel.clicked.connect(lambda x: self.OnTreeWidgetItem_BtnDelClicked(item))
                self.demoAddDialog.treeWidget.addTopLevelItem(item)
                self.demoAddDialog.treeWidget.setItemWidget(item, 0, widget)

        for i in range(0, c):
            InitItem(items[i])

        self.demoAddDialog.treeWidget.expandAll()

    def OnTreeWidgetItem_BtnAddClicked(self, item):
        self.DemoAddDialog_AddPreItem(item)

    # 清空子节点数据
    def DelTreeWidgetItem_SubItemsData(self, item):
        c = item.childCount()
        for i in range(0, c):
            n = item.child(i)
            widget = self.demoAddDialog.treeWidget.itemWidget(n, 0)
            SampleType().delete_by_id(widget.Id)
            self.DelTreeWidgetItem_SubItemsData(n)

    # 删除
    def OnTreeWidgetItem_BtnDelClicked(self, item):
        i = self.demoAddDialog.treeWidget.indexOfTopLevelItem(item)
        widget = self.demoAddDialog.treeWidget.itemWidget(item, 0)
        if i >= 0:
            self.DelTreeWidgetItem_SubItemsData(item)
            SampleType().delete_by_id(widget.Id)
            self.demoAddDialog.treeWidget.takeTopLevelItem(i)
        else:
            self.DelTreeWidgetItem_SubItemsData(item)
            SampleType().delete_by_id(widget.Id)
            pNode = item.parent()
            pNode.removeChild(item)

    # 取消
    def OnTreeWidgetItem_BtnCancelClicked(self, item):
        i = self.demoAddDialog.treeWidget.indexOfTopLevelItem(item)
        if i >= 0:
            self.demoAddDialog.treeWidget.takeTopLevelItem(i)
        else:
            pNode = item.parent()
            pNode.removeChild(item)

    def OnTreeWidgetItem_BtnSaveClicked(self, item):
        widget = self.demoAddDialog.treeWidget.itemWidget(item, 0)
        if self.demoAddDialog.treeWidget.indexOfTopLevelItem(item) < 0:
            pItem = item.parent()
            pWidget = self.demoAddDialog.treeWidget.itemWidget(pItem, 0)
            st = SampleType().create(Name=widget.txtName.text(), ParentId=pWidget.Id,
                                     Path="")
        else:
            st = SampleType().create(Name=widget.txtName.text(), ParentId=0,
                                     Path="")
        if st.Id > 0:
            widget.Id = st.Id
            path = self.DemoAddDialog_GetNodePath(item)
            SampleType.update({SampleType.Path: path}).where(SampleType.Id == st.Id).execute()
            self.DemoAddDialog_AddedItem(item)
        else:
            MessageBoxEx.show("保存失败!", "提示", "确定")

    def FindItemById(self, id):
        item = QTreeWidgetItemIterator(self.treeWidgetDemoCategory)
        while item.value():
            tmp = item.value()
            if tmp.data(0, QtCore.Qt.UserRole).Id == id:
                return item.value()
            item = item.__iadd__(1)
        return None

    def RefreshData(self):
        self.treeWidgetDemoCategory.clear()
        items = SampleType.select()
        c = len(items)
        for i in range(0, c):
            if items[i].ParentId > 0:
                item = self.FindItemById(items[i].ParentId)
                if item is not None:
                    node = QTreeWidgetItem()
                    node.setText(0, items[i].Name)
                    node.setData(0, QtCore.Qt.UserRole, items[i])
                    item.addChild(node)
            else:
                item = QTreeWidgetItem()
                item.setText(0, items[i].Name)
                item.setData(0, QtCore.Qt.UserRole, items[i])
                self.treeWidgetDemoCategory.addTopLevelItem(item)
        self.treeWidgetDemoCategory.expandAll()

    def OnSearch(self):
        result = Sample.select().where(
            SQL("No like '%{}%' or Name like '%{}%'".format(self.lineSearch.text(), self.lineSearch.text())))
        self.listWidgetDemo.clear()
        for item in result:
            self.AddSampleItem(item)

    def OnBtnAddDemoCategoryClicked(self):
        self.demoAddDialog.show()
        self.DemoAddDialog_RefreshData()
