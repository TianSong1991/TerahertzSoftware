import thzres_rc
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class LoadingWidget(QDialog):
    def __init__(self, message, parent=None):
        super(LoadingWidget, self).__init__(parent)
        self.setStyleSheet("QGroupBox{border:1px solid #FF00A3DA;}"
                           "QWidget{background-color:#FFFFFFFF;color:#FF4D4D4D;}")
        self.vLayout = QVBoxLayout(self)
        self.vLayout.setContentsMargins(0, 0, 0, 0)
        self.gbxContent = QGroupBox(self)
        self.vLayout.addWidget(self.gbxContent)

        hLayout = QHBoxLayout(self.gbxContent)
        hLayout.setSpacing(15)
        hSpacer1 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        hLayout.addItem(hSpacer1)

        lblGif = QLabel('i', self)
        lblGif.setFixedSize(40, 40)
        hLayout.addWidget(lblGif)

        movie = QMovie(":/Image/circle.gif")
        lblGif.setMovie(movie)

        lblInfo = QLabel(message, self)
        hLayout.addWidget(lblInfo)

        hSpacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum);
        hLayout.addItem(hSpacer2)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_AttributeCount)
        self.setWindowModality(Qt.ApplicationModal)
        movie.start()

    def showDialog(self):
        self.exec_()

    def close(self):
        self.done(QDialog.Accepted)

