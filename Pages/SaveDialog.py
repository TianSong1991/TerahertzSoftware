import datetime
from Entity.models import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Common.DialogEx import DialogEx
import globalvar as gl


class SaveDialog(DialogEx):
    def __init__(self):
        super(SaveDialog, self).__init__(None)
        self.set2BtnMode()
        self.content = QWidget()
        self.gridLayout = QGridLayout(self.content)
        self.label = QLabel('样品类型', self.content)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.txtType = QComboBox(self.content)
        self.txtType.setStyleSheet("background-color: #FFEBEBEB; border:none;")
        self.gridLayout.addWidget(self.txtType, 0, 1, 1, 1)
        self.txtType.currentIndexChanged.connect(self.onSelectedChanged)

        self.label_2 = QLabel('样品名称', self.content)

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.txtName = QLineEdit(self.content)

        self.gridLayout.addWidget(self.txtName, 1, 1, 1, 1)
        self.setContent(self.content)
        self.SetTypeData()
        self.resize(380, 250)

    @pyqtSlot()
    def on_btnOk_clicked(self):
        if gl.isStrNoneOrEmpty(self.txtName.text()) \
                or self.txtType.currentIndex() == -1:
            return

        self.done(QDialog.Accepted)

    def SetTypeData(self):
        arr = SampleType.select().where(SampleType.Id > 0)
        for item in arr:
            item.save()
            self.txtType.addItem(item.Name, item)
        self.txtType.setCurrentIndex(-1)

    def onSelectedChanged(self, index):
        if index == -1:
            self.txtName.setText('')
            return
        data = self.txtType.currentData()
        nowStr = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.txtName.setText(f'{data.Name}_{nowStr}')
        self.txtType.setProperty('id', data.Id)
