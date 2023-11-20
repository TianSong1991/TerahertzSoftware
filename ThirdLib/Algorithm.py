import os
import time
import numpy as np
import struct
from ThirdLib.AlgFunctions import Functions
from ThirdLib.AlgSampleProperties import SampleProperties
from ThirdLib.AlgConfig import AlgConfig
from ThirdLib.AlgSignalUtil import *
class Algorithm:
    # 获取时域
    @staticmethod
    def get_times(ps, num):
        times = []
        for i in range(num):
            times.append(round(ps / num * i, 2))
        return times

    # 获取频域
    @staticmethod
    def get_freq(t: np.array([]), ref: np.array([]),maxFreq=15):
        fxs, fys = Functions.calFrequency(t, ref)
        index=(fxs<0.1).sum()
        index2 = (fxs < maxFreq).sum()
        return fxs[index:index2], fys[index:index2]

    #获取吸收系数、折射率
    @staticmethod
    def get_absorption_refractive(t: np.array([]), ref_value: np.array([]), sample_value: np.array([]), d: float):
        sp = SampleProperties(t, ref_value, t, sample_value, d)
        f = sp.f 
        index = (f < 0.1).sum()
        index2 = (f < 6).sum()
        absorption = np.array(sp.calAbsorptionRate())
        refractive = np.array(sp.calRefractiveIndex())
        return f[index:index2], absorption[index:index2], refractive[index:index2]

 
    '''
    datas字节数组
    num 采集点个数
    fp 分频数
    markertype   0:正向 1:反向  2:双向
    '''

    @staticmethod
    def cxgp_unpack(datas: np.array([]), num: int, markertype: int) -> np.array([]):
        thz_signal = Functions.calUnpackData(datas, num, markertype)
        return thz_signal

    '''
        datas字节数组
        num 采集点个数
        fp 分频数
        markertype   0:正向 1:反向  2:双向
        minpeak 二次反射峰高度百分比
        pulseToMM 脉冲信号转mm
    '''

    @staticmethod
    def cx_unpack(t: np.array([]), datas: np.array([]), num: int, markertype: int, minpeak: float, pulseToMM):

        xList, yList, pp, td, timeSeriesList = Functions.calUnpackDataImage(t, datas, num, markertype, minpeak, pulseToMM)

        return xList, yList, pp, td, timeSeriesList

    @staticmethod
    def cx_unpackpp(t: np.array([]), datas: np.array([]), num: int, markertype: int, minpeak: float, pulseToMM):
        xList, yList, pp = Functions.calUnpackDataImagepp(t, datas, num, markertype, minpeak,pulseToMM)
        return xList, yList, pp

    @staticmethod
    def cx_calcPVAndThick1(cxMode,devCxMode,datas):
        xStep = cxMode.xStep
        yStep = cxMode.yStep
        xArr = np.array(
            Algorithm.get_times(devCxMode.kuaiYan.getPs(), devCxMode.kuaiYan.getSampleNumber()))
        xlists = datas[0,:]
        ylists = datas[1,:]
        signals = datas[2:,:]
        pvData, thkData = Functions.getPPThicks(xlists,ylists,xStep,yStep,xArr,signals)
        return pvData, thkData

    @staticmethod
    def cx_calcPVAndThick(datas,cxMode,devCxMode):
        cols = int((cxMode.xEnd - cxMode.xStart) / cxMode.xStep)
        xStep = cxMode.xStep
        yStep = cxMode.yStep
        xArr = np.array(
            Algorithm.get_times(devCxMode.kuaiYan.getPs(), devCxMode.kuaiYan.getSampleNumber()))
        xlists = np.array([])
        ylists = np.array([])
        pps = np.array([])
        thicks = np.array([])
        pack_data = np.array([])
        pp_method, _ = AlgConfig.choose_pp()
        data=[]
        for index in range(len(datas)):
            data.extend(datas[index])
            if index%500!=0 and index!=len(datas)-1:
                continue
            pack_data = Functions.supply_data(np.array(data), devCxMode.kuaiYan.getSampleNumber(), pack_data,
                                             pp_method)
            xList, yList, pp, thick = Functions.calUnpackDataImageActual(xArr, pack_data, devCxMode.kuaiYan.getSampleNumber(), 2, 0.3,
                                                                         pulseToMM=2048)

            xlists, ylists, pps, thicks, result = Functions.dealData(xList, yList, pp, thick, xlists, ylists, pps,
                                                                     thicks, xStep)
            pvData, thkData = Functions.obtainPPThickImage(result, xStep, yStep, cols)
            data.clear()
        return pvData,

    @staticmethod
    def unpack_network(data,num):
        yArrs = []
        for barray in data:
            yArr = np.array(struct.unpack('h' * num, barray[0:2*num]))
            yArr = removeNoise(yArr,num,1)
            yArrs.append(yArr)

        fast_thz_signal = align_signal(yArrs)

        readConfig = AlgConfig()
        size = readConfig.read_moveAverage()
        if size > 1:
            fast_thz_signal = move_average_signal(fast_thz_signal, size)
        return fast_thz_signal

    @staticmethod
    def unpackDataImageNet(t, datas, num, compress_signal, minpeak, pulseToMM):
        yArrs = []
        xlists = []
        ylists = []
        td = []
        pp = []

        for barray in datas:
            yArr = np.array(struct.unpack('h' * num, barray[0:2*num]))

            td = obtain_thick(yArr, minpeak, t, td)
            pp.append(np.max(yArr) - np.min(yArr))
            yArr = compressSignal(yArr, compress_signal)
            yArrs.append(yArr)

            x1, y1, x2, y2 = struct.unpack('i' * 4, barray[num*2:num*2+4*4])
            xlists.append(x1/pulseToMM)
            ylists.append(y1/pulseToMM)

        return np.array(xlists), np.array(ylists), np.array(pp), np.array(td), np.array(yArrs)


