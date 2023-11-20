import time
import numpy as np
from AppData import *
import globalvar as gl
from Common.LedButton import LedButton
from Core.DelayLine import GPLine
from Core.LaserHelper import LaserHelper
from Core.ComHelper import ComHelper
from Core.AmplifierHelper import AmplifierHelper
from Core.DataDecoder import DataDecoder
from ThirdLib.Algorithm import Algorithm

class IWorkFlow(object):
    def __init__(self):
        self.asyncNotify = None

    def turnOn(self):
        return gl.SUCCESS

    def turnOff(self):
        return gl.SUCCESS

    def collRun(self):
        return gl.SUCCESS


class GpWorkFlow(IWorkFlow):
    def __init__(self):
        super(GpWorkFlow, self).__init__()
        self.calcFreq = None
        self.com = ComHelper('公共串口')
        self.laser = LaserHelper(self.com)
        self.delayLine = GPLine(self.com)
        self.amplifier = AmplifierHelper(self.com)

    def turnOn(self):
        print('一键开启设备！')
        if self.openLBA() is False:
            return gl.ERR_COM_LBA

        code = self.turnOff()
        if code != gl.SUCCESS:
            return code

        if self.laser.isLocked() is False:
            print('激光器锁定超时！')
            self.laser.turnOff()
            return gl.ERR_LASTER_LOCK

        if self.laser.turnOn() is False:
            print('打开激光器失败！')
            return gl.ERR_LASTER_ON

        if self.amplifier.turnOn() is False:
            print('打开偏压源失败！')
            self.laser.turnOff()
            return gl.ERR_BAISSRC_ON

        if self.amplifier.setMagnify() is False:
            print('锁相放大失败！')
            self.amplifier.turnOff()
            gl.waitOne(150)
            self.laser.turnOff()
            return gl.ERR_AMPLIFIER_MAGNIFY

        if self.amplifier.setPhase(SysConf.devGpMode.amplifier.phase) is False:
            print('相位设置失败！')
            self.amplifier.turnOff()
            gl.waitOne(150)
            self.laser.turnOff()
            return gl.ERR_AMPLIFIER_PHASE_SET

        return gl.SUCCESS

    def turnOff(self):
        print('一键关闭光谱设备！')
        # 锁相放大器关闭
        gl.waitOne(500)
        if self.amplifier.turnOff() is False:
            return gl.ERR_BAISSRC_OFF

        gl.waitOne(500)
        if self.laser.turnOff() is False:
            return gl.ERR_LASER_OFF

        if self.delayLine.reset(SysConf.appData.gpMode.start) is False:
            return gl.ERR_DELAYLINE_RESET

        return gl.SUCCESS

    def openLBA(self):
        if gl.isStrNoneOrEmpty(SysConf.devGpMode.serial):
            print('系统未配置串口！')
            return False
        info = ComHelper.getInfoByName(SysConf.devGpMode.serial)
        if info is None:
            print('未找到指定硬件编号的串口设备！')
            return False

        return self.com.open(info=info, baudRate=115200)

    def closeLBA(self):
        self.com.close()

    def collRun(self):
        if self.delayLine.reset() is False:
            return gl.ERR_DELAYLINE_RESET

        _num = 0
        _data = [0]
        _min = 1000000
        _max = -1000000
        start = SysConf.appData.gpMode.start
        end = SysConf.appData.gpMode.end
        step = SysConf.appData.gpMode.step
        thread = threading.Thread(target=self.calcFreq)
        thread.start()
        for i in range(start, end, step):
            self.delayLine.gotoPosition(i)

            if gl.waitOne(20):
                return gl.MANUAL_EXIT

            if self.amplifier.getAmlifierData(_data) is False:
                print('锁相采集失败！')
                return gl.ERR_AMPLIFIER_DATA
            else:
                if _data[0] < _min:
                    _min = _data[0]
                if _data[0] > _max:
                    _max = data[0]
                _num = _num + 1
                data = {((i * 1000) / 1000.0), _num, (_max - _min)}
                # 信号发送数据
                if SysConf.appData.gpMode.samIndex == 0:
                    self.xRef.append(i)
                    self.yRef.append(data)
                else:
                    self.xSam.append(i)
                    self.ySam.append(data)
                self.asyncNotify.emit(None, 1007, (SysConf.appData.gpMode.samIndex, i, data))

        return gl.SUCCESS

    def runLaser(self):
        if self.openLBA() is False:
            return gl.ERR_COM_LBA

        if self.laser.turnOn() is False:
            print('打开激光器失败！')
            return gl.ERR_LASTER_ON

        if self.laser.isLocked() is False:
            print('激光器锁定超时！')
            self.laser.turnOff()
            return gl.ERR_LASTER_LOCK
        else:
            return gl.SUCCESS


