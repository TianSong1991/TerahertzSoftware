from PyQt5.QtWidgets import *

from Common.MessageBoxEx import MessageBoxEx
from Entity.models import Setting, SettingKey
from Ui.UiSysParamsSetting import Ui_Form


class ThzSysParamsSetting(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(ThzSysParamsSetting, self).__init__(parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.cbxLogSaveTime.setView(QListView())
        self.cbxDataSaveTime.setView(QListView())
        self.cbxDataBaseVer.setView(QListView())
        self.btnSave.clicked.connect(self.OnBtnSaveClicked)
        self.LoadConfig()

    def LoadConfig(self):
        data = Setting.select().where(Setting.ConfigKey == SettingKey)
        if len(data) > 0:
            self.cbxLogSaveTime.setCurrentText(data[0].LogSaveTime)
            self.cbxDataSaveTime.setCurrentText(data[0].DataSaveTime)
            self.cbxDataBaseVer.setCurrentText(data[0].DataBaseType)
            self.txtDataSavePath.setText(data[0].DataSavePath)
        else:
            Setting.replace({Setting.ConfigKey: SettingKey, Setting.LogSaveTime: "一周", Setting.DataSaveTime: "一周",
                             Setting.DataSavePath: "", Setting.DataBaseType: "光谱"}).execute()

    def OnBtnSaveClicked(self):
        Setting.update({Setting.LogSaveTime: self.cbxLogSaveTime.currentText(),
                        Setting.DataSaveTime: self.cbxDataSaveTime.currentText(),
                        Setting.DataBaseType: self.cbxDataBaseVer.currentText(),
                        Setting.DataSavePath: self.txtDataSavePath.text()}).execute()
        MessageBoxEx.show("保存成功", "提示", "确定")
