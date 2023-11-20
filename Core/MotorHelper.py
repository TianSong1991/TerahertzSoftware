import time

import globalvar as gl
from AppData import *
from Core.ComHelper import ComHelper


class MotorHelper(object):
    def __init__(self):
        self.com = ComHelper('Motor')

    def open(self):
        # if gl.isStrNoneOrEmpty(SysConf.devCxMode.motor.serial):
        #     print('系统未配置串口！')
        #     return False
        # info = ComHelper.getInfoByName(SysConf.devCxMode.motor.serial)
        # if info is None:
        #     print('未找到指定硬件编号的串口设备！')
        #     return False
        return self.com.open('Motor', baudRate=115200)

    def close(self):
        self.com.close()

    def isEnable(self):
        if self.com.isEnable() is False:
            return self.open()
        else:
            return True

    def sendCmd(self, name, cmd, rLen):
        # print(name, cmd)
        res = self.com.writeReturn(cmd+' 55 aa 0d 0a', rLen)
        # print(len(res), res)
        return res

    def config(self, axis=1, speed=1000, acc=300, dec=300):
        cmd = f'96 43 0{axis} {gl.toHex(acc)} {gl.toHex(dec)} {gl.toHex(speed)}'
        self.sendCmd('config send', cmd, 2)
        return cmd

    def zero(self):
        self.config(SysConf.devCxMode.motor.xMotor)
        self.config(SysConf.devCxMode.motor.yMotor)

        cmd = f'96 5a 0{SysConf.devCxMode.motor.xMotor}'
        self.sendCmd('zero send', cmd, 2)
        cmd = f'96 5a 0{SysConf.devCxMode.motor.yMotor}'
        self.sendCmd('zero send', cmd, 2)
        self.waitStop(SysConf.devCxMode.motor.xMotor,0)
        self.waitStop(SysConf.devCxMode.motor.yMotor, 0)

    def move(self, mm, axis=1):
        pulse=mm*200+200000
        arr = gl.toHex(pulse, 4)
        cmd = f'96 4d 0{axis} 0{axis} {arr}'
        #print(cmd)
        self.sendCmd('move send', cmd, 2)
        return cmd

    def stop(self, axis=1):
        cmd = f'96 53 0{axis}'
        self.sendCmd('stop send', cmd, 2)
        return cmd

    def getPosition(self, axis=1):
        cmd = '96 41 0{0} 01'.format(axis)
        res = self.sendCmd('get position send', cmd, 8)
        if len(res) >= 8:
            return res[-1] + (res[-2] << 8) + (res[-3] << 16) + (res[-4] << 24)
        return -1

    def waitStop(self, axis,mm=-1):
        gl.waitTime(100)
        pos = self.getPosition(axis)
        checkpulse=-1
        if mm>0:
            checkpulse=mm*200+200000
        starttime=time.time()
        while True:
            gl.waitTime(10)
            current = self.getPosition(axis)
            if abs(checkpulse-current)<2:
                gl.waitTime(5)
                return True
            if current != pos:
                starttime=time.time()
            if time.time()-starttime>2:
                return False
            pos=current
        return False

    def goHome(self):
        self.move(SysConf.appData.cxMode.xStart, SysConf.devCxMode.motor.xMotor)
        self.move(SysConf.appData.cxMode.yStart, SysConf.devCxMode.motor.yMotor)
        self.waitStop(SysConf.devCxMode.motor.xMotor, SysConf.devCxMode.motor.xMotor)
        self.waitStop(SysConf.devCxMode.motor.yMotor, SysConf.devCxMode.motor.yMotor)

