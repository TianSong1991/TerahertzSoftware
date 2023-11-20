from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from Common.SysCfgItem import SysCfgTableItem
from Core.StringHelper import FixString
from Entity.models import SysConfig
from Ui.UiSystemSettingCfgMgr import Ui_Form


class ThzSystemSettingCfgMgr(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(ThzSystemSettingCfgMgr, self).__init__(parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.LoadSysConfigInfo()
        self.btnCfgImport.clicked.connect(self.OnBtnCfgImportClicked)
        self.btnCfgExport.clicked.connect(self.OnBtnCfgExportClicked)
        self.chkAll.clicked.connect(lambda: self.OnCheckAllClicked(self.chkAll.isChecked()))

    def OnCheckAllClicked(self, isChecked):
        count = self.listWidgetSysCfg.count()
        # 遍历listwidget中的内容
        for i in range(count):
            widget = self.listWidgetSysCfg.itemWidget(self.listWidgetSysCfg.item(i))
            widget.checkBox.setChecked(isChecked)

    def OnBtnCfgExportClicked(self):
        print("Export!")

    def OnBtnCfgImportClicked(self):
        print("Import!")

    def AddSysCfgItem(self, data):
        c = self.gbxSysCfgTableHeader.children()
        widget = SysCfgTableItem(c)
        widget.lblName.setText(str(data.Name))
        FixString(widget.lblName)
        widget.lblFileType.setText(str(data.Type))
        FixString(widget.lblFileType)
        widget.lblComment.setText(str(data.Comment))
        FixString(widget.lblComment)
        widget.Id = data.Id
        item = QListWidgetItem()
        item.setSizeHint(widget.sizeHint())
        widget.exportClicked.connect(lambda: self.OnSysCfgListWidgetExportBtnClicked(item))

        self.listWidgetSysCfg.addItem(item)
        self.listWidgetSysCfg.setItemWidget(item, widget)

    def OnSysCfgListWidgetExportBtnClicked(self, item):
        print("export!")

    # 加载用户信息
    def LoadSysConfigInfo(self):
        data = SysConfig().select()
        for item in data:
            self.AddSysCfgItem(item)
