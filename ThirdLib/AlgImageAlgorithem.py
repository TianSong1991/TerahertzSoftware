# -*- coding: utf-8 -*-
"""
Create Time: 2021/3/22 9:28
Author: Kevin
"""
import numpy as np
from scipy import signal
from PIL import Image
import time
from ThirdLib.AlgSignalUtil import convertToFrequency
from scipy import ndimage
from ThirdLib.AlgConfig import  ImageConfig
import os
import pywt


def ImageChoose(ref_path,image_choose,fast_thz_time,M_thz_sig):
    try:
        if image_choose == 1:
            for i in range(M_thz_sig.shape[1]):
                _, xfRange = convertToFrequency(fast_thz_time,M_thz_sig[2:,i])
                M_thz_sig[2:, i] = xfRange[0:len(fast_thz_time)]
        with open(os.path.join(os.getcwd(),'ThirdLib','alg.log'), 'a+') as ff:
            if image_choose == 1:
                ff.write(
                    f'{time.strftime("%Y-%m-%d %X", time.localtime())} 3D Image use frequency to show! \n')
            else:
                ff.write(
                    f'{time.strftime("%Y-%m-%d %X", time.localtime())} 3D Image use original signal to show! \n')

    except Exception as e:
        with open(os.path.join(os.getcwd(),'ThirdLib','alg.log'), 'a+') as ff:
            ff.write(f'{time.strftime("%Y-%m-%d %X", time.localtime())} 3D Image image_choose wrong :{e} \n')

    return M_thz_sig


def New_3DImage(t_THz,M_THz_sig,platform,compress):
    z = int(t_THz/compress)
    x = M_THz_sig[0,:]
    y = M_THz_sig[1, :]
    inverse_y = y[-1] - y[0]

    peak, _ = signal.find_peaks(x)
    valley, _ = signal.find_peaks(-x)
    data_pv = np.append(peak, valley)
    data_pv = np.append(data_pv, [0, x.shape[0] - 1])
    data_pv.sort()
    data_diff = np.diff(data_pv)
    counts = np.bincount(data_diff)
    col_num = np.argmax(counts) + 1
    data3d = np.zeros((data_pv.shape[0] - 1, z, col_num))

    for i in range(data_pv.shape[0] - 1):
        if platform == 2:
            if x[data_pv[i+1]] < x[data_pv[i]] and inverse_y > 0:
                data3d[i, :, :] = np.array(Image.fromarray(M_THz_sig[2:, data_pv[i]:data_pv[i+1]][:,::-1]).resize((col_num,z)))
            elif x[data_pv[i+1]] < x[data_pv[i]] and inverse_y < 0:
                data3d[i, :, :] = np.array(Image.fromarray(M_THz_sig[2:, data_pv[i]:data_pv[i+1]][::-1,::-1]).resize((col_num,z)))
            elif x[data_pv[i+1]] > x[data_pv[i]] and inverse_y < 0:
                data3d[i, :, :] = np.array(Image.fromarray(M_THz_sig[2:, data_pv[i]:data_pv[i+1]][::-1,:]).resize((col_num,z)))
            else:
                data3d[i, :, :] = np.array(Image.fromarray(M_THz_sig[2:, data_pv[i]:data_pv[i+1]]).resize((col_num,z)))
        else:
            if x[data_pv[i + 1]] < x[data_pv[i]] and inverse_y > 0:
                data3d[i, :, :] = np.array(
                    Image.fromarray(M_THz_sig[2:, data_pv[i]:data_pv[i + 1]][:, :]).resize((col_num, z)))
            elif x[data_pv[i + 1]] < x[data_pv[i]] and inverse_y < 0:
                data3d[i, :, :] = np.array(
                    Image.fromarray(M_THz_sig[2:, data_pv[i]:data_pv[i + 1]][::-1, :]).resize((col_num, z)))
            elif x[data_pv[i + 1]] > x[data_pv[i]] and inverse_y < 0:
                data3d[i, :, :] = np.array(
                    Image.fromarray(M_THz_sig[2:, data_pv[i]:data_pv[i + 1]][::-1, ::-1]).resize((col_num, z)))
            else:
                data3d[i, :, :] = np.array(
                    Image.fromarray(M_THz_sig[2:, data_pv[i]:data_pv[i + 1]][:, ::-1]).resize((col_num, z)))

    return data3d

