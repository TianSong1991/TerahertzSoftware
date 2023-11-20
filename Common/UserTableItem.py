# 左侧
from PyQt5.Qt import *
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QCheckBox, QGroupBox
from PyQt5 import QtCore

# 设置自定义table表头
class UserTableItem(QWidget):
    deleteClicked = pyqtSignal([QWidget])
    editClicked = pyqtSignal([QWidget])
    resetClicked = pyqtSignal([QWidget])
    Id = 0
    RoleId = 0
    def __init__(self,controls, parent=None):
        super(UserTableItem, self).__init__(parent)
        self.setObjectName("item")
        # 复选框
        self.checkBox = QCheckBox()
        self.checkBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        # 角色
        self.nameLabel = QLabel()
        self.phoneLabel = QLabel()
        self.roleLabel = QLabel()
        # 备注
        self.commentLabel = QLabel()
        # 操作
        self.gpxOptional = QGroupBox()
        self.gpxOptional.setStyleSheet('''background-color: transparent;''')
        self.hboxOpt = QHBoxLayout(self.gpxOptional)
        self.hboxOpt.setContentsMargins(0, 0, 0, 0)

        self.editBtn = QPushButton(self.gpxOptional)
        self.resetPwdBtn = QPushButton(self.gpxOptional)
        self.deleteBtn = QPushButton(self.gpxOptional)
        self.editBtn.setText("修改")
        self.editBtn.setObjectName("optEdit")
        self.resetPwdBtn.setText("重置密码")
        self.resetPwdBtn.setObjectName("optResetPwd")
        self.deleteBtn.setText("删除")
        self.deleteBtn.setObjectName("optDel")
        self.hboxOpt.addWidget(self.editBtn)
        self.hboxOpt.addWidget(self.resetPwdBtn)
        self.hboxOpt.addWidget(self.deleteBtn)
        self.nameLabel.setAlignment(Qt.AlignCenter)
        self.phoneLabel.setAlignment(Qt.AlignCenter)
        self.commentLabel.setAlignment(Qt.AlignCenter)
        self.roleLabel.setAlignment(Qt.AlignCenter)

        # 设置布局用来对nameLabel和avatorLabel进行布局
        self.hbox = QHBoxLayout()
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.setSpacing(0)
        self.checkBox.setMaximumWidth(controls[1].maximumWidth())
        self.checkBox.setMinimumWidth(controls[1].minimumWidth())
        self.hbox.addWidget(self.checkBox)
        self.nameLabel.setMaximumWidth(controls[2].maximumWidth())
        self.nameLabel.setMinimumWidth(controls[2].minimumWidth())
        self.hbox.addWidget(self.nameLabel)
        self.phoneLabel.setMaximumWidth(controls[3].maximumWidth())
        self.phoneLabel.setMinimumWidth(controls[3].minimumWidth())
        self.hbox.addWidget(self.phoneLabel)
        self.roleLabel.setMaximumWidth(controls[4].maximumWidth())
        self.roleLabel.setMinimumWidth(controls[4].minimumWidth())
        self.hbox.addWidget(self.roleLabel)
        self.commentLabel.setMaximumWidth(controls[5].maximumWidth())
        self.commentLabel.setMinimumWidth(controls[5].minimumWidth())
        self.hbox.addWidget(self.commentLabel)
        self.gpxOptional.setMaximumWidth(controls[6].maximumWidth())
        self.gpxOptional.setMinimumWidth(controls[6].minimumWidth())
        self.hbox.addWidget(self.gpxOptional)
        # 设置widget的布局
        self.setLayout(self.hbox)
        self.deleteBtn.clicked.connect(self.OnDeleteBtnClicked)
        self.editBtn.clicked.connect(self.OnEditBtnClicked)
        self.resetPwdBtn.clicked.connect(self.OnResetPwdBtnClicked)

    def OnDeleteBtnClicked(self):
        self.deleteClicked[QWidget].emit(self)

    def OnEditBtnClicked(self):
        self.editClicked[QWidget].emit(self)

    def OnResetPwdBtnClicked(self):
        self.resetClicked[QWidget].emit(self)
