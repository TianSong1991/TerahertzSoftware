import json
import math
from datetime import datetime

from AppData import *
import globalvar as gl
from Entity.models import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from Ui.UiCxGpDataMgr import Ui_Form
from Core.StringHelper import FixString
from Common.CxGpDataItem import CxGpTableItem
from Common.MessageBoxEx import MessageBoxEx


class ThzCxGpDataMgr(QWidget, Ui_Form):
    pageSize = 50
    currentPage = 1

    def __init__(self, parent=None):
        super(ThzCxGpDataMgr, self).__init__(parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.LoadCxGpDataInfo()
        self.searchAction = QAction(self.lineSearch)
        self.searchAction.setIcon(QIcon('./Res/search.png'))
        self.searchAction.triggered.connect(self.OnSearch)
        self.lineSearch.addAction(self.searchAction, QLineEdit.TrailingPosition)
        self.lineSearch.textChanged.connect(self.OnSearch)
        self.btnCxGpDataDel.clicked.connect(self.OnDelMany)
        self.btnPrev.clicked.connect(self.OnPrevClicked)
        self.btnNext.clicked.connect(self.OnNextClicked)
        self.cbxPages.setView(QListView())
        self.cbxPages.currentIndexChanged.connect(self.OnCbxPages_CurrentIndexChanged)

    def OnDelMany(self):
        count = self.listWidgetCxGpData.count()
        items = []
        for i in range(count):
            item = self.listWidgetCxGpData.item(i)
            widget = self.listWidgetCxGpData.itemWidget(item)
            if widget.checkBox.isChecked():
                data = GPData()
                data.delete_by_id(widget.Id)
                items.append(item)

        for it in items:
            self.listWidgetCxGpData.takeItem(self.listWidgetCxGpData.row(it))
            self.listWidgetCxGpData.removeItemWidget(it)

    def OnCbxPages_CurrentIndexChanged(self):
        self.currentPage = int(self.cbxPages.currentText())
        items = self.Paging()
        for item in items:
            self.AddCxGpDataItem(item)

    def OnPrevClicked(self):
        if self.currentPage > 1:
            self.currentPage = self.currentPage - 1
            self.cbxPages.setCurrentText(str(self.currentPage))
            items = self.Paging()
            for item in items:
                self.AddCxGpDataItem(item)
        else:
            MessageBoxEx.show("已经到第一页了", "提示", "确定")

    def OnNextClicked(self):
        if self.currentPage < self.cbxPages.count():
            self.currentPage = self.currentPage + 1
            self.cbxPages.setCurrentText(str(self.currentPage))
            items = self.Paging()
            for item in items:
                self.AddCxGpDataItem(item)
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
            "select count(*) from TB_CXGPDATA").fetchone()
        page = math.ceil(res[0] / self.pageSize)
        self.RefreshCombox(page)

    def Paging(self):
        self.listWidgetCxGpData.clear()
        offset = (self.currentPage - 1) * self.pageSize
        if len(self.lineSearch.text()) > 0:
            return CXGPData.select().where(
                SQL("SampleName like '%{}%' or SampleType like '%{}%'".format(self.lineSearch.text(),self.lineSearch.text()))).order_by(CXGPData.Id.desc()).limit(self.pageSize).offset(offset)
        else:
            return CXGPData.select().order_by(CXGPData.Id.desc()).limit(self.pageSize).offset(offset)

    def OnSearch(self):
        result = CXGPData.select().order_by(CXGPData.Id.desc()).where(
            SQL("Operator like '%{}%' or AddDate like '%{}%' or SampleName like '%{}%'".format(self.lineSearch.text(),
                                                                                               self.lineSearch.text(),
                                                                                               self.lineSearch.text())))
        self.listWidgetCxGpData.clear()
        for role in result:
            self.AddCxGpDataItem(role)

    def AddCxGpDataItem(self, data):
        c = self.gbxCxGpDataTableHeader.children()
        widget = CxGpTableItem(c)
        widget.lblName.setText(str(data.SampleName))
        FixString(widget.lblName)
        widget.lblType.setText(str(data.SampleType))
        FixString(widget.lblType)
        widget.lblScanTime.setText(str(data.ScanTime))
        FixString(widget.lblScanTime)
        widget.lblThickness.setText(str(data.Thickness))
        FixString(widget.lblThickness)
        item = SysConf.devCxMode.kuaiYan.scanArr[data.Index]
        widget.lblScanRange.setText(f'频率:{item.freq}Hz / 扫描时间范围:{item.time}ps')
        FixString(widget.lblScanRange)
        widget.lblDivFreq.setText(SysConf.devCxMode.kuaiYan.RefDivideFreqArr[data.DivFreq])
        FixString(widget.lblDivFreq)
        widget.lblOperator.setText(data.Operator)
        FixString(widget.lblOperator)
        if data.AddDate is not None:
            widget.lblDate.setText(data.AddDate.strftime("%Y-%m-%d %H:%M:%S"))
        FixString(widget.lblDate)
        widget.Id = data.Id
        item = QListWidgetItem()
        item.setSizeHint(widget.sizeHint())
        widget.deleteClicked.connect(lambda: self.OnCxGpDataListWidgetDeletedBtnClicked(item))
        widget.viewClicked.connect(lambda: self.OnCxGpDataListWidgetViewBtnClicked(item))
        widget.exportClicked.connect(lambda: self.OnCxGpDataListWidgetExportBtnClicked(item))
        self.listWidgetCxGpData.addItem(item)
        self.listWidgetCxGpData.setItemWidget(item, widget)

    # 加载用户信息
    def LoadCxGpDataInfo(self):
        self.ReSetPages()
        data = self.Paging()
        for item in data:
            self.AddCxGpDataItem(item)

    # 删除
    def OnCxGpDataListWidgetDeletedBtnClicked(self, item):
        widget = self.listWidgetCxGpData.itemWidget(item)
        u = CXGPData()
        u.delete_by_id(widget.Id)
        self.listWidgetCxGpData.takeItem(self.listWidgetCxGpData.row(item))
        self.listWidgetCxGpData.removeItemWidget(item)

    # 修改
    def OnCxGpDataListWidgetViewBtnClicked(self, item):
        widget = self.listWidgetCxGpData.itemWidget(item)
        dt = CXGPData().get_by_id(widget.Id)
        if dt.Data is None:
            MessageBoxEx.show('当前成像光谱记录无数据！')
            return
        gl.appMainWnd.turn2GpView(1, dt)

    # 导出
    def OnCxGpDataListWidgetExportBtnClicked(self, item):
        widget = self.listWidgetCxGpData.itemWidget(item)
        dt = CXGPData().get_by_id(widget.Id)
        if dt.Data is None:
            MessageBoxEx.show('当前成像光谱记录无数据！')
            return

        defFile = f'{QDir.currentPath()}/{dt.SampleName}.qda'
        fileName, _type = QFileDialog.getSaveFileName(self, caption='导出成像光谱数据文件', directory=defFile,
                                                      filter='qda(*.qda)')
        if gl.isStrNoneOrEmpty(fileName):
            return

        jMap = json.loads(dt.Data.decode('utf8'))
        cg = {'scanTime': dt.ScanTime,
              'thickness': dt.Thickness,
              'index': dt.Index,
              'freqDivision': dt.DivFreq,
              'angle': 20,
              'avgNum': 10,
              'name': dt.SampleName,
              'type': dt.SampleType,
              'typeId': dt.SampleTypeID,
              'data': jMap}

        with open(f'{fileName}', "w", encoding='utf-8') as f:
            json.dump(cg, f, indent=4)
