import threading
from AppData import *
import globalvar as gl
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Ui.UiDevGp import Ui_Form
from Common.MessageBoxEx import MessageBoxEx


class ThzDevGpPage(QWidget, Ui_Form):
    signalNotify = pyqtSignal(QWidget, int, object)

    def __init__(self, parent=None):
        super(ThzDevGpPage, self).__init__(parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.txtHz.setEnabled(False)
        self.btnLaser.clicked.connect(self.onBtnLaser)
        self.btnBaisSrc.clicked.connect(self.onBtnBaisSrc)
        self.slider.setRange(0, 360)
        self.signalNotify.connect(self.signalNotifyProc)
        self.slider.valueChanged.connect(self.onValueChanged)
        self.txtPhase.setValidator(QIntValidator(0, 360, self))
        self.txtPhase.textChanged.connect(self.onTextChanged)
        self.txtTime.setValidator(QIntValidator(0, 20000, self))
        self.txtPhase.setText(f'{SysConf.devGpMode.amplifier.phase}')
        self.txtTime.setText(f'{SysConf.devGpMode.amplifier.time}')
        self.txtPort.setText(SysConf.devGpMode.serial)

    def onValueChanged(self, data):
        self.txtPhase.setText(f'{data}')

    def onTextChanged(self, text):
        if gl.isStrNoneOrEmpty(text):
            self.slider.setValue(0)
        else:
            self.slider.setValue(int(text))

    def onBtnLaser(self):
        if self.btnLaser.isChecked():  # 打开
            print("设备管理中，光谱模式打开激光器操作！")
            self.btnLaser.setEnabled(False)
            self.btnLaser.setStyleSheet('QPushButton{background-color:#FF4EBE44;border:none;}')
            thread = threading.Thread(self.turnOnLaserProc)
            thread.start()
        else:
            if self.btnBaisSrc.isEnabled():
                MessageBoxEx.Show("请先关闭偏压源！")
                self.btnLaser.setChecked(True)
                return

            print("设备管理中，光谱模式关闭激光器操作！")
            if SysConf.gpFlow.laser.turnOff():
                SysConf.gpFlow.closeLBA()
                self.btnLaser.setStyleSheet('QPushButton{background-color:#FF00A3DA;border:none;}'
                                            ' QPushButton:hover{background-color:#8F00A3DA;}')
            else:
                self.btnLaser.setChecked(True)
                MessageBoxEx.Show("关闭激光器失败！")

    def turnOnLaserProc(self):
        gl.set()
        code = SysConf.gpFlow.runLaser()
        gl.reset()
        self.signalNotify.emit(None, 6000, code)

    def onBtnBaisSrc(self):
        if self.btnBaisSrc.isChecked():
            print("设备管理中，光谱模式打开偏压源操作！")
            if SysConf.gpFlow.amplifier.turnOn():
                self.btnBaisSrc.setStyleSheet('QPushButton{background-color:#FF4EBE44;border:none;}')
            else:
                self.btnBaisSrc.setChecked(False)
                MessageBoxEx.Show("偏压源开启失败！")
        else:
            print("设备管理中，光谱模式关闭偏压源操作！")
            if SysConf.gpFlow.amplifier.turnOff():
                self.btnLaser.setStyleSheet('QPushButton{background-color:#FF00A3DA;border:none;}'
                                            ' QPushButton:hover{background-color:#8F00A3DA;}')
            else:
                self.btnBaisSrc.setChecked(True)
                MessageBoxEx.Show("关闭偏压源失败！")

    def signalNotifyProc(self, widget, mode, value):
        if mode == 6000:
            self.btnLaser.setEnabled(True)
            if value == gl.SUCCESS:
                self.btnBaisSrc.setEnabled(True)
            else:
                self.btnLaser.setChecked(False)
                SysConf.gpFlow.closeLBA()
                self.btnLaser.setStyleSheet('QPushButton{background-color:#FF00A3DA;border:none;}'
                                            ' QPushButton:hover{background-color:#8F00A3DA;}')
                MessageBoxEx.Show(f"设备管理中，光谱模式打开激光器失败! 错误代码：{value}")
