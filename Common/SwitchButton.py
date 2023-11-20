from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class SwitchButton(QPushButton):
    def __init__(self, parent=None):
        super(SwitchButton, self).__init__(parent)

        # 设置无边框和背景透明
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.resize(60, 22)
        self.setCheckable(True)
        self.setChecked(False)
        # self.state = False  # 按钮状态：True表示开，False表示关

    def mousePressEvent(self, event):
        """鼠标点击事件：用于切换按钮状态"""
        super(SwitchButton, self).mousePressEvent(event)

        self.update()

    def paintEvent(self, event):
        """绘制按钮"""
        super(SwitchButton, self).paintEvent(event)

        # 创建绘制器并设置抗锯齿和图片流畅转换
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        brush = QBrush(QColor('#FFFFFFFF'))
        painter.setBrush(brush)
        painter.drawRect(0.0, 0.0, self.width(), self.height())
        # 定义字体样式
        font = QFont('Microsoft YaHei')
        font.setPixelSize(14)
        painter.setFont(font)

        # 开关为开的状态
        if self.isChecked() is True:
            # 绘制背景
            painter.setPen(Qt.NoPen)
            brush.setColor(QColor('#FF475D'))
            painter.setBrush(brush)
            painter.drawRoundedRect(0, 0, self.width(), self.height(), self.height() // 2, self.height() // 2)

            # 绘制圆圈
            painter.setPen(Qt.NoPen)
            brush.setColor(QColor('#ffffff'))
            painter.setBrush(brush)
            x = self.width() - self.height() + 3
            r = (self.height() - 6)
            c = r // 2
            painter.drawRoundedRect(x, 3, r, r, c, c)

            # 绘制文本
            painter.setPen(QPen(QColor('#ffffff'), 1))
            painter.setBrush(Qt.NoBrush)
            painter.drawText(QRect(0, 0, x, self.height()), Qt.AlignCenter, '开')
        # 开关为关的状态
        else:
            # 绘制背景
            painter.setPen(Qt.NoPen)
            brush.setColor(QColor('#FFB1B1B1'))
            painter.setBrush(brush)
            painter.drawRoundedRect(0, 0, self.width(), self.height(), self.height() // 2, self.height() // 2)

            # 绘制圆圈
            r = (self.height() - 6)
            c = r // 2
            brush.setColor(QColor('#FFFFFFFF'))
            painter.setBrush(brush)
            painter.drawRoundedRect(3, 3, r, r, c, c)

            # 绘制文本
            painter.setPen(QPen(QColor('#FF999999'), 1))
            painter.setBrush(Qt.NoBrush)
            painter.drawText(QRect(r + 3, 0, self.width() - r - 3, self.height()), Qt.AlignCenter, '关')
