# -*- coding: utf-8 -*-
"""
Create Time: 2021/1/29 8:36
Author: Kevin
"""
import numpy as np
from numpy.fft import fft
from scipy import signal
from ThirdLib.AlgConfig import AlgConfig
from PIL import Image
import struct
#与C#版本的配置文件一样，文件中函数提取FrequencyAnalysisUtil.py中
def convertToFrequency(t, x, fs = -1, fe = -1,duration = 100, isInDb = True, denoise = False):
    if np.all(x == 0):
        return np.array([]), np.array([])
    (f, xf) = timeToFrequency(t, x, duration, denoise)
    if fs == -1:
        fs = min(f)
        fe = max(f)

    if isInDb:
        xf = amplitudeToDb(xf)

    fRange, xfRange = selectRangeOfFrequency(f, xf, fs, fe)

    return fRange, xfRange

def dealNoise(xf):
    if np.array(xf).shape[0] > 300:
        data = np.array(xf[300:].copy())
        Percentile = np.percentile(data, [0, 25, 50, 75, 100])
        IQR = Percentile[3] - Percentile[1]
        DownLimit = Percentile[1] - IQR * 1.5
        data1 = np.array(np.where(data < DownLimit))
        if data1.shape[1] > 0:
            data1 = data1.reshape(data1.shape[1])
            random_value = np.random.random(data1.shape[0])
            data[data1] = DownLimit + random_value
            xf[300:] = data
    return xf

def timeToFrequency(t, x, duration, denoise = False):
    (tc, xc) = concatenateTimeSeries(t, x, duration)
    timeLength = len(xc)

    f, _ = calRangeOfFrequency(t, timeLength)
    N = len(xc)
    xf = fft(xc,N)

    xf /= timeLength
    xf *= 2

    # Normalization
    xf = np.abs(xf)
    f_index = f[0:int(np.floor(f.shape[0] / 2))]
    xf_index = xf[0:int(np.floor(xf.shape[0] / 2))]
    xf_max = np.max(xf_index[f_index >= 0.1])
    xf = xf / xf_max

    return f, xf

def concatenateTimeSeries(t, x, duration):
    """Concatenate time series to a specified duration."""
    # The original duration of the time series
    origDuration = t[-1] - t[0]
    deltaT = calAverageTimeStep(t)
    timeLength = len(t)

    tc = t[:]
    xc = x[:]

    # Concatenate time series if it is shorter than the duration
    if origDuration < duration:
        newTimeLength = int(round(duration / deltaT) + 1)
        tc = np.arange(newTimeLength) * deltaT + t[0]
        tc = tc.tolist()
        xc = [0] * newTimeLength
        xc[0 : timeLength] = x[:]

    return tc, xc

def obtain_f(t,n):
    t = np.array(t)
    dt = t[1:] - t[0:-1]
    dt = dt.mean()
    fRange = 1 / dt
    df = fRange / n
    f = np.arange(n) * df
    return f

def calAverageTimeStep(t):
    """Calculate the average step of a time series."""
    t = np.array(t)
    dt = t[1:] - t[0:-1]
    dt = dt.mean()
    return dt

def calRangeOfFrequency(t, n, isFromZero = True):
    """
    Calculate the range of frequency from the step increment of t

    n the number of steps of the time series
    isFromZero if the frequency start from 0, otherwise the first element of the frequency series is df
    f the frequency series
    df the step increment of f
    """
    dt = calAverageTimeStep(t)
    fRange = 1 / dt
    df = fRange / n
    f = np.arange(n) * df

    if not isFromZero:
        f = np.arange(1, n + 1) * df
    return f, df

def amplitudeToDb(xf):
    """Convert intensities to decibels."""
    xfDb = 20 * np.log10(xf)
    return xfDb

def selectRangeOfFrequency(f, xf, fs, fe):
    """
    Select the range of frequency, starting from fs and endding at fe.
    """
    f = np.array(f)
    xf = np.array(xf)

    fRange = f[(f >= fs) & (f <= fe)]
    xfRange = xf[(f >= fs) & (f <= fe)]

    return fRange, xfRange


