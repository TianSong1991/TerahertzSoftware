import threading
import time

import globalvar as gl
from AppData import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Ui.UiDevCx import Ui_Form
from Common.MessageBoxEx import MessageBoxEx


class ThzDevCxPage(QWidget, Ui_Form):
    signalNotify = pyqtSignal(QWidget, int, object)

    def __init__(self, parent=None):
        super(ThzDevCxPage, self).__init__(parent)
        self.setupUi(self)
        self.btnEnable.setEnabled(True)
        self.btnMotor.setEnabled(True)
        self.txtSmdjPP.setEnabled(False)
        self.txtLaserHz.setEnabled(False)
        self.cbxFpxz.setView(QListView())
        self.cbxFdqzy.setView(QListView())
        self.cbxDtlbqjzpl.setView(QListView())
        self.cbxSmdjDjX.setView(QListView())
        self.cbxSmdjDjY.setView(QListView())
        self.cbxKycxScanCfg.setView(QListView())
        self.signalNotify.connect(self.signalNotifyProc)
        self.btnBoard.clicked.connect(self.onBtnZeroCheck)
        self.btnLaser.clicked.connect(self.onBtnLaser)
        self.btnBaisSrc.clicked.connect(self.onBtnBaisSrc)
        self.btnMotor.clicked.connect(self.OnBtnMotor)
        self.btnEnable.clicked.connect(self.onBtnEnable)
        self.btnZero.clicked.connect(self.onBtnGoHome)
        self.btnStart.clicked.connect(self.onBtnStart)

        self.cbxKycxScanCfg.clear()
        for item in SysConf.devCxMode.kuaiYan.scanArr:
            self.cbxKycxScanCfg.addItem(f'频率:{item.freq}Hz / 扫描时间范围:{item.time}ps', item)

        self.cbxFpxz.clear()
        for item in SysConf.devCxMode.kuaiYan.DivdeFreqArr:
            self.cbxFpxz.addItem(item)

        self.cbxDtlbqjzpl.clear()
        for item in SysConf.devCxMode.board.cutOffFreqArr:
            self.cbxDtlbqjzpl.addItem(item)

        self.cbxFdqzy.clear()
        for item in SysConf.devCxMode.board.overFlowArr:
            self.cbxFdqzy.addItem(item['name'], item)

    def onBtnZeroCheck(self):
        print('设备管理中，通道校准操作！')
        self.btnBoard.setEnabled(False)
        self.btnBoard.setStyleSheet('QPushButton{background-color:#FF4EBE44;border:none;}')
        thread = threading.Thread(self.checkZeroPro)
        thread.start()

    def onBtnLaser(self):
        if self.btnLaser.isChecked():  # 打开
            print('设备管理中，打开激光器操作！')
            self.btnLaser.setEnabled(False)
            self.btnLaser.setStyleSheet('QPushButton{background-color:#FF4EBE44;border:none;}')
            thread = threading.Thread(target=self.turnOnLaserProc)
            thread.start()
        else:  # 关闭
            if self.btnBaisSrc.isChecked():
                MessageBoxEx.show("请先关闭偏压源！")
                self.btnLaser.setChecked(True)
                return
            print('设备管理中，关闭激光器操作！')
            SysConf.usb.turnOffLaser()
            self.btnLaser.setStyleSheet('QPushButton{background-color:#FF00A3DA;border:none;}'
                                        ' QPushButton:hover{background-color:#8F00A3DA;}')
            self.btnLaser.setText('开 启')

    def onBtnBaisSrc(self):
        if self.btnBaisSrc.isChecked():  # 打开
            print('设备管理中，打开偏压源操作！')
            if SysConf.usb.turnOnBaisSrc():
                self.btnBaisSrc.setText('关　闭')
                self.btnBaisSrc.setStyleSheet('QPushButton{background-color:#FF4EBE44;border:none;}')
            else:
                self.btnBaisSrc.setChecked(False)
        else:  # 关闭
            print('设备管理中，关闭偏压源操作！')
            if SysConf.usb.turnOffBaisSrc():
                self.btnBaisSrc.setText('开　启')
                self.btnBaisSrc.setStyleSheet(
                    'QPushButton{background-color:#FF00A3DA;border:none;}'
                    'QPushButton:hover{background-color:#8F00A3DA;}')
            else:
                self.btnBaisSrc.setChecked(True)

    def OnBtnMotor(self):
        if SysConf.motor.isEnable() is False:
            MessageBoxEx.show('电机打开失败！')
            return
        self.btnMotor.setEnabled(False)
        self.btnEnable.setStyleSheet('QPushButton{background-color:#FF4EBE44;border:none;}')
        print('设备管理中，扫描电机回零操作！')
        thread = threading.Thread(target=self.onMotorProc)
        thread.start()

    def onBtnEnable(self):
        self.btnEnable.setEnabled(False)
        self.btnZero.setEnabled(False)
        self.btnStart.setEnabled(False)
        if self.btnEnable.isChecked():
            print('设备管理中，音圈使能操作！')
            action = self.yinQEnableProc
        else:
            print("设备管理中，音圈不使能操作！")
            action = self.yinQDisableProc
        self.btnEnable.setStyleSheet('QPushButton{background-color:#FF4EBE44;border:none;}')
        self.btnZero.setStyleSheet('QPushButton:disabled{background-color:#FFB1B1B1;}')
        self.btnStart.setStyleSheet('QPushButton:disabled{background-color:#FFB1B1B1;}')
        thread = threading.Thread(target=action)
        thread.start()

    def onBtnGoHome(self):
        self.btnEnable.setEnabled(False)
        self.btnZero.setEnabled(False)
        self.btnStart.setEnabled(False)
        self.btnZero.setStyleSheet('QPushButton{background-color:#FF4EBE44;border:none;}')
        thread = threading.Thread(target=self.onBtnGoHomeProc)
        thread.start()

    def onBtnStart(self):
        self.btnEnable.setEnabled(False)
        self.btnZero.setEnabled(False)
        self.btnStart.setEnabled(False)
        self.btnStart.setStyleSheet('QPushButton{background-color:#FF4EBE44;border:none;}')
        if self.btnStart.isChecked():
            action = self.onStartYQProc
        else:
            action = self.onStopYQProc
        thread = threading.Thread(target=action)
        thread.start()

    def laserCallBack(self, freq):
        self.signalNotify.emit(None, 5008, freq)

    def turnOnLaserProc(self):
        gl.reset()
        code = SysConf.usb.dmTurnOnLaser(self.laserCallBack)
        gl.set()
        self.signalNotify.emit(None, 5000, code)

    def checkZeroPro(self):
        gl.reset()
        isOk = SysConf.usb.checkAmplifierZero()
        gl.set()
        self.signalNotify.emit(None, 5001, isOk)

    def yinQEnableProc(self):
        gl.reset()
        code = SysConf.usb.yinQEnableEx()
        gl.set()
        self.signalNotify.emit(None, 5002, code)

    def yinQDisableProc(self):
        gl.reset()
        isOk = SysConf.usb.yinQDisable()
        gl.set()
        self.signalNotify.emit(None, 5003, isOk)

    def onBtnGoHomeProc(self):
        isOk = SysConf.usb.yinQGoZero()
        self.signalNotify.emit(None, 5004, isOk)

    def onStartYQProc(self):
        SysConf.usb.yinQStart()
        self.signalNotify.emit(None, 5005, gl.SUCCESS)

    def onStopYQProc(self):
        SysConf.usb.turnoffYinQ()
        self.signalNotify.emit(None, 5006, gl.SUCCESS)

    def onMotorProc(self):
        gl.set()
        SysConf.moto.zero()
        gl.reset()
        self.signalNotify.emit(None, 5007, gl.SUCCESS)

    def signalNotifyProc(self, widget, mode, value):
        if mode == 5000:
            self.btnLaser.setEnabled(True)
            if value == gl.SUCCESS:
                self.btnBoard.setEnabled(True)
                self.btnBaisSrc.setEnabled(True)
                self.btnLaser.setText('关 闭')
            else:
                self.btnLaser.setChecked(False)
                self.btnLaser.setStyleSheet('QPushButton{background-color:#FF00A3DA;border:none;}'
                                            ' QPushButton:hover{background-color:#8F00A3DA;}')
        elif mode == 5001:
            self.btnBoard.setStyleSheet('QPushButton{background-color:#FF00A3DA;border:none;}'
                                        'QPushButton:hover{background-color:#8F00A3DA;}')
            self.btnBoard.setEnabled(True)
            info = '零点校准成功！' if value else '零点校准失败！'
            MessageBoxEx.show(info)
        elif mode == 5002:
            self.btnEnable.setEnabled(True)
            if value == gl.SUCCESS:
                self.btnEnable.setText("不使能")
                self.btnZero.setEnabled(True)
            else:
                self.btnEnable.setChecked(False)
                self.btnEnable.setStyleSheet('QPushButton{background-color:#FF00A3DA;border:none;}'
                                             'QPushButton:hover{background-color:#8F00A3DA;}')
                MessageBoxEx.show(f'音圈电机使能失败！错误代码：{value}')
        elif mode == 5003:
            self.btnEnable.setEnabled(True)
            if value:
                self.btnEnable.setText("使　能")
                self.btnZero.setEnabled(False)
                self.btnEnable.setStyleSheet('QPushButton{background-color:#FF00A3DA;border:none;}'
                                             'QPushButton:hover{background-color:#8F00A3DA;}')
            else:
                self.btnEnable.setChecked(True)
                MessageBoxEx.show("音圈电机不使能失败,请重试！")
        elif mode == 5004:
            self.btnEnable.setEnabled(True)
            self.btnZero.setEnabled(True)
            self.btnZero.setStyleSheet('QPushButton{background-color:#FF00A3DA;border:none;}'
                                       'QPushButton:hover{background-color:#8F00A3DA;}')
            if value:
                self.btnStart.setEnabled(True)
            else:
                MessageBoxEx.show(f'音圈回零失败！错误代码：{gl.ERR_YINQ_ZERO}')
        elif mode == 5005:
            self.btnStart.setText('停　止')
            self.btnEnable.setEnabled(True)
            self.btnZero.setEnabled(True)
            self.btnStart.setEnabled(True)
            pass
        elif mode == 5006:
            self.btnStart.setText('启　动')
            self.btnEnable.setText('使　能')
            self.btnEnable.setEnabled(True)
            self.btnZero.setEnabled(False)
            self.btnStart.setEnabled(False)
            self.btnEnable.setChecked(False)
            self.btnZero.setStyleSheet('QPushButton:disabled{background-color:#FFB1B1B1;}')
            self.btnStart.setStyleSheet('QPushButton:disabled{background-color:#FFB1B1B1;}')
        elif mode == 5007:
            self.btnMotor.setEnabled(True)
            self.btnMotor.setStyleSheet('QPushButton{background-color:#FF00A3DA;border:none;}'
                                        'QPushButton:hover{background-color:#8F00A3DA;}')
        elif mode == 5008:
            self.txtLaserHz.setText(f'{value:.1f}')







