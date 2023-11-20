from PyQt5.QtGui import QIcon
from PyQt5.QtDesigner import QPyDesignerCustomWidgetPlugin

from LedButton import LedButton


class LedButtonPlugin(QPyDesignerCustomWidgetPlugin):
    def __init__(self, parent=None):
        super(LedButtonPlugin, self).__init__(parent)
        self.initialized = False

    def initialize(self, core):
        if self.initialized:
            return
        self.initialized = True

    def isInitialized(self):
        return self.initialized

    def isContainer(self):
        return False

    def icon(self):
        return QIcon()

    def domXml(self):
        return '<widget class="LedButton" name="ledButton">\n</widget>\n'

    def group(self):
        return "FJRabbit"

    def includeFile(self):
        return "LedButton"

    def name(self):
        return "LedButton"

    def toolTip(self):
        return ""

    def whatsThis(self):
        return ""

    def createWidget(self, parent):
        return LedButton(parent)
