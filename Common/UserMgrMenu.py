#左侧
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout
from PyQt5 import QtCore

class MenuQListWidgetItem(QWidget):
    def __init__(self, parent=None):
        super(MenuQListWidgetItem,self).__init__(parent)
        self.nameLabel = QLabel()
        self.avatorLabel = QLabel()
        self.nameLabel.setObjectName("lblName")

        # 设置布局用来对nameLabel和avatorLabel进行布局
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.avatorLabel)
        self.hbox.addWidget(self.nameLabel)
        # 设置widget的布局
        self.setLayout(self.hbox)
        # self.nameLabel.setStyleSheet('''
        #           font: 12pt;
        #           color:#FF4D4D4D;
        # ''')
        self.avatorLabel.setMaximumWidth(25)
        self.avatorLabel.setMaximumHeight(25)

    def setTextUp(self, text):
        self.nameLabel.setText(text)

    def getText(self):
        return self.nameLabel.text()

    def setIcon(self, imagePath):
        self.avatorLabel.setScaledContents(True)
        self.avatorLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.avatorLabel.setPixmap(QPixmap(imagePath))