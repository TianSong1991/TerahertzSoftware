import os
import json
import threading


class DeserializeBase:
    def __init__(self):
        pass

    def convertBack(self, _map):
        for key in _map:
            setattr(self, key, _map[key])
        return self


####################################Dev#########################################
class DevBoard(DeserializeBase):
    def __init__(self):
        self.multiple = 0
        self.lpfFreq = None
        self.lockedTimeOut = 600
        self.overFlowArr = [{'name': '1倍放大', 'DAC': 2497}, {'name': '2倍放大', 'DAC': 2497}, {'name': '5倍放大', 'DAC': 2497},
                            {'name': '10倍放大', 'DAC': 2497}]
        self.cutOffFreqArr = ['20kHz', '50kHz', '100kHz', '200kHz']

    def convert(self):
        return {'class': 'DevBoard', 'multiple': self.multiple, 'lpfFreq': self.lpfFreq,
                'lockedTimeOut': self.lockedTimeOut}


class DevKuaiYan(DeserializeBase):
    def __init__(self):
        self.serial = None
        self.dType = 0
        self.index = -1
        self.name = None
        self.zero = 0.7
        self.kType = 0.5
        self.scanArr = [{'freq': 25, 'time': 90}, {'freq': 25, 'time': 90}]
        self.scanArr = [{'freq': 10, 'time': 300}, {'freq': 25, 'time': 90}]
        self.lightMul = 6
        self.freqDivision = 0
        self.DivdeFreqArr = ["不分频", "2分频", "4分频", "8分频", "16分频"]
        self.RefDivideFreqArr = ["最大点数", "1/2点数", "1/4点数", "1/8点数", "1/16点数"]

    def convert(self):
        return {'class': 'DevKuaiYan', 'serial': self.serial, 'dType': self.dType, 'index': self.index,
                'name': self.name, 'zero': self.zero, 'kType': self.kType, 'lightMul': self.lightMul,
                'freqDivision': self.freqDivision, 'scanArr': self.scanArr}

    def setIndex(self, index):
        for _iter in self.scanArr:
            if _iter.index == index:
                self.index = self.scanArr.index(_iter)
                return True
            else:
                return False

    def getMul(self):
        return int(0.5 / self.kType)

    def getSampleNumber(self, index=-1, fp=-1):
        if index == -1 or fp == -1:
            data = (self.scanArr[self.index].time / 40.0) * 2000 * self.getMul() / self.lightMul * 6
            return int(data * 2 / self.getDivdeFreq())

    def getStep(self, mag=1):
        return 40.0 * self.getDivdeFreq() / 2000 / 2 * mag / self.getMul() * 6 / self.lightMul

    def getPlus(self):
        return int(2000 * self.getMul() * (self.zero + self.scanArr[self.index].time / 40.0 * 6 / self.lightMul))

    def getPs(self):
        return self.scanArr[self.index].time

    def getFreq(self):
        return self.scanArr[self.index].freq

    def getRealFreq(self):
        return self.scanArr[self.index].realFreq()

    def getRealDataFreq(self):
        if SysConf.cxMode.kuaiYan.dType > 10:
            return self.scanArr[self.index].freq
        else:
            return self.scanArr[self.index].freq * 2

    def getAmplitudeDot(self):
        return int(2000 * self.getMul() * ((self.scanArr[self.index].time / 40.0) * 6 / self.lightMul + 0.05))

    def getDivdeFreq(self, fp=-1):
        if fp == -1:
            fp = self.freqDivision

        temp = self.scanArr[self.index].time * self.getMul()

        if temp > 900:
            fp = fp + 4
        elif temp > 400:
            fp = fp + 1

        if fp < 0 or fp >= 8:
            return 128
        else:
            arr = [1, 2, 4, 8, 16, 32, 64, 128]
            return arr[fp]

    def getDivdeFreq2(self):
        _min = 5
        num = 131072 / self.getSampleNumber() / 2
        if num < 2 * _min:
            return 1
        elif num < 4 * _min:
            return 2
        elif num < 8 * _min:
            return 4
        elif num < 16 * _min:
            return 8
        else:
            return 16

    def getOffset(self):
        return int(self.zero * self.getMul() * 2000)