def align_signal(timeSeriesList):
    readConfig = AlgConfig()

    align = readConfig.read_align()

    if align == 0:
        fast_thz_signal = np.mean(np.array(timeSeriesList), axis=0)
    else:
        peak0 = np.argmax(timeSeriesList,axis=1)
        mean_peak0 = int(np.mean(peak0))
        for i in range(len(peak0)):
            if peak0[i] < mean_peak0:
                timeSeriesList[i] = np.append(np.zeros(mean_peak0 - peak0[i]),
                                              timeSeriesList[i][0:len(timeSeriesList[i]) - mean_peak0 + peak0[i]])
            elif peak0[i] > mean_peak0:
                timeSeriesList[i] = np.append(timeSeriesList[i][peak0[i] - mean_peak0:],
                                              np.zeros(peak0[i] - mean_peak0))
        fast_thz_signal = np.mean(np.array(timeSeriesList), axis=0)

    return fast_thz_signal

def unpackData(python_value, nPoints,markertype):
    """Unpack time series of every point of the scan and the corresponding x and y
    from the serialized data by applying specific decoding mechanism. """
    marker = np.array([(163, 163, 165, 165), (164, 164, 166, 166)])
    markerPositions0 = __findMarkerPositions(python_value, marker[0, :])
    markerPositions1 = __findMarkerPositions(python_value, marker[1, :])
    markerPositions = markerPositions0.copy()
    markerPositions.extend(markerPositions1)
    markerPositions = np.array(markerPositions)

    if len(markerPositions) <= 1:
        return np.array([])
    markerPositions.sort()

    # Remove all the marker positions that aren't distanced by 2 * nPoints + 20
    markerPositions = __removeIllegalPositions(python_value, markerPositions, nPoints,marker)
    if len(markerPositions) <= 1:
        return np.array([])

    nSeries = len(markerPositions) - 1

    # Decode the time series, x, and y
    timeSeriesList = []
    if len(markerPositions1) > 0:
        for i in range(nSeries):
            if markertype == 1 and markerPositions[i] in markerPositions0:
                continue
            if markertype == 0 and markerPositions[i] in markerPositions1:
                continue
            series = __decodeTimeSeries(python_value, markerPositions, i, nPoints)
            series = np.array(series)
            if markertype == 2 and markerPositions[i] not in markerPositions1:
                series = series[::-1]
            if markertype == 0:
                series = series[::-1]
            denoised = __removeNoise(series, nPoints, 1)
            timeSeriesList.append(denoised)
    else:
        for i in range(nSeries):
            series = __decodeTimeSeries(python_value, markerPositions, i, nPoints)
            series = np.array(series)
            denoised = __removeNoise(series, nPoints, 1)
            timeSeriesList.append(denoised)

    fast_thz_signal = align_signal(timeSeriesList)

    try:
        readConfig = AlgConfig()
        size = readConfig.read_moveAverage()
        if size > 1:
            fast_thz_signal = move_average_signal(fast_thz_signal,size)
    except Exception as e:
        pass

    return fast_thz_signal

def unpackDataImage(t,datas, num, compress_signal, markertype,minpeak,pulseToMM):
    marker = np.array([(163, 163, 165, 165), (164, 164, 166, 166)])
    markerPositions0 = __findMarkerPositions(datas, marker[0, :])
    markerPositions1 = __findMarkerPositions(datas, marker[1, :])
    markerPositions = markerPositions0.copy()
    markerPositions.extend(markerPositions1)
    markerPositions = np.array(markerPositions)

    if len(markerPositions) <= 1:
        return np.array([]),np.array([]),np.array([]),np.array([]),np.array([])

    markerPositions.sort()

    markerPositions = __removeIllegalPositions(datas, markerPositions, num,marker)
    if len(markerPositions) <= 1:
        return np.array([]),np.array([]),np.array([]),np.array([]),np.array([])

    timeSeriesList = []
    nSeries = len(markerPositions) - 1

    td = []
    pp = []

    if len(markerPositions1) > 0:
        for i in range(nSeries):
            if markertype == 1 and markerPositions[i] in markerPositions0:
                continue
            if markertype == 0 and markerPositions[i] in markerPositions1:
                continue
            denoised = obtain_denoise(datas, markerPositions, i, num, markertype, markerPositions1)
            try:
                readConfig = AlgConfig()
                size = readConfig.read_moveAverage()
                if size > 1:
                    denoised = move_average_signal(denoised, size)
            except Exception as e:
                pass
            td = obtain_thick(denoised, minpeak, t, td)
            pp.append(np.max(denoised) - np.min(denoised))
            denoised = compressSignal(denoised,compress_signal)
            timeSeriesList.append(denoised)
    else:
        for i in range(nSeries):
            series = __decodeTimeSeries(datas, markerPositions, i, num)
            denoised = __removeNoise(series,num,1)
            try:
                readConfig = AlgConfig()
                size = readConfig.read_moveAverage()
                if size > 1:
                    denoised = move_average_signal(denoised, size)
            except Exception as e:
                pass
            td = obtain_thick(denoised, minpeak, t, td)
            pp.append(np.max(denoised) - np.min(denoised))
            denoised = compressSignal(denoised, compress_signal)
            timeSeriesList.append(denoised)

    timeSeriesList = np.array(timeSeriesList)
    precision = pulseToMM/1000
    xList, yList = obtain_xy(datas, markerPositions, num, precision)

    if len(markerPositions1) != 0:
        if markertype == 0:
            xList = xList[0::2]
            yList = yList[0::2]
        elif markertype == 1:
            xList = xList[1::2]
            yList = yList[1::2]

    return xList, yList, np.array(pp),np.array(td),np.array(timeSeriesList)




