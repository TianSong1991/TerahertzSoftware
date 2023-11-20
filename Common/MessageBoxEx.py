from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        Form.resize(420, 250)
        Form.setStyleSheet("QGroupBox{border:1px solid #FF00A3DA;}"
                           "#lblTitle{color:white;}"
                           "QWidget{background-color: #FFFFFFFF;color:#FF4D4D4D}"
                           "QPushButton{background-color:#FF00A3DA;color:#FFFFFFFF;border:none;}"
                           "QPushButton:hover{background-color:#8F00A3DA;}"
                           "QPushButton:disabled{background-color:#FFB1B1B1;}")

        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.gbxContent = QGroupBox(Form)
        self.gbxContent.setContentsMargins(0, 0, 0, 0)
        self.gbxContent.setTitle("")
        self.gbxContent.setObjectName("gbxContent")
        self.horizontalLayout.addWidget(self.gbxContent)

        self.verticalLayout = QVBoxLayout(self.gbxContent)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.widget = QWidget(self.gbxContent)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QSize(0, 50))
        self.widget.setMaximumSize(QSize(16777215, 50))
        self.widget.setStyleSheet("background-color: #FF00A3DA;")
        self.horizontalLayout = QHBoxLayout(self.widget)
        spacerItem = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.lblTitle = QLabel('温馨提示', self.widget)
        self.lblTitle.setObjectName("lblTitle")
        self.horizontalLayout.addWidget(self.lblTitle)
        spacerItem1 = QSpacerItem(294, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btnClose = QPushButton('r', self.widget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnClose.sizePolicy().hasHeightForWidth())
        self.btnClose.setSizePolicy(sizePolicy)
        self.btnClose.setMinimumSize(QSize(28, 28))
        self.btnClose.setMaximumSize(QSize(28, 28))
        self.btnClose.setStyleSheet("QPushButton{background-color:#FF00A3DA; font-family:'Webdings'; font-size:16pt;"
                                    "color:white;border:none;} QPushButton:hover{background-color:Red; color: white;}")
        self.btnClose.setObjectName("btnClose")
        self.horizontalLayout.addWidget(self.btnClose)
        self.verticalLayout.addWidget(self.widget)
        self.widget2 = QWidget(self.gbxContent)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget2.sizePolicy().hasHeightForWidth())
        self.widget2.setSizePolicy(sizePolicy)
        self.widget2.setMinimumSize(QSize(0, 0))
        self.widget2.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout3 = QHBoxLayout(self.widget2)
        spacerItem2 = QSpacerItem(38, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.horizontalLayout3.addItem(spacerItem2)
        self.lblMsg = QLabel(self.widget2)
        self.lblMsg.setMaximumSize(QSize(400, 16777215))
        self.lblMsg.setAlignment(Qt.AlignCenter)
        self.lblMsg.setWordWrap(False)
        self.horizontalLayout3.addWidget(self.lblMsg)
        spacerItem3 = QSpacerItem(38, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.horizontalLayout3.addItem(spacerItem3)
        self.verticalLayout.addWidget(self.widget2)
        self.widget3 = QWidget(self.gbxContent)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget3.sizePolicy().hasHeightForWidth())
        self.widget3.setSizePolicy(sizePolicy)
        self.widget3.setMinimumSize(QSize(0, 80))
        self.widget3.setMaximumSize(QSize(16777215, 80))
        self.horizontalLayout2 = QHBoxLayout(self.widget3)
        spacerItem4 = QSpacerItem(114, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout2.addItem(spacerItem4)
        self.btnOk = QPushButton('确　定', self.widget3)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(32)
        sizePolicy.setHeightForWidth(self.btnOk.sizePolicy().hasHeightForWidth())
        self.btnOk.setSizePolicy(sizePolicy)
        self.btnOk.setMinimumSize(QSize(90, 32))
        self.btnOk.setObjectName("btnOk")
        self.horizontalLayout2.addWidget(self.btnOk)
        spacerItem5 = QSpacerItem(60, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontalLayout2.addItem(spacerItem5)
        self.btnCancel = QPushButton('取　消', self.widget3)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(32)
        sizePolicy.setHeightForWidth(self.btnCancel.sizePolicy().hasHeightForWidth())
        self.btnCancel.setSizePolicy(sizePolicy)
        self.btnCancel.setMinimumSize(QSize(90, 32))
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout2.addWidget(self.btnCancel)
        spacerItem6 = QSpacerItem(115, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout2.addItem(spacerItem6)
        self.verticalLayout.addWidget(self.widget3)
        QMetaObject.connectSlotsByName(Form)


class MessageBoxEx(QDialog, Ui_Form):
    def __init__(self):
        super(MessageBoxEx, self).__init__(None)
        self.dragPos = None
        self.dragEnable = False
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_AttributeCount)
        self.setWindowModality(Qt.ApplicationModal)
        self.widget.installEventFilter(self)  # 初始化事件过滤器
        self.widget2.installEventFilter(self)
        self.widget3.installEventFilter(self)

    @pyqtSlot()
    def on_btnClose_clicked(self):
        self.done(-1)

    @pyqtSlot()
    def on_btnOk_clicked(self):
        self.done(QDialog.Accepted)

    @pyqtSlot()
    def on_btnCancel_clicked(self):
        self.done(QDialog.Rejected)

    def eventFilter(self, obj, event):
        # 事件过滤器,用于解决鼠标进入其它控件后还原为标准鼠标样式
        if isinstance(event, QEnterEvent):
            self.setCursor(Qt.ArrowCursor)
        return super(MessageBoxEx, self).eventFilter(obj, event)  # 注意 ,MessageBoxEx是所在类的名称
        # return QWidget.eventFilter(self, obj, event)  # 用这个也行，但要注意修改窗口类型

    def mousePressEvent(self, event) -> None:
        if (event.button() == Qt.LeftButton) and (event.y() < self.widget.height()):
            # 鼠标左键点击标题栏区域
            self.dragEnable = True
            self.dragPos = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event) -> None:
        if Qt.LeftButton and self.dragEnable:
            # 标题栏拖放窗口位置
            self.move(event.globalPos() - self.dragPos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.dragEnable = False

    def __setInfo(self, message, title, okTitle, cancelTitle):

        self.lblTitle.setText('温馨提示' if len(title) == 0 else title)
        self.lblMsg.setText(message)
        if len(okTitle) == 0:
            self.btnOk.setText("确定")
        else:
            self.btnOk.setText(okTitle)

        if len(cancelTitle) == 0:
            self.btnCancel.setVisible(False)
            self.horizontalLayout2.removeItem(self.horizontalLayout2.itemAt(2))
        else:
            self.btnCancel.setText(cancelTitle)

    @staticmethod
    def show(message, title='', okStr='', cancelStr=''):
        dlg = MessageBoxEx()
        dlg.__setInfo(message, title, okStr, cancelStr)
        return dlg.exec_()