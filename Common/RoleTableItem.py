# 左侧
from PyQt5.Qt import *
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QCheckBox, QGroupBox
from PyQt5 import QtCore


# 设置自定义table表头
class RoleTableItem(QWidget):
    deleteClicked = pyqtSignal([QWidget])
    editClicked = pyqtSignal([QWidget])
    rightClicked = pyqtSignal([QWidget])
    Id = 0

    def __init__(self,controls, parent=None):
        super(RoleTableItem, self).__init__(parent)
        # 复选框
        self.checkBox = QCheckBox()
        self.checkBox.setMaximumWidth(40)
        self.checkBox.setMaximumHeight(20)
        self.checkBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        # 角色
        self.roleLabel = QLabel()
        # 备注
        self.commentLabel = QLabel()
        # 操作
        self.gpxOptional = QGroupBox()
        self.gpxOptional.setContentsMargins(0, 0, 0, 0)
        self.gpxOptional.setStyleSheet('''background-color: transparent;''')
        self.hboxOpt = QHBoxLayout(self.gpxOptional)
        self.hboxOpt.setContentsMargins(0, 0, 0, 0)
        self.editBtn = QPushButton(self.gpxOptional)
        self.rightBtn = QPushButton(self.gpxOptional)
        self.deleteBtn = QPushButton(self.gpxOptional)
        self.editBtn.setText("修改")
        self.editBtn.setObjectName("optEdit")
        self.rightBtn.setText("权限分配")
        self.rightBtn.setObjectName("optRight")
        self.deleteBtn.setText("删除")
        self.deleteBtn.setObjectName("optDel")
        self.roleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.commentLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.hboxOpt.addWidget(self.editBtn)
        self.hboxOpt.addWidget(self.rightBtn)
        self.hboxOpt.addWidget(self.deleteBtn)
        # 设置布局用来对nameLabel和avatorLabel进行布局
        self.hbox = QHBoxLayout()
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.setSpacing(0)
        self.checkBox.setMaximumWidth(controls[1].maximumWidth())
        self.checkBox.setMinimumWidth(controls[1].minimumWidth())
        self.hbox.addWidget(self.checkBox)
        self.roleLabel.setMaximumWidth(controls[2].maximumWidth())
        self.roleLabel.setMinimumWidth(controls[2].minimumWidth())
        self.hbox.addWidget(self.roleLabel)
        self.commentLabel.setMaximumWidth(controls[3].maximumWidth())
        self.commentLabel.setMinimumWidth(controls[3].minimumWidth())
        self.hbox.addWidget(self.commentLabel)
        self.gpxOptional.setMaximumWidth(controls[4].maximumWidth())
        self.gpxOptional.setMinimumWidth(controls[4].minimumWidth())
        self.hbox.addWidget(self.gpxOptional)
        # 设置widget的布局
        self.setLayout(self.hbox)
        self.deleteBtn.clicked.connect(self.OnDeleteBtnClicked)
        self.editBtn.clicked.connect(self.OnEditBtnClicked)
        self.rightBtn.clicked.connect(self.OnRightBtnClicked)

    def OnDeleteBtnClicked(self):
        self.deleteClicked[QWidget].emit(self)

    def OnEditBtnClicked(self):
        self.editClicked[QWidget].emit(self)

    def OnRightBtnClicked(self):
        self.rightClicked[QWidget].emit(self)