def unpackDataRobot(t,datas, num, compress_signal, markertype,minpeak,pulseToMM):
    marker = np.array([(163, 163, 165, 165), (164, 164, 166, 166)])
    markerPositions0 = __findMarkerPositions(datas, marker[0, :])
    markerPositions1 = __findMarkerPositions(datas, marker[1, :])
    markerPositions = markerPositions0.copy()
    markerPositions.extend(markerPositions1)
    markerPositions = np.array(markerPositions)


    if len(markerPositions) <= 1:
        return np.array([]),np.array([]),np.array([]),np.array([]),np.array([])
    markerPositions.sort()

    markerPositions = __removeIllegalPositions(datas, markerPositions, num,marker)
    if len(markerPositions) <= 1:
        return np.array([]),np.array([]),np.array([]),np.array([]),np.array([])

    timeSeriesList = []
    nSeries = len(markerPositions) - 1

    td = []
    pp = []

    if len(markerPositions1) > 0:
        for i in range(nSeries):
            if markertype == 1 and markerPositions[i] in markerPositions0:
                continue
            if markertype == 0 and markerPositions[i] in markerPositions1:
                continue
            denoised = obtain_denoise(datas, markerPositions, i, num, markertype, markerPositions1)
            td = obtain_thick(denoised, minpeak, t, td)
            pp.append(np.max(denoised) - np.min(denoised))
            denoised = compressSignalRobot(denoised,compress_signal)
            timeSeriesList.append(denoised)
    else:
        for i in range(nSeries):
            series = __decodeTimeSeries(datas, markerPositions, i, num)
            denoised = __removeNoise(series,num,1)
            td = obtain_thick(denoised, minpeak, t, td)
            pp.append(np.max(denoised) - np.min(denoised))
            denoised = compressSignalRobot(denoised, compress_signal)
            timeSeriesList.append(denoised)

    timeSeriesList = np.array(timeSeriesList)
    precision = 1
    xList, yList = obtain_xy(datas, markerPositions, num, precision)

    if markertype == 0:
        xList = xList[0::2]
        yList = yList[0::2]
    elif markertype == 1:
        xList = xList[1::2]
        yList = yList[1::2]

    return xList, yList, np.array(pp),np.array(td),np.array(timeSeriesList)


def compressSignal(data,compress):
    data=np.int32(data)
    data = np.array(Image.fromarray(data.reshape(1,len(data))).resize((int(len(data)/compress),1))).reshape(-1,)
    return data

def compressSignalRobot(data,compress):
    data = np.array(Image.fromarray(data.reshape(1,len(data))).resize((int(len(data)/compress),1))).reshape(-1,)
    return data