class CgWorkFlow(IWorkFlow):
    def __init__(self, usb):
        super(CgWorkFlow, self).__init__()
        self.usb = usb
        self.calcFreq = None
        self.decoder = DataDecoder()
        self.decoder.dataDecoded = self.onDataDecoded
        self.datas = []

    def laserCallBack(self, freq):
        self.asyncNotify.emit(None, 2009, freq)

    def turnOn(self):
        if self.usb.isUsbEnable() is False:
            return gl.ERR_USB_OPEN

        if self.usb.yinQLoad() is False:
            return gl.ERR_YINQ_CONFIG

        # nErr = self.turnOff()
        # if nErr != gl.SUCCESS:
        #     return nErr
        #
        # print('一键开启设备！')
        # if self.usb.turnOnLaser():
        #     self.asyncNotify.emit(None, 2003, LedButton.ON)
        # else:
        #     print('打开激光器失败！')
        #     return gl.ERR_LASER_ON
        #
        # timeOut = SysConf.devCxMode.board.lockedTimeOut
        # if self.usb.isLaserLocked(timeOut, self.laserCallBack) is False:
        #     print("激光器锁定超时！")
        #     self.usb.turnOffLaser()
        #     self.asyncNotify.emit(None, 2003, LedButton.OFF)
        #     return gl.ERR_LASER_OFF
        #
        # if gl.waitOne(5000):
        #     return gl.MANUAL_EXIT

        if self.usb.turnOnBaisSrc():
            self.asyncNotify.emit(None, 2004, LedButton.ON)
        else:
            print('开启偏压源失败！')
            self.turnOffLaser()
            self.asyncNotify.emit(None, 2003, LedButton.OFF)
            return gl.ERR_BAISSRC_ON

        self.usb.setLPFFreq(SysConf.devCxMode.board.lpfFreq)

        self.usb.setAmplifierData(SysConf.devCxMode.board.multiple)

        return gl.SUCCESS

    def turnOff(self):
        print('一键关闭成像设备！')
        self.usb.turnoffYinQ()
        if self.usb.turnOffBaisSrc():
            self.asyncNotify.emit(None, 2004, LedButton.OFF)
        else:
            return gl.ERR_BAISSRC_OFF

        # if self.usb.turnOffLaser():
        #     self.asyncNotify.emit(None, 2003, LedButton.OFF)
        # else:
        #     return gl.ERR_LASER_OFF

        return gl.SUCCESS

    def collRun(self):
        self.datas.clear()
        x = 0.0
        print('开始成像光谱数据采集！')
        if self.usb.turnOnYinQ():
            self.asyncNotify.emit(None, 2005, LedButton.ON)
        else:
            self.usb.yinQDisable()
            return gl.ERR_YINQ_ZERO

        if gl.waitOne(20):
            self.usb.turnoffYinQ()
            self.asyncNotify.emit(None, 2005, LedButton.OFF)
            return gl.MANUAL_EXIT

        if self.usb.isReady2ReadData() is False:
            self.usb.turnoffYinQ()
            self.asyncNotify.emit(None, 2005, LedButton.OFF)
            return gl.ERR_READY_READ

        self.usb.freeFIFO()
        self.decoder.decoderRun(isCxMode=False)
        thread = threading.Thread(target=self.calcFreq)
        thread.start()
        start = time.time_ns()
        end_time = start + SysConf.appData.cgMode.scanTime * 1000 * 1000000
        fp = 1
        code = gl.SUCCESS
        while time.time_ns() < end_time:
            runTime = (time.time_ns() - start) / 1000000000
            self.asyncNotify.emit(None, 2006, runTime)
            if self.usb.isEnableRead(fp):
                data = self.usb.readBuffer(int(128 / fp))
                self.decoder.addPackage(list(data))

            if gl.waitOne(100):
                code = gl.MANUAL_EXIT
                break
        if code == gl.SUCCESS:
            self.asyncNotify.emit(None, 2006, SysConf.appData.cgMode.scanTime)
        self.usb.turnoffYinQ()
        # self.decoder.exitEvent.set()
        self.asyncNotify.emit(None, 2005, LedButton.OFF)
        return code

    def isFlowStopped(self):
        return self.decoder.isDecodeStopped()

    def onDataDecoded(self, data):
        self.datas.append(data[1])
        if 0 < SysConf.appData.cgMode.avgNum < len(self.datas):
            del self.datas[0]

        value = list(np.array(self.datas[-SysConf.appData.cgMode.avgNum:]).mean(axis=0))
        para_data = [SysConf.appData.cgMode.samIndex, data[0], value]
        self.asyncNotify.emit(None, 2007, para_data)


