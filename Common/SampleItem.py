# 左侧
from PyQt5.Qt import *
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QCheckBox, QGroupBox
from PyQt5 import QtCore


# 设置自定义table表头
class SampleItem(QWidget):
    deleteClicked = pyqtSignal([QWidget])
    viewClicked = pyqtSignal([QWidget])

    Id = 0

    def __init__(self, controls, parent=None):
        super(SampleItem, self).__init__(parent)
        self.setObjectName("item")
        # 复选框
        self.checkBox = QCheckBox()
        self.checkBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        # 角色
        self.lblNo = QLabel()
        self.lblName = QLabel()
        self.lblAddDate = QLabel()
        # 备注
        self.lblComment = QLabel()
        # 操作
        self.gpxOptional = QGroupBox()
        self.gpxOptional.setStyleSheet('''background-color: transparent;''')
        self.hboxOpt = QHBoxLayout(self.gpxOptional)
        self.hboxOpt.setContentsMargins(0, 0, 0, 0)

        self.btnDel = QPushButton(self.gpxOptional)
        self.btnView = QPushButton(self.gpxOptional)
        self.btnDel = QPushButton(self.gpxOptional)
        self.btnView.setText("详情")
        self.btnView.setObjectName("optView")

        self.btnDel.setText("删除")
        self.btnDel.setObjectName("optDel")
        self.hboxOpt.addWidget(self.btnView)
        self.hboxOpt.addWidget(self.btnDel)

        # 设置布局用来对nameLabel和avatorLabel进行布局
        self.hbox = QHBoxLayout()
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.setSpacing(0)
        self.checkBox.setMaximumWidth(controls[1].maximumWidth())
        self.checkBox.setMinimumWidth(controls[1].minimumWidth())
        self.hbox.addWidget(self.checkBox)
        self.lblNo.setMaximumWidth(controls[2].maximumWidth())
        self.lblNo.setMinimumWidth(controls[2].minimumWidth())
        self.hbox.addWidget(self.lblNo)
        self.lblName.setMaximumWidth(controls[3].maximumWidth())
        self.lblName.setMinimumWidth(controls[3].minimumWidth())
        self.hbox.addWidget(self.lblName)
        self.lblAddDate.setMaximumWidth(controls[4].maximumWidth())
        self.lblAddDate.setMinimumWidth(controls[4].minimumWidth())
        self.hbox.addWidget(self.lblAddDate)
        self.lblComment.setMaximumWidth(controls[5].maximumWidth())
        self.lblComment.setMinimumWidth(controls[5].minimumWidth())
        self.hbox.addWidget(self.lblComment)
        self.gpxOptional.setMaximumWidth(controls[6].maximumWidth())
        self.gpxOptional.setMinimumWidth(controls[6].minimumWidth())
        self.hbox.addWidget(self.gpxOptional)
        # 设置widget的布局
        self.setLayout(self.hbox)
        self.btnDel.clicked.connect(self.OnDeleteBtnClicked)
        self.btnView.clicked.connect(self.OnViewClicked)

    def OnDeleteBtnClicked(self):
        self.deleteClicked[QWidget].emit(self)

    def OnViewClicked(self):
        self.viewClicked[QWidget].emit(self)
