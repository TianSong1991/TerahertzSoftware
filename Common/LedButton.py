from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class LedButton(QWidget):
    def __init__(self, parent=None):
        super(LedButton, self).__init__(parent)

        # 设置无边框和背景透明
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.color = QColor('#FF4D4D4D')
        self.resize(80, 54)
        self.text = 'Led'
        self.state = LedButton.OFF  # 按钮状态：ON表示开，OFF表示关, ERROR表示故障

    @pyqtSlot(int)
    def setState(self, state):
        self.state = state
        self.update()

    def getState(self):
        return self.state

    State = pyqtProperty(int, getState, setState)

    def setText(self, text):
        self.text = text
        self.update()

    def getText(self):
        return self.text

    Text = pyqtProperty(int, getText, setText)

    def setTextColor(self, color):
        self.color = color
        self.update()

    def paintEvent(self, event):
        """绘制按钮"""
        super(LedButton, self).paintEvent(event)

        # 创建绘制器并设置抗锯齿和图片流畅转换
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        # 定义字体样式
        font = QFont('Microsoft YaHei')
        font.setPixelSize(14)
        painter.setFont(font)

        # 绘制圆圈
        painter.setPen(Qt.NoPen)
        brush = QBrush(Qt.lightGray)
        if self.state == LedButton.ERROR:
            brush.setColor(Qt.red)
        elif self.state == LedButton.ON:
            brush.setColor(Qt.green)
        else:
            brush.setColor(Qt.lightGray)

        painter.setBrush(brush)
        r = (self.height() - 6 - 20)
        x = (self.width() - r) // 2
        c = r // 2
        painter.drawRoundedRect(x, 3, r, r, c, c)

        # 绘制文本
        painter.setPen(QPen(self.color))
        painter.setBrush(Qt.NoBrush)
        painter.drawText(QRect(0, self.height() - 20, self.width(), 20), Qt.AlignCenter, self.text)

    OFF = 0
    ON = 1
    ERROR = 2
