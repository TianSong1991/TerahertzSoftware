from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Ui.UiGpChartView import Ui_UiGpChartView


class GpChartView(QWidget, Ui_UiGpChartView):
    def __init__(self, parent=None):
        super(GpChartView, self).__init__(parent)
        self.setupUi(self)
        self.retranslateUi(self)