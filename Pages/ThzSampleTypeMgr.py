from datetime import datetime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from peewee import SQL
from Common.SampleItem import SampleItem
from Core.StringHelper import FixString
from Entity.models import Sample
from Pages.ThzSampleAdd import ThzSampleAdd
from Ui.UiSampleMgr import Ui_SampleMgrForm


class ThzSampleTypeMgr(QWidget, Ui_SampleMgrForm):
    pageSize = 50
    currentPage = 1

    def __init__(self, parent=None):
        super(ThzSampleTypeMgr, self).__init__(parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.sampleAddDialog = ThzSampleAdd()
        self.btnDemoAdd.clicked.connect(self.OnSampleAdd)
        self.searchAction = QAction(self.lineSearch)
        self.searchAction.setIcon(QIcon('./Res/search.png'))
        self.searchAction.triggered.connect(self.OnSearch)
        self.lineSearch.addAction(self.searchAction, QLineEdit.TrailingPosition)
        self.lineSearch.textChanged.connect(self.OnSearch)
        self.chkAll.clicked.connect(lambda: self.OnCheckAllClicked(self.chkAll.isChecked()))
        self.btnDemoBatchDel.clicked.connect(self.OnBtnBatchDel)
        # self.DemoAddDialog_RefreshData()
        # item = self.treeWidgetDemoCategory.topLevelItem(0)
        # if item is not None:
        #     data = item.data(0, QtCore.Qt.UserRole)
        #     self.SampleTypeId = data.Id
        #     self.LoadData(data.Id)




    def LoadData(self, typeId):
        self.listWidgetDemo.clear()
        items = Sample.select(Sample.Id, Sample.No, Sample.TypeId, Sample.Name, Sample.AddDate, Sample.Note).where(
            Sample.TypeId == typeId)

        def InitList(data):
            self.AddSampleItem(data)

        for d in items:
            InitList(d)

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

    def OnSearch(self):
        result = Sample.select().where(
            SQL("No like '%{}%' or Name like '%{}%'".format(self.lineSearch.text(), self.lineSearch.text())))
        self.listWidgetDemo.clear()
        for item in result:
            self.AddSampleItem(item)