def xyThzsgl(x_pos, y_pos, mThz):
    if mThz.shape[0] < 1:
        return np.array([])
    orgxy = mThz[0:2,:].copy()

    x_pos1 = x_pos + min(orgxy[0,:])
    y_pos1 = y_pos + min(orgxy[1,:])
    sum_xy = np.abs(orgxy[0,0]) - x_pos1 + np.abs(orgxy[1,0] - y_pos1)
    index = 0
    for i in range(1,orgxy.shape[1]):
        if sum_xy > np.abs(orgxy[0,i]- x_pos1)  + np.abs(orgxy[1,i] - y_pos1):
            sum_xy = np.abs(orgxy[0,i]- x_pos1)  + np.abs(orgxy[1,i] - y_pos1)
            index = i
    sigThzxy = mThz[2:,index].T.copy()
    return sigThzxy


def removeNoise(x):
    t = np.arange(len(x))
    params = np.polyfit(t,x,1)
    noise = np.polyval(params,t)
    denoised = np.array(x) - np.array(noise)
    return denoised


def obtain_alpha(c,max_range,mode):
    minv, maxv = c['range']

    if abs(minv) > abs(maxv):
        min_range = abs(minv)
    else:
        min_range = abs(maxv)

    if len(mode) > 0 and os.path.exists(os.path.join(ImageConfig.color_path, str(mode) + '.txt')):
        path_color = os.path.join(ImageConfig.color_path, str(mode) + '.txt')
        color_data = np.loadtxt(path_color)
        value_data = minv + np.arange(max_range) * (maxv - minv) / max_range
        m = np.hstack([value_data.reshape(max_range, 1), color_data])
        m = m.tolist()
    else:
        value_0 = minv + np.arange(max_range) * (maxv - minv) / max_range
        value_r = np.arange(max_range) / max_range
        value_g = np.arange(max_range) / max_range
        value_b = np.arange(max_range) / max_range
        m = np.hstack([value_0.reshape(max_range, 1), value_r.reshape(max_range, 1), value_g.reshape(max_range, 1),
                       value_b.reshape(max_range, 1)])
        m = m.tolist()
    alpha = []
    alpha.append([-min_range, 0])
    alpha.append([-min_range * 0.8, 0.9])
    alpha.append([-min_range * 0.5, 0.2])
    alpha.append([-min_range * 0.3, 0.01])
    alpha.append([min_range * 0.3, 0.01])
    alpha.append([min_range * 0.5, 0.01])
    alpha.append([min_range * 0.8, 0.2])
    alpha.append([min_range, 0.9])
    c['rgb'] = m
    c['alpha'] = alpha
    return c

def xyz_orientation(data, num):
    if num == 0:
        return data
    elif num == 1:
        return np.fliplr(data)
    elif num == 2:
        return np.flipud(data)
    elif num == 3:
        return np.fliplr(np.flipud(data))
    elif num == 4:
        return ndimage.rotate(data,90)
    elif num == 5:
        return np.fliplr(ndimage.rotate(data,90))
    elif num == 6:
        return np.flipud(ndimage.rotate(data,90))
    elif num == 7:
        return ndimage.rotate(data,270)
    elif num == 8:
        return np.fliplr(ndimage.rotate(data,270))
    elif num == 9:
        return np.flipud(ndimage.rotate(data,270))
    else:
        return data


