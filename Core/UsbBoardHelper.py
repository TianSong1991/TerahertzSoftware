import usb.util
import usb
import time

from numpy import byte

import globalvar as gl
from AppData import *


class UsbBoardHelper(object):
    def __init__(self):
        self.lastKey = ''
        self.dev = None
        self.value21 = -1
        self.instruction = ['停止', '使能', '回零', '启动', ""]

    def open(self):
        if self.dev is not None and self.read(9) != -1:
            return True
        else:
            try:
                self.dev = usb.core.find(idVendor=0x1979, idProduct=0x7331)
                if self.dev is None:
                    return False
                self.dev.set_configuration()
                if -1 == self.read(9):
                    self.dev = None
                    return False
                else:
                    return True
            except BaseException:
                return False

    def read(self, addr):
        if self.dev is None:
            print('主板未打开，不能读数据！')
            return -1
        else:
            time.sleep(2/1000)
            temp = self.dev.ctrl_transfer(0xc0, 0xb2, 1, addr, 8, 100)
            return temp[0]

    def write(self, addr, value):
        if self.dev is None:
            print('主板未打开，不能写数据！')
            return False
        else:
            time.sleep(2/1000)
            self.dev.ctrl_transfer(0x40, 0xb1, value, addr, 8, 100)
            return True

    def readBuffer(self, readLen):
        self.dev.ctrl_transfer(0xc0, 0xb0, 1, readLen, 8, 100)
        return self.dev.read(0x82, readLen*1024)

    def close(self):
        if self.dev is None:
            return
        self.dev.close()
        self.dev = None

    def isUsbEnable(self):
        if self.dev is not None and self.read(9) != -1:
            return True
        else:
            return self.open()

    #####################Laster##########################
    def turnOnLaser(self):
        print('打开激光器！')
        if self.write(50, 0x86) is False:
            print('读激光器序列号写入失败!')
            return False

        gl.waitTime(500)
        status = self.read(9)
        if status == -1:
            print('读激光器序列号读状态失败!')
            return False
        elif (status & 0x01) == 0x00:
            self.write(50, 0x86)
            gl.waitTime(1000)
            status = self.read(9)
            if (status & 0x01) == 0x00:
                print('读激光器序列号未准备好!')
                return False

        key = f'{self.read(34):02X}{self.read(32):02X}'

        if SysConf.laserPower is None:
            print('激光器功率配置不存在！')
            return False
        elif key not in SysConf.laserPower:
            print(f'激光器{key}不存在！')
            return False
        self.write(20, SysConf.laserPower[key]['hWord'])
        self.write(22, SysConf.laserPower[key]['lWord'])
        gl.waitTime(100)
        result = self.write(50, 0x82)
        gl.waitTime(1000)
        self.write(51, 0x01)
        self.write(51, 0x00)
        return result

    def turnOffLaser(self):
        print('关闭激光器！')
        return self.write(50, 0x83)

    def getLaserFreq(self):
        if self.write(50, 0x81) is False:
            return gl.ERR_USB_READ_WRITE, 0
        gl.waitTime(50)
        status = self.read(9)
        if status == -1:
            return gl.ERR_USB_READ_WRITE, 0
        elif (status & 0x01) == 0:
            return gl.NOT_READY_READ, 0

        b1 = self.read(25)
        b2 = self.read(26)
        b3 = self.read(27)
        b4 = self.read(28)
        if b1 == -1 and b2 == -1 and b3 == -1 and b4 == -1:
            return gl.ERR_USB_READ_WRITE, 0
        freq = b1 + (b2 << 8) + (b3 << 16) + (b4 << 24)
        freq = freq * 4000
        self.write(51, 0x01)
        self.write(51, 0x00)
        return gl.SUCCESS, freq / 1000000.0

    def checkLock(self):
        if self.write(50, 0x88) is False:
            return gl.ERR_USB_READ_WRITE

        if gl.waitOne(50):
            return False

        status = self.read(9)
        if status == -1:
            return gl.ERR_USB_READ_WRITE
        elif (status & 0x01) == 0:
            return gl.NOT_READY_READ

        b1 = self.read(29)
        if b1 == -1:
            return gl.ERR_USB_READ_WRITE
        self.write(51, 0x01)
        self.write(51, 0x00)
        return gl.SUCCESS if b1 == 0xEE else -1

    def isLaserLocked(self, timeout, callBack):
        print("等待激光器锁定！")
        count = 0
        end = time.time_ns() + timeout * 1000000000
        while time.time_ns() < end:
            code, freq = self.getLaserFreq()
            if code == gl.SUCCESS:
                callBack(freq)
                gl.waitTime(100)
                if self.checkLock() == gl.SUCCESS:
                    print('激光器已锁定！')
                    return True
            elif code == gl.ERR_USB_READ_WRITE:
                count = count + 1
                if count >= 5:
                    print('连续读取频率失败，请检查USB通讯是否正常！')
                    return False

            if gl.waitOne(500):
                return False
        return False

    #####################BaisSrc##########################

    def turnOnBaisSrc(self):
        print('打开偏压源！')
        if self.write(49, 0x01) is False:
            return False
        gl.waitTime(150)

        return (self.read(13) & 0x01) == 0x01

    def turnOffBaisSrc(self):
        print('关闭偏压源!')
        if self.write(49, 0x00) is False:
            return False
        gl.waitTime(150)
        return (self.read(13) & 0x01) == 0x00

    def setProgress(self, value):
        self.write(13, byte(value))

    #####################YinQ##########################
    def sendCmd(self, mode, cmd):
        if gl.isStrNoneOrEmpty(cmd):
            return
        print(f'音圈电机-{self.instruction[mode]}')
        # buff = bytes(cmd, encoding="utf8")
        # self.write(47, 1)
        # self.write(47, 0)
        # for bt in buff:
        #     self.write(45, bt)
        # self.write(46, ((0x80 | (len(buff) - 1)) & 0x7F))
        buff = bytes(cmd, encoding='utf-8')
        self.write(47, 1)
        self.write(47, 0)
        for i in range(len(buff)):
            gl.waitTime(20)
            self.write(45, buff[i])
        self.write(46, 0x80 | ((len(buff) - 1) & 0x7F))
        gl.waitTime(150)

    def yinQLoad(self):
        self.sendCmd(4, 'g f0x92\n\n')
        rData = []
        while self.yinQFeedBack(400):
            rData.append(self.value21)

        rstr = bytes(rData).decode()
        arr = rstr.split(' ')
        if len(arr) != 2:
            return False
        name = arr[1].replace('\r', '').replace('\0', '')
        # load kuai yan config
        if SysConf.loadYinQConf(name):
            SysConf.devCxMode.kuaiYan.kType = SysConf.yinQConf.type
            SysConf.devCxMode.kuaiYan.zero = SysConf.yinQConf.zero
            SysConf.devCxMode.kuaiYan.lightMul = SysConf.yinQConf.lightMul
            return True
        else:
            return False

    def turnOnYinQ(self):
        print('开启音圈电机！')
        self.yinQEnable()
        gl.waitTime(100)
        if self.yinQGoZero() is False:
            return False

        self.yinQStart()
        print('音圈电机开启成功！')
        return True

    def turnoffYinQ(self):
        print('关闭音圈电机！')
        self.sendCmd(4, 's r0x9A 0\n\n')
        self.sendCmd(4, 't 2\n\n')
        gl.waitTime(500)
        self.sendCmd(4, 't 0\n\n')
        gl.waitTime(500)
        return self.yinQDisable()

    def yinQEnable(self):
        print('音圈电机使能！')
        self.sendCmd(1, 's r0x24 23\r\r')
        self.sendCmd(1, 's r0x71 6 4500 1 \r\r')
        self.sendCmd(1, 's r0x72 6 -4500 1 \r\r')

    def yinQDisable(self):
        print('音圈电机不是能！')
        self.sendCmd(1, 's r0x24 0\n\n')
        if self.yinQFeedBack(1000) is False:
            return False
        return self.value21 == 0x6F

    def yinQGoZero(self):
        print('音圈电机回零')
        index = SysConf.devCxMode.kuaiYan.index
        scanArr = SysConf.devCxMode.kuaiYan.scanArr
        key = f"{scanArr[index].freq}Hz/{scanArr[index].time}ps"
        param = None
        for item in SysConf.yinQConf.confArr:
            if item.key == key:
                param = item
                break
        if param is None:
            return False
        if self.lastKey != key and param is not None:
            self.sendCmd(2, f"s r0x00 {param.cp}\n\n")  # cp
            self.sendCmd(2, f"s r0x01 {param.ci}\n\n")  # ci
            self.sendCmd(2, f"s r0x27 {param.vp}\n\n")  # vp
            self.sendCmd(2, f"s r0x28 {param.vi}\n\n")  # vi
            self.sendCmd(2, f"s r0x30 {param.pp}\n\n")  # pp
            self.sendCmd(2, f"s r0x33 {param.vff}\n\n")  # vff
            self.sendCmd(2, f"s r0x34 {param.aff}\n\n")  # aff
            self.sendCmd(2, f"s r0x5f {param.offc}\n\n")  # offc

        self.lastKey = ''
        # self.sendCmd(2, "s r0xc2 532\n\n")
        # self.sendCmd(2, "s r0xc6 0\r\r")
        # self.sendCmd(2, "s r0x24 21\n\n")
        # self.sendCmd(2, "t 2\n\n")
        # gl.waitTime(2000)
        # self.sendCmd(2, "s r0xc2 544\n\n")
        # self.sendCmd(2, f"s r0xc6 {SysConf.devCxMode.kuaiYan.getOffset()}\r\r")  # 1400为设置偏移量
        # self.sendCmd(2, "s r0x24 21\n\n")
        # self.sendCmd(2, "t 2\n\n")

        self.sendCmd(2, "s r0xc2 548\n\n")
        gl.waitTime(500)
        self.sendCmd(2, f"s r0xc6 {SysConf.devCxMode.kuaiYan.getOffset()}\r\r")  # 1400为设置偏移量
        self.sendCmd(2, "s r0x24 21\n\n")
        self.sendCmd(2, "t 2\n\n")

        arr = []
        values = []
        count = 0
        start = time.time_ns()
        while time.time_ns() - start < 12000000000:
            self.sendCmd(2, "g r0x32\n\n")
            arr.clear()
            while self.yinQFeedBack(400):
                arr.append(self.value21)
            rstr = bytes.decode(bytes(arr), encoding='utf8')
            values.append(rstr)
            tarr = rstr.split('\r')
            for istr in tarr:
                if len(istr.split()) == 2:
                    count = 0 if int(istr.split()[1]) >= 30 else count + 1

            if count > 1:
                self.lastKey = key;
                return True
            gl.waitTime(100)
        return False

    def yinQStart(self):
        print('启动音圈电机！')
        self.sendCmd(3, "s r0x21 1.2\r\r")
        self.sendCmd(3, "s r0x22 1.2\r\r")
        self.sendCmd(3, "s r0x98 2\n\n")
        freq = SysConf.devCxMode.kuaiYan.scanArr[SysConf.devCxMode.kuaiYan.index].freq
        self.sendCmd(3, f"s r0x99 {freq}\n\n")  # 30代表频率
        # 4600代表振幅，也就是扫描时间范围
        # 扫描时间[单位ps] / 40就是振幅，有个算法，2000 * (振幅[单位mm] + 0.05)
        self.sendCmd(3, f"s r0x9A {SysConf.devCxMode.kuaiYan.getAmplitudeDot()}\n\n")
        self.sendCmd(3, "s r0x24 24\n\n")
        self.sendCmd(3, "t 2\n\n")

    def yinQFeedBack(self, timeout=50000):
        if self.read(20) == -1 or self.read(20) == -1:
            print('音圈反馈读20失败！')
            return False

        nErr = 0
        code = 0
        isReadEnable = False
        timeout *= 1000000
        start = time.time_ns()
        while time.time_ns() - start < timeout:
            code = self.read(22)
            if (code & 0x01) == 0:
                isReadEnable = True
            elif code == -1:
                if ++nErr >= 6:
                    print('连续读快延迟线应答失败，请检查USB通讯是否正常！')
                    return False
            if gl.waitOne(150):
                break

        if isReadEnable is False:
            print('YinQ反馈读等待超时失败！')
            return False
        if self.write(48, 1) is False:
            print('YinQ反馈写48失败！')
            return False
        if -1 == self.read(20):
            print('YinQ反馈读20失败！')
            return False
        self.value21 = self.read(21)
        if -1 == self.value21:
            print('YinQ反馈读20失败！')
            return False
        if self.write(48, 0):
            print('YinQ反馈写48成功！')
            return True
        else:
            print('YinQ反馈写48失败！')
            return False

    def yinQEnableEx(self):
        if self.isUsbEnable is False:
            return gl.ERR_USB_OPEN

        if self.yinQLoad() is False:
            return gl.ERR_YINQ_CONFIG

        self.yinQEnable()
        return gl.SUCCESS

    #####################Param##########################
    def setAmplifierData(self, data):
        print('设置前端放大器增益！')
        if self.write(41, data) is False:
            print('前端放大器增益设置失败！')
            return False
        else:
            self.setDAC(2497)
            return True

    def setDAC(self, dac):
        print('设置DAC控制字！')
        if self.write(43, (dac & 0xFF) and self.write(44, ((dac >> 8) & 0xFF))):
            gl.waitTime(20)
            return True
        else:
            print('DAC控制字下发失败！')
            return False

    def setLPFFreq(self, freq):
        print('设置低通过滤波器截止频率！')
        if self.write(42, freq) is False:
            print('低通过滤波器截止频率设置失败！')
            return False
        else:
            return True

    def setFreqDivision(self, mode):
        if self.write(11, mode):
            return True
        else:
            print('分频选择设置失败！')
            return False

    def setPulse(self, data):
        if self.write(5, (data & 0xFF)) \
                and self.write(6, ((data >> 8) & 0xFF)) \
                and self.write(7, ((data >> 16) & 0xFF)):
            return True
        else:
            print('开始脉冲数设置失败！')
            return False

    def setSampleNum(self, num):
        if self.write(8, (num & 0xFF)) \
                and self.write(9, ((num >> 8) & 0xFF)) \
                and self.write(10, ((num >> 16) & 0xFF)):
            return True
        else:
            print('采集点数设置失败！')
            return False

    def checkAmplifierZero(self):
        print('放大倍数零点校准中...')
        self.write(41, SysConf.devCxMode.board.multiple)
        dac = SysConf.devCxMode.board.overFlowArr[SysConf.devCxMode.board.multiple]['DAC']
        isZeroOk = False
        end_time = time.time_ns() + 60000 * 1000000
        while time.time_ns() < end_time:
            if self.setDAC(dac) is False:
                break
            if gl.waitOne(20):
                break
            self.write(30, 0)
            self.write(31, 1)
            if gl.waitOne(20):
                break
            lWord = self.read(30)
            hWord = self.read(31)
            if lWord == -1 or hWord == -1:
                continue
            avg = (lWord & 0xFF) + ((hWord << 8) & 0xFF00)
            if avg > 32968:
                dac -= 1
            elif avg < 32568:
                dac += 1
            else:
                isZeroOk = True
                print('放大倍数零点校准成功!')
                break

            if dac <= 0 or dac > 4095:
                print('零点校准失败，DAC控制字超出范围！')
                break

        return isZeroOk

    def freeFIFO(self):
        print('清空数据采集FIFO！')
        if self.write(14, 1) and self.write(14, 00):
            return True
        else:
            print('清空数据采集FIFO失败！')
            return False

    def isEnableRead(self, fp=1):
        code = self.read(5)
        value = byte(fp * 4 - 1)
        # print(f'能否读数状态：{code}')
        if (code & value) != 0:
            return True
        elif code == -1:
            print('连续查询数据采集是否可读失败，请确认USB通讯是否正常！')
            return False
        else:
            return False

    def isReady2ReadData(self):
        print('数据采集所需参数设置！')
        if self.setFreqDivision(SysConf.devCxMode.kuaiYan.freqDivision) is False:
            return False
        if self.setPulse(SysConf.devCxMode.kuaiYan.getPlus()) is False:
            return False
        return self.setSampleNum(SysConf.devCxMode.kuaiYan.getSampleNumber())

    #####################Device Manager##########################
    def dmTurnOnLaser(self, callBack):
        print('一键开启设备！')
        if self.turnOnLaser() is False:
            print('打开激光器失败！')
            return gl.ERR_LASER_ON

        timeOut = SysConf.devCxMode.board.lockedTimeOut
        if self.isLaserLocked(timeOut, callBack):
            return gl.SUCCESS
        else:
            print("激光器锁定超时！")
            self.turnOffLaser()
            return gl.ERR_LASER_OFF


