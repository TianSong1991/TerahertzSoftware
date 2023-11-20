from Core.ComHelper import ComHelper
import globalvar as gl
import time


class AmplifierHelper(object):
    def __init__(self, serial):
        self.serial = serial
        self.buff = []

    def turnOn(self):
        self.buff.clear()
        self.buff.append([0xA5, 0x5A, 0x22, 0x01, 0x00, 0x00, 0x00])
        print('光谱-打开偏压源!')
        if self.serial.writeDataReturn(self.buff, 7, 7, 200) is False:
            return False
        elif self.buff[1] == 0x5A and self.buff[3] == 0x01:
            return True
        else:
            return False

    def turnOff(self):
        self.buff.clear()
        self.buff.append([0xA5, 0x5A, 0x22, 0x00, 0x00, 0x00, 0x00])
        print('光谱-关闭偏压源!')
        if self.serial.writeDataReturn(self.buff, 7, 7, 200) is False:
            return False
        elif self.buff[1] == 0x5A and self.buff[3] == 0x00:
            return True
        else:
            return False

    def setPhase(self, phase):
        self.buff.clear()
        self.buff.append([0xA5, 0x5A, 0x02, (phase >> 8) & 0xFF, phase & 0xFF, 0x00, 0x00])
        print('锁相放大器相位设置!')
        if self.serial.writeDataReturn(self.buff, 7, 7) is False:
            return False
        elif (self.buff[4] + (self.buff[3] << 8)) == phase:
            return True
        else:
            return False

    def setMagnify(self):
        self.buff.clear()
        self.buff.append([0xA5, 0x5A, 0x02, 0x00, 0x00, 0x00, 0x00])
        setArr = [[0x32, gl.getValue('PAG')], [0x33, gl.getValue('BPG')], [0x34, gl.getValue('LPG')]]
        print('设置锁相放大倍数!')
        for i in Range(3):
            self.buff[2] = setArr[i][0]
            self.buff[3] = setArr[i][1]
            if self.serial.writeDataReturn(self.buff, 7, 7) is False:
                return False
            elif self.buff[2] != setArr[i][0] or self.buff[3] != setArr[i][1]:
                return False
        return True

    def getAmplifierData(self, data):
        self.buff.clear()
        self.buff.append([0xA5, 0x5A, 0x01, 0x00, 0x00, 0x00, 0x00])
        print('采集锁相放大器相位')
        if self.serial.writeDataReturn(self.buff, 7, 7, 0):
            data[0] = 0xFFFF & ((self.buff[3] << 8) + self.buff[4]);
            data[0] = float(0.3051757813 * data);
            return True
        else:
            return False

    def setProgress(self, value):
        self.buff.clear()
        self.buff.append([0x51, 0x44, 0x08, value, 0x00, 0x00, 0x00])
        print('设置进度')
        if self.serial.writeDataReturn(self.buff, 7, 7, 0) is False:
            return False
        elif self.buff[0] == 0x4F and self.buff[1] == 0x48:
            return True
        else:
            return False
