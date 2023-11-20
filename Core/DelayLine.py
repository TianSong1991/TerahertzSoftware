import re
import time
import globalvar as gl


class GPLine(object):
    def __init__(self, serial):
        self.serial = serial

    def gotoPosition(self, pos):
        print(f'移动GP延长线{pos}')
        buff = []
        if self.serial.writeStrReturn(f"_ABS_{pos:.2f}$", buff, True) is False:
            return False
        elif len(buff) == 0:
            return False
        elif buff[0] == 0x4F and buff[1] == 0x4B:
            return True
        else:
            return False

    def setSpeed(self, speed):
        buff = []
        if self.serial.writeStrReturn(f"_SPD_{speed}$", buff, True) is False:
            return False
        elif len(buff) == 0:
            return False
        elif buff[0] == 0x4F and buff[1] == 0x4B:
            return True
        else:
            return False

    def init(self):
        buff = [0x5F, 0x72, 0x65, 0x64, 0x61, 0x62, 0x73, 0x5F, 0x24]
        self.serial.writeDataReturn(buff, 9, 10)

    def getPosition(self):
        buff = []
        if self.serial.writeStrReturn("_redabs_$", buff, True, 30) is False:
            return -1
        else:
            feedback = bytes.decode(buff)
            if re.match(r'ABS:\d+\.\d+PS', feedback) is not None:
                return re.findall(r'\d+\.\d+', feedback)[0]
            else:
                return -1

    def callBack(self, old):
        pos = self.getPosition()
        if -1 == pos:
            return False
        elif abs(pos - old[0]) <= 1:
            return True
        else:
            old[0] = pos
            return False

    def reset(self, pos):
        self.setSpeed(8)
        time.sleep(0.1)
        self.gotoPosition(pos)
        time.sleep(2000)
        old = [0]
        return gl.timeOutNoreturn(25000, 500, lambda: self.callBack(old))
