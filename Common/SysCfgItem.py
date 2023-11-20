# 左侧
from PyQt5.Qt import *
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QCheckBox, QGroupBox
from PyQt5 import QtCore

# 设置自定义table表头
class SysCfgTableItem(QWidget):
    exportClicked = pyqtSignal([QWidget])
    Id = 0
    def __init__(self,controls, parent=None):
        super(SysCfgTableItem, self).__init__(parent)
        self.setObjectName("item")
        # 复选框
        self.checkBox = QCheckBox()
        self.checkBox.setMaximumWidth(40)
        self.checkBox.setMaximumHeight(20)
        self.checkBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblName = QLabel()
        self.lblFileType = QLabel()
        self.lblComment = QLabel()
        # 操作
        self.gpxOptional = QGroupBox()
        self.gpxOptional.setStyleSheet('''background-color: transparent;''')
        self.hboxOpt = QHBoxLayout(self.gpxOptional)
        self.hboxOpt.setContentsMargins(0, 0, 0, 0)

        self.btnExport = QPushButton(self.gpxOptional)
        self.btnExport.setText("导出")
        self.btnExport.setObjectName("optExport")
        self.hboxOpt.addWidget(self.btnExport)

        # 设置布局用来对nameLabel和avatorLabel进行布局
        self.hbox = QHBoxLayout()
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.setSpacing(0)
        self.checkBox.setMaximumWidth(controls[1].maximumWidth())
        self.checkBox.setMinimumWidth(controls[1].minimumWidth())
        self.hbox.addWidget(self.checkBox)
        self.lblName.setMaximumWidth(controls[2].maximumWidth())
        self.lblName.setMinimumWidth(controls[2].minimumWidth())
        self.hbox.addWidget(self.lblName)
        self.lblFileType.setMaximumWidth(controls[3].maximumWidth())
        self.lblFileType.setMinimumWidth(controls[3].minimumWidth())
        self.hbox.addWidget(self.lblFileType)
        self.lblComment.setMaximumWidth(controls[4].maximumWidth())
        self.lblComment.setMinimumWidth(controls[4].minimumWidth())
        self.hbox.addWidget(self.lblComment)
        self.gpxOptional.setMaximumWidth(controls[5].maximumWidth())
        self.gpxOptional.setMinimumWidth(controls[5].minimumWidth())
        self.hbox.addWidget(self.gpxOptional)
        # 设置widget的布局
        self.setLayout(self.hbox)
        self.btnExport.clicked.connect(self.OnExportBtnClicked)

    def OnExportBtnClicked(self):
        self.exportClicked[QWidget].emit(self)

