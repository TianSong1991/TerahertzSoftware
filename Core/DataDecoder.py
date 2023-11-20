import math
import time

import numpy as np
from queue import Queue
import globalvar as gl
from AppData import *
from ThirdLib.Algorithm import Algorithm
from ThirdLib.AlgFunctions import Functions
from ThirdLib.AlgConfig import AlgConfig
from ThirdLib.AlgConfig import ImageConfig

class DataDecoder(object):
    def __init__(self):
        self.queue = Queue()
        self.dataDecoded = None
        self.exitEvent = threading.Event()  # 线程退出信号量
        self.exitEvent.set()
        self.signalAll = np.array([])
        self.xlists = np.array([])
        self.ylists = np.array([])

    def addPackage(self, package):
        self.queue.put(package)

    def decoderRun(self, isCxMode):
        self.queue.queue.clear()
        self.exitEvent.clear()
        action = self.cxDecoderProc if isCxMode else self.cgDecoderProc
        thread = threading.Thread(target=action)
        thread.start()

    def cgDecoderProc(self):
        index=0
        dir='./'+str(int(time.time()))
        if SysConf.devCxMode.gpcxSave==0:
            save=False
        else:
            save=True
        while self.exitEvent.wait(0.02) is False:
            if  gl.waitOne(1)and self.queue.qsize() == 0:    # 采集线程结束，且数据队列中无数据，退出循环，结束解码线程
                break
            dataArr = list(self.queue.queue)
            self.queue.queue.clear()
            if len(dataArr) < 1:
                continue
            data = [i for raw in dataArr for i in raw]
            xArr = Algorithm.get_times(SysConf.devCxMode.kuaiYan.getPs(), SysConf.devCxMode.kuaiYan.getSampleNumber())
            yArr = Algorithm.cxgp_unpack(np.array(data), SysConf.devCxMode.kuaiYan.getSampleNumber(),0)
            if self.dataDecoded is not None and type(yArr) is np.ndarray:
                self.dataDecoded([xArr, list(yArr)])
            if save:
                if os.path.exists(dir)==False:
                    os.makedirs(dir)
                index=index+1
                f = open(dir+'/'+str(index)+'.txt', 'w')
                f.write(str(data))
                f.close()

        self.exitEvent.set()

    def cxDecoderProc(self):
        xStart = SysConf.appData.cxMode.xStart
        yStart = SysConf.appData.cxMode.yStart
        xEnd = SysConf.appData.cxMode.xEnd
        yEnd = SysConf.appData.cxMode.yEnd
        xStep = SysConf.appData.cxMode.xStep
        yStep = SysConf.appData.cxMode.yStep
        xArr = np.array(Algorithm.get_times(SysConf.devCxMode.kuaiYan.getPs(), SysConf.devCxMode.kuaiYan.getSampleNumber()))
        # all=[]
        robot = SysConf.devCxMode.robot #当robot值为1时走机械臂算法
        mean_num = 10 #对单点采集的信号平均多少次
        cols = int((xEnd - xStart) / xStep)
        xlists = np.array([])
        ylists = np.array([])
        thicks=np.array([])
        pps = np.array([])
        pack_data = np.array([])
        signalAll = np.array([])
        readConfig = AlgConfig()
        pp_method, _ = readConfig.choose_pp()
        compress_signal = SysConf.devCxMode.compress_signal
        xArr_compress = np.array(
            Algorithm.get_times(SysConf.devCxMode.kuaiYan.getPs(), int(SysConf.devCxMode.kuaiYan.getSampleNumber()/compress_signal)))
        
        if robot == 1:
            params = ImageConfig()
            params.init()
            params.updateParams()

            robot_x, robot_y, robot_num, dx, dy = Functions.robot_data(params.robot_xyz)
            datax = np.zeros((2, len(robot_x))).astype(np.int)
            datax[0, :] = np.arange(1, len(robot_x) + 1)
            pps_robot = np.zeros_like(robot_x)
            thicks_robot = np.zeros_like(robot_x)
        while gl.waitOne(1) is False:
            if gl.waitOne(1) and self.queue.qsize() == 0:   # 采集线程结束，且数据队列中无数据，退出循环，结束解码线程
                break
            dataArr = list(self.queue.queue)
            self.queue.queue.clear()
            if len(dataArr) < 1:
                continue
            data = [i for raw in dataArr for i in raw]
            # all.append(data)
            if robot == 0:

                pack_data = Functions.supply_data(np.array(data),  SysConf.devCxMode.kuaiYan.getSampleNumber(), pack_data, pp_method)
                xList, yList, pp, thick,signals = Functions.calUnpackDataImage(xArr, pack_data, SysConf.devCxMode.kuaiYan.getSampleNumber(),compress_signal,
                                                                             2, 0.3, pulseToMM=2048)
                xlists,ylists,pps,thicks,signalAll,result = Functions.dealDataAll(xList, yList, pp, thick, signals, xlists, ylists, pps, thicks,signalAll,xStep)
                ppResult,thickResult = Functions.obtainPPThickImage(result,xStep,yStep,cols)
                self.signalAll = signalAll
            else:

                xList, yList, pp, thick, signals = Functions.calUnpackDataRobot(xArr, np.array(data), SysConf.devCxMode.kuaiYan.getSampleNumber(),compress_signal,
                                                                             2, 0.3, pulseToMM=2048)

                xlists ,pps, thicks, signalAll, pps_robot, thicks_robot, datax = Functions.robotData(xList, pp, thick,
                                                                                                     signals,
                                                                                                     xlists, pps,
                                                                                                     thicks, signalAll,
                                                                                                     pps_robot,
                                                                                                     thicks_robot,
                                                                                                     datax,
                                                                                                     mean_num=20)

                ppResult, thickResult = Functions.robotImage(xlists, pps, thicks, robot_x, robot_y, robot_num, dx, dy)
                self.signalAll = signalAll.T

            if robot == 0:
                self.xlists = xlists
                self.ylists = ylists
            else:
                if len(xlists) <= len(robot_x):
                    self.xlists = robot_x[0:len(xlists)]
                    self.ylists = robot_y[0:len(xlists)]
                else:
                    self.xlists[0:len(robot_x)] = robot_x
                    self.ylists[0:len(robot_x)] = robot_y
            self.pps = pps
            self.thicks = thicks
            # self.signalAll = signalAll.T
            if self.dataDecoded is not None and ppResult.shape[0] > 0:
                print(ppResult.shape)
                self.dataDecoded((ppResult, thickResult,xArr_compress.tolist(),self.signalAll[:,-1].tolist()))


        # f=open('cxdata.txt', 'w')
        # for dd in all:
        #     f.write(str(dd))
        self.exitEvent.set()

    def isDecodeStopped(self):
        return self.exitEvent.wait(2)

    def stop(self):
        self.exitEvent.set()
        self.queue.queue.clear()