class ScanParam(DeserializeBase):
    def __init__(self):
        self.time = None
        self.freq = None

    def index(self):
        if self.time == 90:
            return 0
        elif self.time == 120:
            return 1
        elif self.time == 150:
            return 2
        elif self.time == 300:
            return 3
        elif self.time == 40:
            return 4
        elif self.time == 20:
            return 5
        elif self.time == 1000:
            return 6
        else:
            return -1

    def realFreq(self):
        if SysConf.cxMode.kuaiYan.dType % 10 >= 2:
            return 2 * self.freq
        else:
            return self.freq

    def isEmpty(self):
        return self.time == 0 and self.freq == 0

    def convert(self):
        return {'class': 'ScanParam', 'time': self.time, 'freq': self.freq}


class DevAmplifier(DeserializeBase):
    def __init__(self):
        self.time = None
        self.phase = None
        self.BPG = None
        self.LPG = None
        self.PAG = None

    def convert(self):
        return {'class': 'DevAmplifier', 'time': self.time, 'phase': self.phase, 'BPG': self.BPG,
                'LPG': self.LPG, 'PAG': self.PAG}


class Delay(DeserializeBase):
    def __init__(self):
        self.start = None
        self.speed = None
        self.interval = None

    def convert(self):
        return {'class': 'Delay', 'start': self.start, 'speed': self.speed, 'interval': self.interval}


class DevMotor(DeserializeBase):
    def __init__(self):
        self.serial = None
        self.xMotor = 0
        self.yMotor = 2
        self.speed = 0
        self.maxSpeed = 1
        self.pulse = 0
        self.type = None
        self.motorArr = [0, 1, 2, 3]

    def motoType(self):
        return 1 if self.type == 'own' else 0

    def convert(self):
        return {'class': 'DevMotor', 'xMotor': self.xMotor, 'yMotor': self.yMotor, 'speed': self.speed,
                'maxSpeed': self.maxSpeed, 'pulse': self.pulse, 'type': self.type, 'serial': self.serial}


class DevGpMode(DeserializeBase):
    def __init__(self):
        self.serial = ''
        self.showThick = False
        self.amplifier = DevAmplifier()
        self.delay = Delay()
        self.pi = ''
        self.serialArr = []

    def convert(self):
        return {'class': 'DevGpMode', 'serial': self.serial, 'showThick': self.showThick, 'amplifier': self.amplifier,
                'delay': self.delay, 'pi': self.pi}


class DevCxMode(DeserializeBase):
    def __init__(self):
        self.board = DevBoard()
        self.motor = DevMotor()
        self.kuaiYan = DevKuaiYan()
        self.gpcxSave = 0
        self.ptCheck = 0
        self.yinQConf = None
        self.compress_signal=10
        self.robot=0

    def convert(self):
        return {'class': 'DevCxMode', 'board': self.board, 'motor': self.motor, 'kuaiYan': self.kuaiYan,
                'gpcxSave': self.gpcxSave, 'ptCheck': self.ptCheck,'compress_signal':self.compress_signal,'robot':self.robot}


class YinQConf(DeserializeBase):
    def __init__(self):
        self.type = 0
        self.zero = 0
        self.lightMul = 6
        self.confArr = []

    def convert(self):
        return {'class': 'YinQConf', 'type': self.type, 'zero': self.zero, 'confArr': self.confArr}


class YinQParam(DeserializeBase):
    def __init__(self):
        self.key = None
        self.freq = 0
        self.time = 0
        self.cp = 0
        self.ci = 0
        self.vp = 0
        self.vi = 0
        self.vff = 0
        self.aff = 0
        self.offc = 0

    def convert(self):
        return {'class': 'YinQParam', 'key': f"{self.freq}Hz/{self.time}ps", 'cp': self.cp, 'ci': self.ci,
                'vp': self.vp, 'vi': self.vi, 'vff': self.vff, 'aff': self.aff, 'offc': self.offc}


####################################Conf#########################################
class GpCxBase(DeserializeBase):
    def __init__(self):
        self.isDeviceOn = False
        self.isManualAnalysis = False
        self.isSave = False
        self.isEdit = False
        self.timeOut = 0
        self.importInfo = None
        self.importStatus = 0
        self.isSample = False # False：Ref，True：Sam