def unpackDataImageActual(t,datas, num, markertype,minpeak,pulseToMM):
    marker = np.array([(163, 163, 165, 165), (164, 164, 166, 166)])
    markerPositions0 = __findMarkerPositions(datas, marker[0, :])
    markerPositions1 = __findMarkerPositions(datas, marker[1, :])
    markerPositions = markerPositions0.copy()
    markerPositions.extend(markerPositions1)
    markerPositions = np.array(markerPositions)
    markerPositions.sort()

    if len(markerPositions) <= 1:
        return np.array([]),np.array([]),np.array([]),np.array([])
    markerPositions = __removeIllegalPositions(datas, markerPositions, num,marker)
    if len(markerPositions) <= 1:
        return np.array([]),np.array([]),np.array([]),np.array([])

    nSeries = len(markerPositions) - 1

    td = []
    pp = []

    if len(markerPositions1) > 0:
        for i in range(nSeries):
            if markertype == 1 and markerPositions[i] in markerPositions0:
                continue
            if markertype == 0 and markerPositions[i] in markerPositions1:
                continue
            denoised = obtain_denoise(datas, markerPositions, i, num, markertype, markerPositions1)
            td = obtain_thick(denoised, minpeak, t, td)
            pp.append(np.max(denoised) - np.min(denoised))
    else:
        for i in range(nSeries):
            series = __decodeTimeSeries(datas, markerPositions, i, num)
            denoised = __removeNoise(series,num,1)
            td = obtain_thick(denoised, minpeak, t, td)
            pp.append(np.max(denoised) - np.min(denoised))

    precision = pulseToMM/1000
    xList, yList = obtain_xy(datas, markerPositions, num, precision)

    if markertype == 0:
        xList = xList[0::2]
        yList = yList[0::2]
    elif markertype == 1:
        xList = xList[1::2]
        yList = yList[1::2]

    return xList, yList, np.array(pp),np.array(td)


def obtain_thick(thz_signal,minpeak,t,td):
    if t[1] - t[0] != 0:
        unit_ps = np.floor(1 / (t[1] - t[0]))
    else:
        unit_ps = 50
    peaks, _ = signal.find_peaks(thz_signal, height=max(thz_signal) * minpeak, distance=2 * unit_ps)

    peak_value = thz_signal[peaks]
    result = np.vstack((peak_value, peaks))
    result = result.T[np.lexsort(result[::-1, :])].T

    if result.shape[1] > 1:
        peaks = np.abs((result[1,-1] - result[1,-2]) * (t[1] - t[0]))
    else:
        peaks = 0
    td.append(peaks)
    return td

def obtain_denoise(dataList, markerPositions, i, nPoints, delay_line, markerPositions1):
    series = __decodeTimeSeries(dataList, markerPositions, i, nPoints)
    denoised = __removeNoise(series,nPoints,1)
    if delay_line == 2 and markerPositions[i] not in markerPositions1:
        denoised = denoised[::-1]
    if delay_line == 0:
        denoised = denoised[::-1]
    return denoised.reshape(-1, )


def obtain_xy(dataList, markerPositions, nPoints,precision):
    x1 = np.tile(np.arange(4, 8), (len(markerPositions)-1, 1)) + 2 * nPoints
    y1 = np.tile(np.arange(8, 12), (len(markerPositions)-1, 1)) + 2 * nPoints
    xyIndices = np.array([markerPositions, markerPositions, markerPositions, markerPositions]).T[0:-1,:]
    x1 = x1 + xyIndices
    y1 = y1 + xyIndices
    nBits = 8
    x = np.arange(4)
    shiftBits = nBits * x
    xComponent = dataList[x1]
    yComponent = dataList[y1]
    xComponent = xComponent << shiftBits
    yComponent = yComponent << shiftBits
    xValue = xComponent.sum(1)
    yValue = yComponent.sum(1)
    umPerMm = 1000.0 * precision
    xValue = np.int32(xValue)
    xList = xValue / umPerMm
    yValue = np.int32(yValue)
    yList = yValue / umPerMm

    if precision != 1:
        threshold_1 = 16777216 / 1000 / precision - 1500
        xList1 = np.array(xList)
        xindex = np.array(np.where((xList1 - threshold_1 > 1000) & (xList1 > threshold_1)))
        xList1[xindex] = xList1[xindex] - 16777.215 / precision
        yList1 = np.array(yList)
        yindex = np.array(np.where((yList1 - threshold_1 > 1000) & (yList1 > threshold_1)))
        yList1[yindex] = yList1[yindex] - 16777.215 / precision
    else:
        xList1 = np.array(xList)
        xindex = np.array(np.where((xList1 - 15000 > 1000) & (xList1 > 15000)))
        xList1[xindex] = xList1[xindex] - 16777.215
        yList1 = np.array(yList)
        yindex = np.array(np.where((yList1 - 15000 > 1000) & (yList1 > 15000)))
        yList1[yindex] = yList1[yindex] - 16777.215
    return xList1,yList1

