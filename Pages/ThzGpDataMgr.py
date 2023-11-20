import json
import math
import globalvar as gl
from peewee import SQL
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from Ui.UiGpData import Ui_Form
from Entity.models import GPData, db
from Core.StringHelper import FixString
from Common.GpDataItem import GpTableItem
from Common.MessageBoxEx import MessageBoxEx


class ThzGpDataMgr(QWidget, Ui_Form):
    pageSize = 50
    currentPage = 1

    def __init__(self, parent=None):
        super(ThzGpDataMgr, self).__init__(parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.LoadGpDataInfo()
        self.searchAction = QAction(self.lineSearch)
        self.searchAction.setIcon(QIcon('./Res/search.png'))
        self.searchAction.triggered.connect(self.OnSearch)
        self.lineSearch.addAction(self.searchAction, QLineEdit.TrailingPosition)
        self.lineSearch.textChanged.connect(self.OnSearch)
        self.btnGpDataDel.clicked.connect(self.OnDelMany)

        self.btnPrev.clicked.connect(self.OnPrevClicked)
        self.btnNext.clicked.connect(self.OnNextClicked)
        self.cbxPages.setView(QListView())
        self.cbxPages.currentIndexChanged.connect(self.OnCbxPages_CurrentIndexChanged)

    def OnDelMany(self):
        count = self.listWidgetGpData.count()
        items = []
        for i in range(count):
            item = self.listWidgetGpData.item(i)
            widget = self.listWidgetGpData.itemWidget(item)
            if widget.checkBox.isChecked():
                data = GPData()
                data.delete_by_id(widget.Id)
                items.append(item)

        for it in items:
            self.listWidgetGpData.takeItem(self.listWidgetGpData.row(it))
            self.listWidgetGpData.removeItemWidget(it)

    def OnCbxPages_CurrentIndexChanged(self):
        self.currentPage = int(self.cbxPages.currentText())
        items = self.Paging()
        for item in items:
            self.AddGpDataItem(item)

    def OnPrevClicked(self):
        if self.currentPage > 1:
            self.currentPage = self.currentPage - 1
            self.cbxPages.setCurrentText(str(self.currentPage))
            items = self.Paging()
            for item in items:
                self.AddGpDataItem(item)
        else:
            MessageBoxEx.show("已经到第一页了", "提示", "确定")

    def OnNextClicked(self):
        if self.currentPage < self.cbxPages.count():
            self.currentPage = self.currentPage + 1
            self.cbxPages.setCurrentText(str(self.currentPage))
            items = self.Paging()
            for item in items:
                self.AddGpDataItem(item)
        else:
            MessageBoxEx.show("已经到最后一页了", "提示", "确定")

    def RefreshCombox(self, pages):
        if pages > 0:
            for i in range(0, pages):
                self.cbxPages.addItem(str(i + 1))
        else:
            self.cbxPages.addItem(str(1))

    def ReSetPages(self):
        self.cbxPages.clear()
        res = db.execute_sql(
            "select count(*) from TB_GPDATA").fetchone()
        page = math.ceil(res[0] / self.pageSize)
        self.RefreshCombox(page)

    def Paging(self):
        self.listWidgetGpData.clear()
        offset = (self.currentPage - 1) * self.pageSize
        if len(self.lineSearch.text()) > 0:
            return GPData.select().where(
                SQL("SampleName like '%{}%' or SampleType like '%{}%'".format(self.lineSearch.text(),self.lineSearch.text()))).order_by(GPData.Id.desc()).limit(self.pageSize).offset(offset)
        else:
            return GPData.select().order_by(GPData.Id.desc()).limit(self.pageSize).offset(offset)


    def OnSearch(self):
        result = GPData.select().order_by(GPData.Id.desc()).where(
            SQL("Operator like '%{}%' or AddDate like '%{}%' or SampleName like '%{}%'".format(self.lineSearch.text(),
                                                                                               self.lineSearch.text(),
                                                                                               self.lineSearch.text())))
        self.listWidgetGpData.clear()
        for role in result:
            self.AddGpDataItem(role)

    def AddGpDataItem(self, data):
        c = self.gbxGpDataTableHeader.children()
        widget = GpTableItem(c)
        widget.lblName.setText(str(data.SampleName))
        FixString(widget.lblName)
        widget.lblType.setText(str(data.SampleType))
        FixString(widget.lblType)
        widget.lblStart.setText(str(data.Start))
        FixString(widget.lblStart)
        widget.lblEnd.setText(str(data.End))
        FixString(widget.lblEnd)
        widget.lblStep.setText(str(data.Step))
        FixString(widget.lblStep)
        widget.lblThickness.setText(str(data.Thickness))
        FixString(widget.lblThickness)
        widget.lblOperator.setText(data.Operator)
        FixString(widget.lblOperator)
        if data.AddDate is not None:
            widget.lblDate.setText(data.AddDate.strftime("%Y-%m-%d %H:%M:%S"))
        FixString(widget.lblDate)
        widget.Id = data.Id
        item = QListWidgetItem()
        item.setSizeHint(widget.sizeHint())
        widget.deleteClicked.connect(lambda: self.OnGpDataListWidgetDeletedBtnClicked(item))
        widget.viewClicked.connect(lambda: self.OnGpDataListWidgetViewBtnClicked(item))
        widget.exportClicked.connect(lambda: self.OnGpDataListWidgetExportBtnClicked(item))
        self.listWidgetGpData.addItem(item)
        self.listWidgetGpData.setItemWidget(item, widget)

    # 加载用户信息
    def LoadGpDataInfo(self):
        self.ReSetPages()
        data = self.Paging()
        for item in data:
            self.AddGpDataItem(item)

    # 删除
    def OnGpDataListWidgetDeletedBtnClicked(self, item):
        widget = self.listWidgetGpData.itemWidget(item)
        u = GPData()
        u.delete_by_id(widget.Id)
        self.listWidgetGpData.takeItem(self.listWidgetGpData.row(item))
        self.listWidgetGpData.removeItemWidget(item)

    # 修改
    def OnGpDataListWidgetViewBtnClicked(self, item):
        widget = self.listWidgetGpData.itemWidget(item)
        dt = GPData().get_by_id(widget.Id)
        if dt.Data is None:
            MessageBoxEx.show('当前成像光谱记录无数据！')
            return
        gl.appMainWnd.turn2GpView(0, dt)

    # 导出
    def OnGpDataListWidgetExportBtnClicked(self, item):
        widget = self.listWidgetGpData.itemWidget(item)
        dt = GPData().get_by_id(widget.Id)
        if dt.Data is None:
            MessageBoxEx.show('当前成像光谱记录无数据！')
            return

        defFile = f'{QDir.currentPath()}/{dt.SampleName}.qda'
        fileName, _type = QFileDialog.getSaveFileName(self, caption='导出光谱数据文件', directory=defFile, filter='qda(*.qda)')
        if gl.isStrNoneOrEmpty(fileName):
            return

        jMap = json.loads(dt.Data.decode('utf8'))
        gp = {'start': dt.Start,
              'end': dt.End,
              'step': dt.Step,
              'thickness': dt.Thickness,
              'name': dt.SampleName,
              'type': dt.SampleType,
              'typeId': dt.SampleTypeID,
              'data': jMap}

        with open(f'{fileName}', "w", encoding='utf-8') as f:
            json.dump(gp, f, indent=4)
