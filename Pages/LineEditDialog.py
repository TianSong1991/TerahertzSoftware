from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Common.DialogEx import DialogEx
import globalvar as gl


class LineEditDialog(DialogEx):
    def __init__(self):
        super(LineEditDialog, self).__init__(None)
        self.set2BtnMode()
        self.content = QWidget()
        self.gridLayout = QGridLayout(self.content)
        self.gridLayout.setContentsMargins(0, 20, 0, 0)
        self.gridLayout.setColumnStretch(0, 15)
        self.gridLayout.setColumnStretch(1, 5)
        self.gridLayout.setColumnStretch(2, 3)
        self.gridLayout.setColumnStretch(3, 1)
        self.gridLayout.addWidget(QLabel('名称', self.content), 0, 0, 1, 1)
        self.gridLayout.addWidget(QLabel('厚度', self.content), 0, 1, 1, 1)
        self.gridLayout.addWidget(QLabel('操作', self.content), 0, 2, 1, 1)
        self.gridLayout.addWidget(QLabel('隐藏', self.content), 0, 3, 1, 1)
        self.setContent(self.content)

    @pyqtSlot()
    def on_btnOk_clicked(self):
        self.done(QDialog.Accepted)

    def delSamLine(self, status):
        index = self.sender().property('index')
        ctrl1 = self.gridLayout.itemAtPosition(index, 0).widget()
        ctrl2 = self.gridLayout.itemAtPosition(index, 1).widget()
        ctrl3 = self.gridLayout.itemAtPosition(index, 2).widget()
        ctrl4 = self.gridLayout.itemAtPosition(index, 3).widget()
        self.gridLayout.removeWidget(ctrl1)
        self.gridLayout.removeWidget(ctrl2)
        self.gridLayout.removeWidget(ctrl3)
        self.gridLayout.removeWidget(ctrl4)
        ctrl1.deleteLater()
        ctrl2.deleteLater()
        ctrl3.deleteLater()
        ctrl4.deleteLater()