def convertData(xList, yList, ppval, td, timeSeriesList):
    M_pp = np.array([xList, yList, ppval])
    M_td = np.array([xList, yList, td])
    M_thz_sig = np.vstack((np.array(xList).reshape(-1,), np.array(yList).reshape(-1,)))
    M_thz_sig = np.vstack((M_thz_sig, np.array(timeSeriesList).T))
    return M_pp, M_td, M_thz_sig

def move_average_signal1(s,size):
    thz_signals = np.array([])

    for i in range(s.shape[0]):
        thz_signal = []
        for j in range(0, s.shape[1] // size):
            thz_signal.append(np.mean(s[i,j * size:(j + 1) * size]))
        if len(thz_signals) == 0:
            thz_signals = np.array(thz_signal)
        else:
            thz_signals = np.vstack((thz_signals,np.array(thz_signal)))
    return thz_signals

def move_average_signal(s,size):
    s = np.array(s).reshape(-1,)
    cov = np.ones(size)
    thz_signal = np.convolve(s, cov, 'same') / size
    return thz_signal

def removeNoise(x, nPoints, order):
    """ Remove noise from the input time series by polynomial fitting.
        TO DO Improve the method to denoise the time series
        order: the order of the polynomial fitting
    """
    t = range(nPoints)
    params = np.polyfit(t, x, order)
    noise = np.polyval(params, t)
    denoise = np.array(x) - np.array(noise)

    return denoise


def __findMarkerPositions(x, marker):
    """Find the positions of the marker, which is used to separate the adjacent time series, in x."""
    positions = []
    arr = np.where(x == marker[0])

    for i in range(len(arr[0])):
        if arr[0][i] + 3 >= len(x):
            continue
        if x[arr[0][i] + 1] == marker[1] and x[arr[0][i] + 2] == marker[2] and x[arr[0][i] + 3] == marker[3]:
            positions.append(arr[0][i])

    return positions


def __removeIllegalPositions(datalist, positions, nPoints,marker):
    x = datalist.copy()
    position = np.array(positions).copy()
    position_distance = np.diff(position)
    defaultDist = 2 * nPoints + 20
    lostPointsIndices = np.array(np.where(position_distance != defaultDist))
    lostPointsIndices = lostPointsIndices.reshape(lostPointsIndices.shape[1], )

    for index in lostPointsIndices:
        if position_distance[index] > defaultDist:
            num = position_distance[index] - defaultDist
            data = x[position[index] + 4:position[index] + 4 + num]
            if marker.shape[0] == 1:
                if np.sum(data == marker[-1]) == num:
                    positions[index] = positions[index] + num
                    position_distance[index] = position_distance[index] - num
            else:
                if np.sum(data == marker[0,-1]) == num or np.sum(data == marker[1,-1]) == num:
                    positions[index] = positions[index] + num
                    position_distance[index] = position_distance[index] - num

    lostPointsIndices1 = np.array(np.where(position_distance != defaultDist))
    lostPointsIndices1 = lostPointsIndices1.reshape(lostPointsIndices1.shape[1], )
    positions = np.delete(positions,lostPointsIndices1)
    return positions


def __removeNoise(x, nPoints, order):
    """ Remove noise from the input time series by polynomial fitting.
        TO DO Improve the method to denoise the time series
        order: the order of the polynomial fitting
    """
    t = range(nPoints)
    params = np.polyfit(t, x, order)
    noise = np.polyval(params, t)
    denoise = np.array(x) - np.array(noise)

    return denoise


def __decodeTimeSeries(dataList, positions, index, nPoints):
    position = positions[index]
    startPos = position + 4
    endPos = position + 2 * nPoints + 4
    seriesInList = dataList[startPos: endPos]
    seriesInList = np.array(seriesInList)
    seriesInListOdd = seriesInList[::2]
    seriesInListEven = seriesInList[1::2]
    decoded = seriesInListOdd + seriesInListEven * 256

    return decoded
