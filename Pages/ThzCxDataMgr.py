import math
import platform
from AppData import *
import globalvar as gl
from peewee import SQL
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from Entity.models import CXData, db
from Ui.UiCxDataMgr import Ui_Form
from Core.StringHelper import FixString
from Common.CxDataItem import CxTableItem
from Common.MessageBoxEx import MessageBoxEx


class ThzCxDataMgr(QWidget, Ui_Form):
    pageSize = 50
    currentPage = 1
    def __init__(self, parent=None):
        super(ThzCxDataMgr, self).__init__(parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.LoadCxDataInfo()
        self.searchAction = QAction(self.lineSearch)
        self.searchAction.setIcon(QIcon('./Res/search.png'))
        self.searchAction.triggered.connect(self.OnSearch)
        self.lineSearch.addAction(self.searchAction, QLineEdit.TrailingPosition)
        self.lineSearch.textChanged.connect(self.OnSearch)
        self.btnCxDataDel.clicked.connect(self.OnDelMany)

        self.btnPrev.clicked.connect(self.OnPrevClicked)
        self.btnNext.clicked.connect(self.OnNextClicked)
        self.cbxPages.setView(QListView())
        self.cbxPages.currentIndexChanged.connect(self.OnCbxPages_CurrentIndexChanged)

    def OnDelMany(self):
        count = self.listWidgetCxData.count()
        items = []
        for i in range(count):
            item = self.listWidgetCxData.item(i)
            widget = self.listWidgetCxData.itemWidget(item)
            if widget.checkBox.isChecked():
                data = CXData()
                data.delete_by_id(widget.Id)
                items.append(item)

        for it in items:
            self.listWidgetCxData.takeItem(self.listWidgetCxData.row(it))
            self.listWidgetCxData.removeItemWidget(it)

    def OnCbxPages_CurrentIndexChanged(self):
        self.currentPage = int(self.cbxPages.currentText())
        items = self.Paging()
        for item in items:
            self.AddCxDataItem(item)

    def OnPrevClicked(self):
        if self.currentPage > 1:
            self.currentPage = self.currentPage - 1
            self.cbxPages.setCurrentText(str(self.currentPage))
            items = self.Paging()
            for item in items:
                self.AddCxDataItem(item)
        else:
            MessageBoxEx.show("已经到第一页了", "提示", "确定")

    def OnNextClicked(self):
        if self.currentPage < self.cbxPages.count():
            self.currentPage = self.currentPage + 1
            self.cbxPages.setCurrentText(str(self.currentPage))
            items = self.Paging()
            for item in items:
                self.AddCxDataItem(item)
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
            "select count(*) from TB_CXDATA").fetchone()
        page = math.ceil(res[0] / self.pageSize)
        self.RefreshCombox(page)

    def Paging(self):
        self.listWidgetCxData.clear()
        offset = (self.currentPage - 1) * self.pageSize
        if len(self.lineSearch.text()) > 0:
            return CXData.select().where(
                SQL("SampleName like '%{}%' or SampleType like '%{}%'".format(self.lineSearch.text(),self.lineSearch.text()))).order_by(CXData.Id.desc()).limit(self.pageSize).offset(offset)
        else:
            return CXData.select().order_by(CXData.Id.desc()).limit(self.pageSize).offset(offset)


    def OnSearch(self):
        result = CXData.select().order_by(CXData.Id.desc()).where(SQL("Operator like '%{}%' or AddDate like '%{}%' or SampleName like '%{}%'".format(self.lineSearch.text(), self.lineSearch.text(), self.lineSearch.text())))
        self.listWidgetCxData.clear()
        for role in result:
            self.AddCxDataItem(role)

    def AddCxDataItem(self, data):
        c = self.gbxCxDataTableHeader.children()
        widget = CxTableItem(c)
        widget.lblName.setText(str(data.SampleName))
        FixString(widget.lblName)
        widget.lblType.setText(str(data.SampleType))
        FixString(widget.lblType)
        widget.lblXStart.setText(str(data.XStart))
        FixString(widget.lblXStart)
        widget.lblXEnd.setText(str(data.XEnd))
        FixString(widget.lblXEnd)
        widget.lblXStep.setText(str(data.XStep))
        FixString(widget.lblXStep)
        widget.lblYStart.setText(str(data.YStart))
        FixString(widget.lblYStart)
        widget.lblYEnd.setText(str(data.YEnd))
        FixString(widget.lblYEnd)
        widget.lblYStep.setText(str(data.YStep))
        FixString(widget.lblYStep)
        widget.lblAngle.setText(str(data.Angle))
        FixString(widget.lblAngle)
        widget.lblZSL.setText(str(data.Refraction))
        FixString(widget.lblZSL)
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
        widget.deleteClicked.connect(lambda: self.OnCxDataListWidgetDeletedBtnClicked(item))
        widget.viewClicked.connect(lambda: self.OnCxDataListWidgetViewBtnClicked(item))
        widget.exportClicked.connect(lambda: self.OnCxDataListWidgetExportBtnClicked(item))
        self.listWidgetCxData.addItem(item)
        self.listWidgetCxData.setItemWidget(item, widget)

    # 加载用户信息
    def LoadCxDataInfo(self):
        self.ReSetPages()
        data = self.Paging()
        for item in data:
            self.AddCxDataItem(item)

    # 删除
    def OnCxDataListWidgetDeletedBtnClicked(self, item):
        widget = self.listWidgetCxData.itemWidget(item)
        u = CXData()
        u.delete_by_id(widget.Id)
        self.listWidgetCxData.takeItem(self.listWidgetCxData.row(item))
        self.listWidgetCxData.removeItemWidget(item)

    # 修改
    def OnCxDataListWidgetViewBtnClicked(self, item):
        widget = self.listWidgetCxData.itemWidget(item)
        dt = CXData().get_by_id(widget.Id)
        if dt.FilePath is None:
            MessageBoxEx.show('当前成像光谱记录无数据！')
            return

        if os.path.exists(dt.FilePath) is False:
            MessageBoxEx.show('当前成像记录数据文件已丢失！')
            return

        gl.appMainWnd.turn2CxView(dt)

    # 导出
    def OnCxDataListWidgetExportBtnClicked(self, item):
        widget = self.listWidgetCxData.itemWidget(item)
        dt = CXData().get_by_id(widget.Id)
        if dt.FilePath is None:
            MessageBoxEx.show('当前成像记录无数据！')
            return
        if os.path.exists(dt.FilePath) is False:
            MessageBoxEx.show('当前成像记录数据文件已丢失！')
            return

        defFile = f'{QDir.currentPath()}/{dt.SampleName}.qda'
        fileName, _type = QFileDialog.getSaveFileName(self, caption='导出成像数据文件', directory=defFile, filter='qda(*.qda)')
        if gl.isStrNoneOrEmpty(fileName):
            return

        if platform.system() == "Windows":
            os.system(f'copy {dt.FilePath} {fileName}')
        else:
            os.system(f'cp {dt.FilePath} {fileName}')