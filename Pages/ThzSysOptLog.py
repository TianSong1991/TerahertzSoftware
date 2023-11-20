import math
import time

from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from peewee import SQL

from Common.MessageBoxEx import MessageBoxEx
from Common.SysOptLogItem import SysOptLogItem
from Core.StringHelper import FixString
from Entity.models import SysLog, db
from Ui.UiSysOptLog import Ui_SysOptLogForm


class ThzSysOptLogMgr(QWidget, Ui_SysOptLogForm):
    pageSize = 50
    currentPage = 1

    def __init__(self, parent=None):
        super(ThzSysOptLogMgr, self).__init__(parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.deBegin.setDate(QDate.currentDate().addDays(-1))
        self.deEnd.setDate(QDate.currentDate().addDays(1))
        self.LoadSysLogInfo()
        self.searchAction = QAction(self.lineSearch)
        self.searchAction.setIcon(QIcon('./Res/search.png'))
        self.searchAction.triggered.connect(self.OnSearch)
        self.lineSearch.addAction(self.searchAction, QLineEdit.TrailingPosition)
        self.lineSearch.textChanged.connect(self.OnSearch)
        self.chkAll.clicked.connect(lambda: self.OnCheckAllClicked(self.chkAll.isChecked()))
        self.btnDel.clicked.connect(self.OnDelManyClick)
        self.btnPrev.clicked.connect(self.OnPrevClicked)
        self.btnNext.clicked.connect(self.OnNextClicked)
        self.cbxPages.setView(QListView())
        self.cbxPages.currentIndexChanged.connect(self.OnCbxPages_CurrentIndexChanged)

    def OnCbxPages_CurrentIndexChanged(self):
        if self.cbxPages.currentIndex() == -1:
            return

        self.currentPage = int(self.cbxPages.currentText())
        logs = self.Paging()
        for log in logs:
            self.AddSysLogItem(log)

    def OnPrevClicked(self):
        if self.currentPage > 1:
            self.currentPage = self.currentPage - 1
            self.cbxPages.setCurrentText(str(self.currentPage))
            logs = self.Paging()
            for log in logs:
                self.AddSysLogItem(log)
        else:
            MessageBoxEx.show("已经到第一页了", "提示", "确定")

    def OnNextClicked(self):
        if self.currentPage < self.cbxPages.count():
            self.currentPage = self.currentPage + 1
            self.cbxPages.setCurrentText(str(self.currentPage))
            logs = self.Paging()
            for log in logs:
                self.AddSysLogItem(log)
        else:
            MessageBoxEx.show("已经到最后一页了", "提示", "确定")

    def OnDelManyClick(self):
        count = self.listWidgetLogs.count()
        items = []
        for i in range(count):
            item = self.listWidgetLogs.item(i)
            widget = self.listWidgetLogs.itemWidget(item)
            if widget.checkBox.isChecked():
                log = SysLog()
                log.delete_by_id(widget.Id)
                items.append(item)

        for it in items:
            self.listWidgetLogs.takeItem(self.listWidgetLogs.row(it))
            self.listWidgetLogs.removeItemWidget(it)

    def OnCheckAllClicked(self, isChecked):
        count = self.listWidgetLogs.count()
        # 遍历listwidget中的内容
        for i in range(count):
            widget = self.listWidgetLogs.itemWidget(self.listWidgetLogs.item(i))
            widget.checkBox.setChecked(isChecked)

    def OnSearch(self):
        self.ReSetPages()
        logs = self.Paging()
        self.cbxPages.setCurrentText(str(self.currentPage))
        for log in logs:
            self.AddSysLogItem(log)

    def ReSetPages(self):
        self.cbxPages.clear()
        btime = self.deBegin.dateTime().toLocalTime().toTime_t()
        etime = self.deEnd.dateTime().toLocalTime().toTime_t()
        res = db.execute_sql(
            "select count(*) as cnt from (select *,CAST(strftime('%s',AddDate,'UTC') as int) as utcTime from TB_SysLog) as a inner join User as u on a.UserId=u.Id where (u.Name like '%{}%' or a.Type like '%{}%') and ( a.utcTime > {} and  a.utcTime < {});".format(
                self.lineSearch.text(), self.lineSearch.text(), btime, etime)).fetchone()
        page = math.ceil(res[0] / self.pageSize)
        self.RefreshCombox(page)

    def Paging(self):
        self.listWidgetLogs.clear()
        btime = self.deBegin.dateTime().toLocalTime().toTime_t()
        etime = self.deEnd.dateTime().toLocalTime().toTime_t()
        offset = (self.currentPage - 1) * self.pageSize
        if len(self.lineSearch.text()) > 0:
            return db.execute_sql(
                "select u.Name,a.Type,a.AddDate,a.Context,a.Id from (select *,CAST(strftime('%s',AddDate,'UTC') as int) as utcTime from TB_SysLog) as a inner join User as u on a.UserId=u.Id where (u.Name like '%{}%' or a.Type like '%{}%') and ( a.utcTime > {} and  a.utcTime < {}) order by a.Id limit {} offset {};".format(
                    self.lineSearch.text(), self.lineSearch.text(), btime, etime, self.pageSize, offset)).fetchall()
        else:
            return db.execute_sql(
                "select u.Name,a.Type,a.AddDate,a.Context,a.Id from (select *,CAST(strftime('%s',AddDate,'UTC') as int) as utcTime from TB_SysLog) as a inner join User as u on a.UserId=u.Id where ( a.utcTime > {} and  a.utcTime < {}) order by a.Id limit {} offset {};".format(
                    btime, etime, self.pageSize, offset)).fetchall()

    def AddSysLogItem(self, log):
        widget = SysOptLogItem(self.gbxSysLogTableHeader.children(), self.listWidgetLogs)
        widget.lblName.setText(str(log[0]))
        FixString(widget.lblName)
        widget.lblType.setText(str(log[1]))
        FixString(widget.lblType)
        widget.lblDate.setText(str(log[2]))
        FixString(widget.lblDate)
        widget.lblContex.setText(str(log[3]))
        FixString(widget.lblContex)
        widget.Id = log[4]
        item = QListWidgetItem()
        item.setSizeHint(widget.sizeHint())
        self.listWidgetLogs.addItem(item)
        self.listWidgetLogs.setItemWidget(item, widget)

    def RefreshCombox(self, pages):
        if pages > 0:
            for i in range(0, pages):
                self.cbxPages.addItem(str(i + 1))
        else:
            self.cbxPages.addItem(str(1))

    # 加载用户信息
    def LoadSysLogInfo(self):
        self.ReSetPages()
        logs = self.Paging()
        for log in logs:
            self.AddSysLogItem(log)
