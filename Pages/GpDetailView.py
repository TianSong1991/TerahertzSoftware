from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Ui.UiGpDetailView import Ui_UiGpDetailView


class GpDetailView(QWidget, Ui_UiGpDetailView):
    def __init__(self, parent=None):
        super(GpDetailView, self).__init__(parent)
        self.setupUi(self)
        self.retranslateUi(self)