from PyQt5 import QtGui

from Common.DialogEx import DialogEx
from Common.UserTableItem import *
# 增加用户弹框
from Entity.models import Role, User


# 添加用户信息窗体
class UserAddDialogForm(DialogEx):
    Id = 0
    Row = -1

    def __init__(self):
        super(UserAddDialogForm, self).__init__(None)
        self.set1BtnMode()
        self.content = QWidget()
        self.content.setStyleSheet('''
            #txtComment{border:none;background-color: #FFEBEBEB;}
            #cbxRole{border:none;background-color: #FFEBEBEB;}
        ''')
        self.verticalLayout = QVBoxLayout(self.content)
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layoutWidget = QWidget(self.content)
        self.layoutWidget.setGeometry(QtCore.QRect(80, 10, 331, 311))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_4.setObjectName("label_4")
        self.label_4.setText("角色:")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("姓名:")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.cbxRole = QComboBox(self.layoutWidget)
        self.cbxRole.setMinimumSize(QtCore.QSize(0, 35))
        self.cbxRole.setMaximumSize(QtCore.QSize(16777215, 35))
        self.cbxRole.setStyleSheet("")
        self.cbxRole.setObjectName("cbxRole")
        self.gridLayout.addWidget(self.cbxRole, 2, 1, 1, 1)
        self.txtUserName = QLineEdit(self.layoutWidget)
        self.txtUserName.setMaximumSize(QtCore.QSize(16777215, 35))
        self.txtUserName.setStyleSheet("")
        self.txtUserName.setText("")
        self.txtUserName.setObjectName("txtUserName")
        self.gridLayout.addWidget(self.txtUserName, 0, 1, 1, 1)
        self.txtPhone = QLineEdit(self.layoutWidget)
        self.txtPhone.setMinimumSize(QtCore.QSize(0, 35))
        self.txtPhone.setMaximumSize(QtCore.QSize(16777215, 35))
        self.txtPhone.setStyleSheet("")
        self.txtPhone.setText("")
        self.txtPhone.setObjectName("txtPhone")
        self.gridLayout.addWidget(self.txtPhone, 1, 1, 1, 1)
        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_3.setObjectName("label_3")
        self.label_3.setText("电话:")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_5 = QLabel(self.layoutWidget)
        self.label_5.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_5.setObjectName("label_5")
        self.label_5.setText("备注:")
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)
        self.txtComment = QPlainTextEdit(self.layoutWidget)
        self.txtComment.setMinimumSize(QtCore.QSize(0, 80))
        self.txtComment.setMaximumSize(QtCore.QSize(16777215, 80))
        self.txtComment.setObjectName("txtComment")
        self.gridLayout.addWidget(self.txtComment, 3, 1, 1, 1)

        self.lblTitle.setText("添加用户")
        self.setContent(self.content)
        self.resize(550, 460)
        self.LoadAndBindRoleData()

    def Clear(self):
        self.txtUserName.setText("")
        self.txtPhone.setText("")
        self.txtComment.setPlainText("")
        self.cbxRole.setCurrentIndex(0)

    # 绑定角色数据
    def LoadAndBindRoleData(self):
        roles = Role().select()
        if roles is not None:
            for r in roles:
                self.cbxRole.addItem(r.Name, r)