def convertData(xList, yList,timeSeriesList,unpack_params):
    x = unpack_params[0]
    dx = unpack_params[1]
    x_max = unpack_params[2]
    y = unpack_params[3]
    y_max = unpack_params[5]
    delete_d = unpack_params[6]
    data = np.array(timeSeriesList)
    M_thz_sig = np.vstack((xList, yList))

    M_thz_sig = np.vstack((M_thz_sig, data))
    M_thz_sig = cut_Data(M_thz_sig, xList, yList, dx, x_max, x, y_max, y, delete_d)
    return M_thz_sig


def cut_Data(M_thz_sig,xList,yList,dx,x_max,x_min,y_max,y_min,delete_d):
    xlist = np.array(xList)
    ylist = np.array(yList)
    xlist_diff = np.diff(xlist)
    delete_d0 = np.array(np.where(np.abs(xlist_diff) < delete_d*dx))
    delete_d1 = np.array(np.where(np.abs(xlist_diff) > 4 * dx))
    delete_x = np.append(delete_d0,delete_d1)
    delete_x = np.unique(delete_x)
    with open(os.path.join(os.getcwd(),'ThirdLib','alg.log'), 'a+', encoding='utf-8') as ff:
        ff.write(f'{time.strftime("%Y-%m-%d %X", time.localtime())} 3D Image total x cord: {len(xlist)} points! \n')
        ff.write(f'{time.strftime("%Y-%m-%d %X", time.localtime())} 3D Image delete x cord: {len(delete_x)} points! \n')
        ff.write(f'{time.strftime("%Y-%m-%d %X", time.localtime())} 3D Image input x cord range is : {x_min} - {x_max} \n')
        ff.write(f'{time.strftime("%Y-%m-%d %X", time.localtime())} 3D Image solve x cord range is : {np.min(xlist)} - {np.max(xlist)} \n')
        ff.write(f'{time.strftime("%Y-%m-%d %X", time.localtime())} 3D Image input y cord range is : {y_min} - {y_max} \n')
        ff.write(f'{time.strftime("%Y-%m-%d %X", time.localtime())} 3D Image solve y cord range is : {np.min(ylist)} - {np.max(ylist)} \n')

    delete_x = delete_x.reshape(-1, )
    M_thz_sig = np.delete(M_thz_sig, delete_x, 1)
    return M_thz_sig

def image_filter(M_thz_sig,param1):
    if param1 == 1:
        if M_thz_sig.shape[0] - 2 >= 9000:
            num1 = 31
            num2 = 300
        elif M_thz_sig.shape[0] - 2 < 3000:
            num1 = 7
            num2 = 100
        else:
            num1 = 15
            num2 = 100
        for i in range(M_thz_sig.shape[1]):
            filter1 = signal.medfilt(M_thz_sig[2:, i], num1)
            mcoeffs = pywt.wavedec(filter1, 'db5', mode='symmetric', level=5)
            for k in range(1, len(mcoeffs)):
                value = np.sqrt(2 * np.log(filter1.shape[0]))
                mcoeffs[k] = pywt.threshold(np.array(mcoeffs[k]), value=value, mode='soft')
            mediandwt = pywt.waverec(mcoeffs, wavelet='db5', mode='symmetric')
            n = int(num2 / 1)
            baseline = (np.convolve(mediandwt, np.ones((n,)) / n, mode="same"))
            data1 = mediandwt - baseline
            M_thz_sig[2:, i] = data1

    return M_thz_sig

def robotPPThick(signals,row_num):
    if signals.shape[1] <= row_num:
        return np.array([]), np.array([])
    else:
        num1 = int(np.floor(signals.shape[1] / row_num))
        ppResult = np.zeros((num1, row_num))
        thickResult = np.zeros((num1, row_num))
        pps = signals[3,:]
        thicks = signals[4,:]
        for i in range(num1):
            if i % 2 == 0:
                ppResult[i, :] = pps[i * row_num:(i + 1) * row_num]
                thickResult[i, :] = thicks[i * row_num:(i + 1) * row_num]
            else:
                ppResult[i, :] = pps[i * row_num:(i + 1) * row_num][::-1]
                thickResult[i, :] = thicks[i * row_num:(i + 1) * row_num][::-1]
    return ppResult,thickResult
