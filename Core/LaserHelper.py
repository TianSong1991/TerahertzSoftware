from Core.ComHelper import ComHelper
import globalvar as gl
import time


class LaserHelper(object):
    def __init__(self, serial):
        self.serial = serial
        self.buff = []

    def turnOn(self):
        self.buff.append([0xEB, 0x90, 0x06, 0xA0, 0x00, 0x02, 0xCC, 0xCC, 0x01])
        print("打开激光器！")
        return self.serial.WriteData(self.buff, 9)

    def turnOff(self):
        self.buff.clear()
        self.buff.append([0xEB, 0x90, 0x06, 0xA0, 0x00, 0x02, 0x00, 0x00, 0x01])
        print("打开激光器！")
        return self.serial.WriteData(self.buff, 9)

    def getFreq(self):
        self.buff.clear()
        self.buff.append([0xEB, 0x90, 0x03, 0xA0, 0x18, 0x2E])
        print("打开激光器！")
        if self.serial.WriteDataReturn(self.buff, 6, 10) is False:
            return 0
        elif self.buff[2] != 0x07:
            return 0
        else:
            freq = (self.buff[6] << 24) + (self.buff[7] << 16) + (self.buff[8] << 8) + self.buff[9];
            return freq * 4000

    def isLock(self):
        self.buff.clear()
        self.buff.append([0xEB, 0x90, 0x03, 0xB0, 0x00, 0x0E])
        print("检查是否锁模！")
        if self.serial.WriteData(self.buff, 9) is False:
            return False
        else:
            return self.buff[7] == 0xEE

    def setLock(self):
        time_out = gl.getDevice()['gp']['timeout'] * 1000 * 1000000

        count = 0
        start = time.time_ns()
        while (time.time_ns() - start) < time_out:
            if 0 == self.getFreq():
                if count >= 5:
                    print("连续读取频率失败，请检查串口通讯是否正常！")
                    return False
                else:
                    ++count
            elif self.isLock():
                print('激光器已锁定！')
                return True