class DatCgModel(GpCxBase):
    def __init__(self):
        super(DatCgModel, self).__init__()
        self.isAutoAnalysis = True
        self.avgNum = 0     # 叠加次数
        self.angle = 0      # 入射角
        self.scanTime = 0   # 扫描时间
        self.thickness = 0  # 厚度值
        self.refraction = 0.0  # 折射率
        self.samIndex = 0   # 0:ref, 1,2...: sam

    def convert(self):
        return {'class': 'DatCgModel', 'avgNum': self.avgNum, 'angle': self.angle, 'scanTime': self.scanTime,
                'thickness': self.thickness, 'isAutoAnalysis': self.isAutoAnalysis, 'timeOut': self.timeOut,'refraction':self.refraction}


class DatGpMode(DatCgModel):
    def __init__(self):
        super(DatGpMode, self).__init__()
        self.isPiMode = False
        self.start = 0
        self.end = 0
        self.step = 0

    def convert(self):
        return {'class': 'DatGpMode', 'angle': self.angle, 'start': self.start, 'end': self.end, 'step': self.step,
                'thickness': self.thickness, 'isAutoAnalysis': self.isAutoAnalysis, 'timeOut': self.timeOut}


class DatCxMode(GpCxBase):
    def __init__(self):
        super(DatCxMode, self).__init__()
        self.xStart = 0
        self.xEnd = 0
        self.xStep = 0
        self.yStart = 0
        self.yEnd = 0
        self.yStep = 0
        self.angle = 0
        self.refraction = 0  # 折射率
        self.isPeakTrough = False
        self.isSection = False
        self.isThickness = False
        self.stepMove = False
        self.stepTime = 1

    def yStartReal(self):
        return 100 - self.yStart

    def convert(self):
        return {'class': 'DatCxMode', 'xStart': self.xStart, 'xEnd': self.xEnd, 'xStep': self.xStep,
                'yStart': self.yStart, 'yEnd': self.yEnd, 'yStep': self.yStep, 'angle': self.angle,
                'refraction': self.refraction, 'isPeakTrough': self.isPeakTrough, 'isSection': self.isSection,
                'isThickness': self.isThickness, 'timeOut': self.timeOut}


class SerialMode(DeserializeBase):
    def __init__(self):
        self.laser = None
        self.amplifier = None
        self.delayLine = None
        self.bias = None
        self.changeOver = None

    def convert(self):
        return {'class': 'SerialMode', 'laser': self.laser, 'amplifier': self.amplifier, 'delayLine': self.delayLine,
                'bias': self.bias, 'changeOver': self.changeOver}


class Listener(DeserializeBase):
    def __init__(self):
        self.ip = None
        self.port = 0
        self.start = False

    def convert(self):
        return {'class': 'Listener', 'ip': self.ip, 'port': self.port, 'start': self.start}


class DevNetwork(DeserializeBase):
    def __init__(self):
        self.ip = None
        self.port = 0
        self.gateWay = None

    def convert(self):
        return {'class': 'DevNetwork', 'ip': self.ip, 'port': self.port, 'gateWay': self.gateWay}


class AppData(DeserializeBase):
    def __init__(self):
        self.cxMode = DatCxMode()
        self.gpMode = DatGpMode()
        self.cgMode = DatCgModel()
        self.serialMode = SerialMode()
        self.tcpListener = Listener()
        self.devNetwork = DevNetwork()
        self.loginCode = None
        self.logLevel = 0
        self.product = 0
        self.loginUser = 'Admin'
        self.dbPath = None
        self.laserOn = None
        self.title = ''
        self.isFastScan = False
        self.isStdSaveEnable = False
        self.bscan1 = False
        self.bscan2 = False
        self.view = None
        self.polarization = 0
        self.model = 0
        self.temperature = 0

    def convert(self):
        return {'class': 'AppData', 'cxMode': self.cxMode, 'gpMode': self.gpMode, 'cgMode': self.cgMode,
                'serialMode': self.serialMode, 'tcpListener': self.tcpListener, 'devNetwork': self.devNetwork,
                'logLevel': self.logLevel, 'product': self.product, 'dbPath': self.dbPath, 'laserOn': self.laserOn,
                'title': self.title, 'bscan1': self.bscan1, 'bscan2': self.bscan2, 'view': self.view,
                'polarization': self.polarization, 'model': self.model, 'temperature': self.temperature,
                'loginCode': self.loginCode}


