from PyQt5 import QtGui

from Common.DialogEx import DialogEx
from Common.UserTableItem import *
# 增加用户弹框
from Entity.models import Role, User


# 添加用户信息窗体
class RoleAddDialogForm(DialogEx):
    Id = 0
    Row = -1
    Rights = {}

    def __init__(self):
        super(RoleAddDialogForm, self).__init__(None)
        self.set1BtnMode()
        self.content = QWidget()
        self.content.setStyleSheet('''
            #txtComment{background-color: #FFEBEBEB;border:none;}
            #txtRoleName{background-color: #FFEBEBEB;}
        ''')
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layoutWidget = QWidget(self.content)
        self.layoutWidget.setGeometry(QtCore.QRect(80, 30, 331, 201))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        self.txtComment = QPlainTextEdit(self.layoutWidget)
        self.txtComment.setMinimumSize(QtCore.QSize(0, 100))
        self.txtComment.setMaximumSize(QtCore.QSize(16777215, 100))
        self.txtComment.setObjectName("txtComment")
        self.gridLayout.addWidget(self.txtComment, 1, 1, 1, 1)
        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("角  色:")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_5 = QLabel(self.layoutWidget)
        self.label_5.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_5.setObjectName("label_5")
        self.label_5.setText("备  注:")
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.txtRoleName = QLineEdit(self.layoutWidget)
        self.txtRoleName.setMaximumSize(QtCore.QSize(16777215, 35))
        self.txtRoleName.setText("")
        self.txtRoleName.setObjectName("txtRoleName")
        self.gridLayout.addWidget(self.txtRoleName, 0, 1, 1, 1)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.lblTitle.setText("角色添加")
        self.setContent(self.content)
        self.resize(550, 400)


    def Clear(self):
        self.txtComment.setPlainText("")
        self.txtRoleName.setText("")
