from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Common.DialogEx import DialogEx


class DataEditDialog(DialogEx):
    def __init__(self):
        self.isDataChanged = False
        self.onOtherBtnEvent = None
        super(DataEditDialog, self).__init__(None)
        self.set3BtnMode('保　存', '还　原', '确　定', False)
        self.content = QWidget()
        vLayout = QVBoxLayout(self.content)
        vLayout.setContentsMargins(0, 0, 0, 0)
        hLayout1 = QHBoxLayout()
        hLayout1.addWidget(QLabel("开始位置：", self.content))
        self.txtStart = QLineEdit(self.content)
        hLayout1.addWidget(self.txtStart)
        vLayout.addLayout(hLayout1)

        hLayout2 = QHBoxLayout()
        hLayout2.addWidget(QLabel("结束位置：", self.content))
        self.txtEnd = QLineEdit(self.content)
        hLayout2.addWidget(self.txtEnd)
        vLayout.addLayout(hLayout2)
        self.setContent(self.content)
        self.resize(400, 250)

    def setRange(self, start, end):
        self.txtStart.setText(f'{start}')
        self.txtEnd.setText(f'{end}')

    def getRange(self):
        return float(self.txtStart.text()), float(self.txtEnd.text())

    @pyqtSlot()
    def on_btnOther_clicked(self):
        if self.onOtherBtnEvent is not None:
            start = int(self.txtStart.text())
            end = int(self.txtEnd.text())
            self.onOtherBtnEvent(start, end)