class SysConf:
    _asyncLock = threading.Lock()

    def __init__(self):
        self.appData = None
        self.devGpMode = None
        self.devCxMode = None
        self.yinQConf = None
        self.text = "Hello"
        self.lastPower = {}

    def __new__(cls, *args, **kwargs):
        if not hasattr(SysConf, "_instance"):
            with SysConf._asyncLock:
                if not hasattr(SysConf, "_instance"):
                    SysConf._instance = object.__new__(cls)

        return SysConf._instance

    @staticmethod
    def load():
        if os.path.exists('config/gpMode.json'):
            with open("config/gpMode.json", "r", encoding='utf-8') as f:
                SysConf.devGpMode = json.load(f, object_hook=SysConf.convertBack)
        else:
            SysConf.devGpMode = DevGpMode()

        if os.path.exists('config/cxMode.json'):
            with open("config/cxMode.json", "r", encoding='utf-8') as f:
                SysConf.devCxMode = json.load(f, object_hook=SysConf.convertBack)
        else:
            SysConf.devCxMode = DevCxMode()

        if os.path.exists('config/config.json'):
            with open("config/config.json", "r", encoding='utf-8') as f:
                SysConf.appData = json.load(f, object_hook=SysConf.convertBack)
        else:
            SysConf.appData = AppData()

        if os.path.exists('config/laserConf.json'):
            with open("config/laserConf.json", "r", encoding='utf-8') as f:
                SysConf.laserPower = json.load(f)
        else:
            SysConf.laserPower = {}

    @staticmethod
    def saveDevGp():
        with open('config/gpMode.json', "w", encoding='utf-8') as f:
            json.dump(SysConf.devGpMode, f, default=lambda a: a.convert(), indent=4)

    @staticmethod
    def saveDevCx():
        with open('config/cxMode.json', "w", encoding='utf-8') as f:
            json.dump(SysConf.devCxMode, f, default=lambda a: a.convert(), indent=4)

    @staticmethod
    def saveConf():
        with open('config/config.json', "w", encoding='utf-8') as f:
            json.dump(SysConf.appData, f, default=lambda a: a.convert(), indent=4)

    @staticmethod
    def saveYinQConf(fileName):
        with open(fileName, "w", encoding='utf-8') as f:
            json.dump(SysConf.yinQConf, f, default=lambda a: a.convert(), indent=4)

    @staticmethod
    def convertBack(_map):
        if 'class' not in _map:
            return None
        _type = _map['class']
        del _map['class']
        if _type == 'DevBoard':
            return DevBoard().convertBack(_map)
        elif _type == 'DevKuaiYan':
            return DevKuaiYan().convertBack(_map)
        elif _type == 'ScanParam':
            return ScanParam().convertBack(_map)
        elif _type == 'DevAmplifier':
            return DevAmplifier().convertBack(_map)
        elif _type == 'Delay':
            return Delay().convertBack(_map)
        elif _type == 'DevMotor':
            return DevMotor().convertBack(_map)
        elif _type == 'DevGpMode':
            return DevGpMode().convertBack(_map)
        elif _type == 'DevCxMode':
            return DevCxMode().convertBack(_map)
        elif _type == 'YinQConf':
            return YinQConf().convertBack(_map)
        elif _type == 'YinQParam':
            return YinQParam().convertBack(_map)
        elif _type == 'DatCgModel':
            return DatCgModel().convertBack(_map)
        elif _type == 'DatGpMode':
            return DatGpMode().convertBack(_map)
        elif _type == 'DatCxMode':
            return DatCxMode().convertBack(_map)
        elif _type == 'SerialMode':
            return SerialMode().convertBack(_map)
        elif _type == 'Listener':
            return Listener().convertBack(_map)
        elif _type == 'DevNetwork':
            return DevNetwork().convertBack(_map)
        elif _type == 'AppData':
            return AppData().convertBack(_map)
        else:
            return None

    @staticmethod
    def loadYinQConf(name):
        filePath = f'./config/yinquan/{str(name).upper()}.json'
        if os.path.exists(filePath):
            with open(filePath, "r", encoding='utf-8') as f:
                SysConf.yinQConf = json.load(f, object_hook=SysConf.convertBack)

            if SysConf.yinQConf.confArr is None \
                or len(SysConf.yinQConf.confArr) <= 0:
                return False
            else:
                return True
        else:
            SysConf.yinQConf = None
            return False