class CxWorkFlow(IWorkFlow):
    def __init__(self, usb, motor):
        super(CxWorkFlow, self).__init__()
        self.usb = usb
        self.samArr = []
        self.signalAll=np.array([])
        self.motor = motor
        self.decoder = DataDecoder()
        self.decoder.dataDecoded = self.onDataDecoded


    def laserCallBack(self, freq):
        self.asyncNotify.emit(None, 3008, freq)

    def turnOn(self):
        self.samArr.clear()
        if SysConf.devCxMode.robot!=1 and self.motor.isEnable() is False:
            return gl.ERR_MOTOR_DEVICE

        if self.usb.isUsbEnable() is False:
            return gl.ERR_USB_OPEN

        if self.usb.yinQLoad() is False:
            return gl.ERR_YINQ_CONFIG

        nErr = self.turnOff()
        if nErr != gl.SUCCESS:
            return nErr

        print('一键开启设备！')
        # if self.usb.turnOnLaser():
        #     self.asyncNotify.emit(None, 3003, LedButton.ON)
        # else:
        #     print('打开激光器失败！')
        #     return gl.ERR_LASER_ON
        #
        # timeOut = SysConf.devCxMode.board.lockedTimeOut
        # if self.usb.isLaserLocked(timeOut, self.laserCallBack) is False:
        #     print("激光器锁定超时！")
        #     self.usb.turnOffLaser()
        #     self.asyncNotify.emit(None, 3003, LedButton.OFF)
        #     return gl.ERR_LASER_OFF
        #
        # if gl.waitOne(5000):
        #     return gl.MANUAL_EXIT

        if self.usb.turnOnBaisSrc():
            self.asyncNotify.emit(None, 3004, LedButton.ON)
        else:
            print('开启偏压源失败！')
            self.usb.turnOffLaser()
            self.asyncNotify.emit(None, 3003, LedButton.OFF)
            return gl.ERR_BAISSRC_ON

        self.usb.setLPFFreq(SysConf.devCxMode.board.lpfFreq)

        self.usb.setAmplifierData(SysConf.devCxMode.board.multiple)
        if SysConf.devCxMode.robot != 1:
            self.motor.zero()
        return gl.SUCCESS

    def turnOff(self):
        print('一键关闭成像设备！')
        self.usb.turnoffYinQ()
        gl.waitOne(200)
        if self.usb.turnOffBaisSrc():
            self.asyncNotify.emit(None, 3004, LedButton.OFF)
        else:
            return gl.ERR_BAISSRC_OFF

        # if self.usb.turnOffLaser():
        #     self.asyncNotify.emit(None, 3003, LedButton.OFF)
        # else:
        #     return gl.ERR_LASER_OFF

        return gl.SUCCESS

    def collRun(self):
        self.samArr.clear()
        print('开始成像数据采集！')
        if self.usb.turnOnYinQ() is False:
            self.usb.yinQDisable()
            return gl.ERR_YINQ_ZERO
        else:
            self.asyncNotify.emit(None, 3005, LedButton.ON)

        if gl.waitOne(20):
            self.usb.turnoffYinQ()
            self.asyncNotify.emit(None, 3004, LedButton.OFF)
            return gl.MANUAL_EXIT

        self.asyncNotify.emit(None, 3006, LedButton.ON)
        if SysConf.devCxMode.robot != 1 and self.motor.goHome() is False:
            code = gl.ERR_MOTOR_INITPOS
        if self.usb.isReady2ReadData() is False:
            code = gl.ERR_READY_READ
        else:
            thread = threading.Thread(target=self.collDataAsync)
            thread.start()
            code = self.motorRun()

        self.usb.turnoffYinQ()
        try:
            self.signalAll = np.insert(self.decoder.signalAll, 0, [self.decoder.xlists, self.decoder.ylists], axis=0)
        except Exception as err:
            print(err)
        # self.decoder.exitEvent.set()
        self.asyncNotify.emit(None, 3005, LedButton.OFF)
        return code

    def motorRun(self):
        i = 0
        if SysConf.devCxMode.robot!=1:
            print('扫描电机弓字形运动中...')
            starty = SysConf.appData.cxMode.yStart
            endy = SysConf.appData.cxMode.yEnd + SysConf.appData.cxMode.yStep
            stepx = SysConf.appData.cxMode.xStep
            stepy = SysConf.appData.cxMode.yStep
            freq = SysConf.devCxMode.kuaiYan.scanArr[SysConf.devCxMode.kuaiYan.index].freq
            speed = int(freq * stepx * 200*2)
            self.motor.config(1, speed,speed,speed)
            self.motor.config(2, 10000,5000,5000)
            lastx = SysConf.appData.cxMode.xStart
            for index in range(int((endy - starty) / stepy)):
                i = i + 1
                x = (SysConf.appData.cxMode.xEnd + 0.1) if (i % 2 == 0) else SysConf.appData.cxMode.xStart
                self.motor.move(starty + stepy * index, SysConf.devCxMode.motor.yMotor)
                print('yto', starty + stepy * index)
                if self.motor.waitStop(SysConf.devCxMode.motor.yMotor, starty + stepy * index) is False:
                    return gl.ERR_MOTOR_INITPOS
                if SysConf.appData.cxMode.stepMove:
                    rang = abs(int((x - lastx) / stepx))
                    for j in range(rang):
                        if x > lastx:
                            tox = stepx * j + stepx + lastx
                        else:
                            tox = lastx - stepx * j - stepx

                        self.motor.move(tox, SysConf.devCxMode.motor.xMotor)
                        print('xto', tox)
                        if self.motor.waitStop(SysConf.devCxMode.motor.xMotor, tox) is False:
                            return gl.ERR_MOTOR_INITPOS
                        time.sleep(SysConf.appData.cxMode.stepTime)
                        if gl.waitOne(5):
                            return gl.MANUAL_EXIT
                    lastx = x
                else:
                    self.motor.move(x, SysConf.devCxMode.motor.xMotor)
                    print('xto', x)
                    if self.motor.waitStop(SysConf.devCxMode.motor.xMotor, x) is False:
                        return gl.ERR_MOTOR_INITPOS
                if gl.waitOne(5):
                    return gl.MANUAL_EXIT
            print('扫描电机扫描结束！')
        else:
            print('机械臂开始...')
            while True:
                if gl.waitOne(5):
                    return gl.MANUAL_EXIT
            print('机械臂结束！')
        return gl.SUCCESS

    def collDataAsync(self):
        print('采集线程开始！')
        self.usb.freeFIFO()
        start = time.time_ns()
        self.decoder.decoderRun(isCxMode=True)
        while gl.waitOne(100) is False:
            if self.usb.isEnableRead():
                data = list(self.usb.readBuffer(128))
                # self.samArr.append(data)
                self.decoder.addPackage(data)
            runTime = (time.time_ns() - start) / 1000000000
            self.asyncNotify.emit(None, 3007, runTime)
        # for i in range(7):
        #     self.decoder.xlists = np.append(self.decoder.xlists, self.decoder.xlists)
        #     self.decoder.ylists = np.append(self.decoder.ylists, self.decoder.ylists)
        #     self.decoder.signalAll = np.append(self.decoder.signalAll, self.decoder.signalAll, axis=1)

        self.asyncNotify.emit(None, 3006, LedButton.OFF)
        print('采集线程结束！')

    def onDataDecoded(self, data):
        self.asyncNotify.emit(None, 3009, data)

    def isDataEnable(self):
        return self.decoder.isDecodeStopped() and self.signalAll.shape[0] >= 0

