from PyQt5 import QtWidgets
from PyQt5.Qt import *
from PyQt5.QtWidgets import QWidget


class PreAddItem(QWidget):
    cancelClicked = pyqtSignal([QWidget])
    saveClicked = pyqtSignal([QWidget])
    Id = 0
    def __init__(self, parent=None):
        super(PreAddItem, self).__init__(parent)
        self.hLayout = QtWidgets.QHBoxLayout()
        self.hLayout.setContentsMargins(0, 0, 0, 0)
        self.hLayout.setObjectName("hLayout")
        self.gbxOpt = QtWidgets.QGroupBox()
        self.gbxOpt.setContentsMargins(0, 0, 0, 0)
        self.gbxOpt.setMinimumWidth(80)
        self.gbxOpt.setMaximumWidth(80)
        self.gbxOpt.setMaximumHeight(25)
        self.gbxOpt.setMinimumHeight(25)
        self.hboxOpt = QHBoxLayout(self.gbxOpt)

        self.hboxOpt.setContentsMargins(0, 0, 0, 0)
        self.txtName = QtWidgets.QLineEdit()
        self.txtName.setObjectName("txtName")
        self.txtName.setMaximumHeight(25)
        self.txtName.setMinimumHeight(25)
        self.hLayout.addWidget(self.txtName)
        self.btnSave = QtWidgets.QPushButton(self.gbxOpt)
        self.btnSave.setObjectName("btnSave")
        self.btnSave.setText("保存")
        self.btnSave.setMaximumHeight(25)
        self.btnSave.setMinimumHeight(25)
        self.hboxOpt.addWidget(self.btnSave)
        self.btnCancel = QtWidgets.QPushButton(self.gbxOpt)
        self.btnCancel.setObjectName("btnCancel")
        self.btnCancel.setText("取消")
        self.btnCancel.setMaximumHeight(25)
        self.btnCancel.setMinimumHeight(25)
        self.hboxOpt.addWidget(self.btnCancel)

        self.hLayout.addWidget(self.gbxOpt)
        self.setLayout(self.hLayout)

        self.btnCancel.clicked.connect(self.OnCancelClicked)
        self.btnSave.clicked.connect(self.OnSaveClicked)

    def OnCancelClicked(self):
        self.cancelClicked[QWidget].emit(self)

    def OnSaveClicked(self):
        self.saveClicked[QWidget].emit(self)


# 设置自定义table表头
class AddedItem(QWidget):
    deleteClicked = pyqtSignal([QWidget])
    addClicked = pyqtSignal([QWidget])
    Id = 0
    def __init__(self, parent=None):
        super(AddedItem, self).__init__(parent)
        self.hLayout = QtWidgets.QHBoxLayout()
        self.hLayout.setContentsMargins(0, 0, 0, 0)
        self.hLayout.setObjectName("hLayout")

        self.gbxOpt = QtWidgets.QGroupBox()
        self.gbxOpt.setContentsMargins(0, 0, 0, 0)
        self.gbxOpt.setMinimumWidth(80)
        self.gbxOpt.setMaximumWidth(80)
        self.gbxOpt.setMaximumHeight(25)
        self.gbxOpt.setMinimumHeight(25)
        self.hboxOpt = QHBoxLayout(self.gbxOpt)
        self.hboxOpt.setContentsMargins(0, 0, 0, 0)

        self.lblName = QtWidgets.QLabel()
        self.lblName.setObjectName("lblName")
        self.lblName.setMaximumHeight(25)
        self.lblName.setMinimumHeight(25)
        self.hLayout.addWidget(self.lblName)
        self.btnAdd = QtWidgets.QPushButton(self.gbxOpt)
        self.btnAdd.setMaximumHeight(25)
        self.btnAdd.setMinimumHeight(25)
        self.btnAdd.setObjectName("btnAdd")
        self.btnAdd.setText("添加")
        self.hboxOpt.addWidget(self.btnAdd)
        self.btnDel = QtWidgets.QPushButton(self.gbxOpt)
        self.btnDel.setMaximumHeight(25)
        self.btnDel.setMinimumHeight(25)
        self.btnDel.setObjectName("btnDel")
        self.btnDel.setText("删除")
        self.hboxOpt.addWidget(self.btnDel)

        self.hLayout.addWidget(self.gbxOpt)
        self.setLayout(self.hLayout)

        self.btnDel.clicked.connect(self.OnDeleteClicked)
        self.btnAdd.clicked.connect(self.OnAddClicked)

    def OnDeleteClicked(self):
        self.deleteClicked[QWidget].emit(self)

    def OnAddClicked(self):
        self.addClicked[QWidget].emit(self)
