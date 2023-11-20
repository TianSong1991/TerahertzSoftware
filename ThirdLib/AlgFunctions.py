# -*- coding: utf-8 -*-
"""
Create Time: 2021/10/26 9:19
Author: Kevin
Python Version：3.7.6
"""
from ThirdLib.AlgSignalUtil import *
from ThirdLib.AlgConfig import AlgConfig
from scipy.interpolate import griddata
import pandas as pd
from scipy.interpolate import NearestNDInterpolator
import numpy as np
from scipy import signal
from PIL import Image
import time
from ThirdLib.AlgSignalUtil import convertToFrequency
from scipy import ndimage
from ThirdLib.AlgConfig import  ImageConfig
import os

#实现解包和成像功能,与C#版本里的函数一致
class Functions():
	@staticmethod
	def calFrequency(t, ref,maxFreq=15):
		if len(ref) > 50:
			t_value = t
			ref_value = ref
			fRange, xfRange = convertToFrequency(t_value, ref_value)
			xfRange = np.array(xfRange)
			fRange = np.array(fRange)
			xfRange = xfRange[0:int(np.floor(xfRange.shape[0] / 2))]
			fRange = fRange[0:int(np.floor(fRange.shape[0] / 2))]
			if np.max(xfRange[fRange > 0.1]) < 0:
				xfRange[fRange > 0.1] = xfRange[fRange > 0.1] - np.max(xfRange[fRange > 0.1])
			xfRange = xfRange[fRange <= maxFreq]
			fRange = fRange[fRange <= maxFreq]
		else:
			with open(os.path.join(os.getcwd(), 'alg.log'), 'a+', encoding='utf-8') as f:
				f.write(
					f'{time.strftime("%Y-%m-%d %X", time.localtime())} Alg calFrequency fail: The length of the signal must be more than 50! \n')
			fRange, xfRange = np.array([]), np.array([])
		return fRange, xfRange

	@staticmethod
	def calUnpackData(data, nPoints, delay_line):
		fast_thz_signal = unpackData(data, int(nPoints), delay_line)
		return fast_thz_signal

	@staticmethod
	def calUnpackDataImage(t, datas, num, compress_signal, markertype, minpeak, pulseToMM):
		xList, yList, pp, td, timeSeriesList = unpackDataImage(t, datas, num,compress_signal, markertype, minpeak, pulseToMM)
		return xList, yList, pp, td, timeSeriesList

	@staticmethod
	def calUnpackDataRobot(t, datas, num, compress_signal, markertype, minpeak,pulseToMM):
		xList, yList, pp, td, timeSeriesList = unpackDataRobot(t, datas, num,compress_signal, markertype, minpeak, pulseToMM)
		xList, yList, pp, td, timeSeriesList = Functions.deleteXlist(xList, yList, pp, td, timeSeriesList)

		return xList, yList, pp, td, timeSeriesList

	@staticmethod
	def deleteXlist(xList, yList, pp, td, timeSeriesList):
		xList = xList * 1000
		yList = yList * 1000

		params = ImageConfig()
		params.init()
		params.updateParams()

		if params.robot_delete == 1:
			delete_x = np.array(np.where(xList == 0))
			delete_x = delete_x.reshape(-1, )
			xList = np.delete(xList, delete_x, 0)
			yList = np.delete(yList, delete_x, 0)
			pp = np.delete(pp, delete_x, 0)
			td = np.delete(td, delete_x, 0)
			timeSeriesList = np.delete(timeSeriesList, delete_x, 0)
			if timeSeriesList.shape[0] == 0:
				timeSeriesList = np.array([])

		return xList, yList, pp, td, timeSeriesList

	@staticmethod
	def calUnpackDataImageAll(t, datas, num, markertype, minpeak,params,cols,pulseToMM):
		xList, yList, pp, thick, timeSeriesList = unpackDataImage(t, datas, num, markertype, minpeak, pulseToMM)
		result = np.vstack((xList, yList))
		result = np.vstack((result, pp))
		result = np.vstack((result, thick))
		ppResult, thickResult = Functions.obtainPPThickImage(result,params[1],params[4],cols)
		return ppResult, thickResult,timeSeriesList

	@staticmethod
	def calUnpackDataImageActual(t, datas, num, markertype, minpeak, pulseToMM):
		xList, yList, pp, td = unpackDataImageActual(t, datas, num, markertype, minpeak, pulseToMM)
		return xList, yList, pp, td


	@staticmethod
	def New_3DImage(M_THz_sig, platform, compress):
		z = int((M_THz_sig.shape[0] - 2) / compress)
		x = M_THz_sig[0, :]
		y = M_THz_sig[1, :]
		inverse_y = y[-1] - y[0]

		peak, _ = signal.find_peaks(x)
		valley, _ = signal.find_peaks(-x)
		data_pv = np.append(peak, valley)
		data_pv = np.append(data_pv, [0, x.shape[0] - 1])
		data_pv.sort()
		data_pv = np.unique(data_pv)
		if len(data_pv) < 2:
			return np.array([])
		data_diff = np.diff(data_pv)
		counts = np.bincount(data_diff)
		col_num = np.argmax(counts) + 1
		data3d = np.zeros((data_pv.shape[0] - 1, z, col_num))

		for i in range(data_pv.shape[0] - 1):
			if platform == 2:
				if x[data_pv[i + 1]] < x[data_pv[i]] and inverse_y > 0:
					data3d[i, :, :] = np.array(
						Image.fromarray(M_THz_sig[2:, data_pv[i]:data_pv[i + 1]][:, ::-1]).resize((col_num, z)))
				elif x[data_pv[i + 1]] < x[data_pv[i]] and inverse_y < 0:
					data3d[i, :, :] = np.array(
						Image.fromarray(M_THz_sig[2:, data_pv[i]:data_pv[i + 1]][::-1, ::-1]).resize((col_num, z)))
				elif x[data_pv[i + 1]] > x[data_pv[i]] and inverse_y < 0:
					data3d[i, :, :] = np.array(
						Image.fromarray(M_THz_sig[2:, data_pv[i]:data_pv[i + 1]][::-1, :]).resize((col_num, z)))
				else:
					data3d[i, :, :] = np.array(
						Image.fromarray(M_THz_sig[2:, data_pv[i]:data_pv[i + 1]]).resize((col_num, z)))
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

	@staticmethod
	def Robot3DImage(M_THz_sig, compress, row_num):
		if M_THz_sig.shape[1] <= row_num:
			return np.array([])
		else:
			num1 = int(np.floor(M_THz_sig.shape[1] / row_num))
			data3d = np.zeros((int(row_num),int(M_THz_sig.shape[0]/compress),num1))
			for i in range(num1):
				if i % 2 == 0:
					data3d[:,:,i] = np.array(
					Image.fromarray(M_THz_sig[:,i*row_num:(i+1)*row_num].T).resize((int(M_THz_sig.shape[0]/compress), num1)))
				else:
					data3d[:,:,i] = np.fliplr(np.array(
					Image.fromarray(M_THz_sig[:,i*row_num:(i+1)*row_num].T).resize((int(M_THz_sig.shape[0]/compress), num1))))

		return data3d

	@staticmethod
	def convertData(xList, yList, timeSeriesList, unpack_params):
		x_min = unpack_params[0]
		dx = unpack_params[1]
		x_max = unpack_params[2]
		y_min = unpack_params[3]
		y_max = unpack_params[5]
		delete_d = unpack_params[6]
		data = np.array(timeSeriesList).T
		M_thz_sig = np.vstack((xList, yList))
		M_thz_sig = np.vstack((M_thz_sig, data))
		xlist = np.array(xList)
		ylist = np.array(yList)
		xlist_diff = np.diff(xlist)
		delete_d0 = np.array(np.where(np.abs(xlist_diff) < delete_d * dx))
		delete_d1 = np.array(np.where(np.abs(xlist_diff) > 4 * dx))
		delete_x = np.append(delete_d0, delete_d1)
		delete_x = np.unique(delete_x)
		delete_x = delete_x.reshape(-1, )
		M_thz_sig = np.delete(M_thz_sig, delete_x, 1)
		return M_thz_sig

	@staticmethod
	def calImage(t, THzsig_intp):
		rows = THzsig_intp.shape[0]
		cols = THzsig_intp.shape[2]
		peak_valley = np.zeros((rows, cols))
		thicks = np.zeros((rows, cols))
		unit_ps = np.floor(1 / (t[1] - t[0]))

		for i in range(rows):
			for j in range(cols):
				peak_valley[i, j] = np.max(THzsig_intp[i, :, j]) - np.min(THzsig_intp[i, :, j])

				peaks, _ = signal.find_peaks(THzsig_intp[i, :, j], height=max(THzsig_intp[i, :, j]) * 0.3,
											 distance=2 * unit_ps)
				if peaks.shape[0] > 1:
					thicks[i, j] = (peaks[1] - peaks[0]) * (t[1] - t[0])
				else:
					thicks[i, j] = 0
		return peak_valley, thicks

	@staticmethod
	def get_THzsig_intp(x, y, datas,startx, starty, endx, endy, stepx, stepy):
		readConfig = AlgConfig()
		params = readConfig.getParamsF()
		delete_d = params[2]
		unpack_params = [startx, stepx, endx, starty, stepy, endy, delete_d]
		M_thz_sig = Functions.convertData(x, y, datas, unpack_params)
		platform = params[0]
		compress = params[1]
		THzsig_intp = Functions.New_3DImage(M_thz_sig, platform, compress)
		return THzsig_intp

	@staticmethod
	def supply_data(python_value,points,pack_data, pp_method):
		if pp_method == 0:
			if pack_data.shape[0] != 0:
				if len(pack_data) > points:
					data_cut = pack_data[-points:]
				else:
					data_cut = np.array([])
				pack_data = np.append(data_cut, python_value)
			else:
				pack_data = python_value
		else:
			pack_data = python_value
		return pack_data

	@staticmethod
	def get_pp(xList,yList,pp,xlists,ylists,pps,xStep):
		xlists = np.around(np.append(xlists, xList),4)
		ylists = np.around(np.append(ylists, yList),4)
		pps = np.around(np.append(pps, pp),4)
		vpp = np.vstack((xlists, ylists))
		vpp = np.vstack((vpp, pps))
		readConfig = AlgConfig()
		open_mean = readConfig.if_open_mean()
		if open_mean == 1:
			data1 = pd.DataFrame(vpp.T)
			data1.columns = ['x', 'y', 'pp']
			data2 = data1.groupby(['x', 'y'], sort=False).mean()
			data2.reset_index(inplace=True)
			vpp = np.array(data2.T)
			xlists = vpp[0,:]
			ylists = vpp[1,:]
			pps = vpp[2,:]

		xlist_diff = np.diff(xlists)
		delete_d0 = np.array(np.where(np.abs(xlist_diff) < 0.5 * xStep))
		delete_d1 = np.array(np.where(np.abs(xlist_diff) > 4 * xStep))
		delete_x = np.append(delete_d0, delete_d1)
		delete_x = np.unique(delete_x)
		delete_x = delete_x.reshape(-1, )
		vpp = np.delete(vpp, delete_x, 1)
		xlists = np.delete(xlists, delete_x, 0)
		ylists = np.delete(ylists, delete_x, 0)
		pps = np.delete(pps, delete_x, 0)
		return xlists,ylists,pps,vpp

	@staticmethod
	def get_pp_result(xlists,ylists,pps,vpp,cols,result):
		ylist_diff = np.abs(np.diff(vpp[1, :]))
		peak, _ = signal.find_peaks(ylist_diff,height=np.max(ylist_diff)*0.5)
		peak = np.append(peak, [0])
		peak.sort()
		peak = np.unique(peak)
		print(peak)
		for i in range(len(peak) - 1):
			if result.shape[0] == 0:
				if result.shape[0] % 2 == 0:
					data = np.array(Image.fromarray(vpp[2, peak[i]:peak[i + 1]][::-1]).resize((1, cols))).reshape(1, cols)
				else:
					data = np.array(Image.fromarray(vpp[2, peak[i]:peak[i + 1]]).resize((1, cols))).reshape(1, cols)
				result = data
			else:
				if result.shape[0] % 2 == 0:
					data = np.array(Image.fromarray(vpp[2, peak[i]:peak[i + 1]][::-1]).resize((1, cols))).reshape(1, cols)
				else:
					data = np.array(Image.fromarray(vpp[2, peak[i]:peak[i + 1]]).resize((1, cols))).reshape(1, cols)
				result = np.vstack((result,data))
		max_index = np.max(peak)
		xlists = xlists[max_index + 1:]
		ylists = ylists[max_index + 1:]
		pps = pps[max_index + 1:]
		vpp = vpp[:, max_index + 1:]
		return xlists,ylists,pps,vpp,result

	@staticmethod
	def dealDataAllNet(xList, yList, pp, thick, signals, xlists, ylists, pps, thicks, signalAll, xStep):
		xlists = np.around(np.append(xlists, xList), 4)
		ylists = np.around(np.append(ylists, yList), 4)
		pps = np.around(np.append(pps, pp), 4)
		thicks = np.around(np.append(thick, thicks), 4)

		if len(signalAll) == 0:
			signalAll = signals.T
		else:
			if len(signals) != 0:
				signalAll = np.hstack((signalAll, signals.T))

		signalAll = np.around(signalAll, 4)

		readConfig = AlgConfig()

		open_mean = readConfig.if_open_mean()

		if open_mean == 1:
			vpp = np.vstack((xlists, ylists))
			vpp = np.vstack((vpp, pps))
			vpp = np.vstack((vpp, thicks))
			vpp = np.vstack((vpp, signalAll))

			data1 = pd.DataFrame(vpp.T)
			data2 = data1.groupby([0,1], sort=False).mean()
			data2.reset_index(inplace=True)
			vpp = np.array(data2.T)
			xlists = vpp[0, :]
			ylists = vpp[1, :]
			pps = vpp[2, :]
			thicks = vpp[3, :]
			signalAll = vpp[4:,:]

		result = np.vstack((xlists, ylists))
		result = np.vstack((result, pps))
		result = np.vstack((result, thicks))
		return xlists, ylists, pps, thicks, signalAll, result


	@staticmethod
	def dealDataAllNetJX(xList, yList, pp, thick, signals, xlists, ylists, pps, thicks, signalAll, xStep):
		xlists = np.around(np.append(xlists, xList), 4)
		ylists = np.around(np.append(ylists, yList), 4)
		pps = np.around(np.append(pps, pp), 4)
		thicks = np.around(np.append(thick, thicks), 4)

		if len(signalAll) == 0:
			signalAll = signals.T
		else:
			if len(signals) != 0:
				signalAll = np.hstack((signalAll, signals.T))

		signalAll = np.around(signalAll, 4)

		vpp = np.vstack((xlists, ylists))
		vpp = np.vstack((vpp, pps))
		vpp = np.vstack((vpp, thicks))

		data1 = pd.DataFrame(vpp.T)
		data2 = data1.groupby([0, 1], sort=False).mean()
		data2.reset_index(inplace=True)
		vpp = np.array(data2.T)
		xlists1 = vpp[0, :]
		ylists1 = vpp[1, :]
		pps1 = vpp[2, :]
		thicks1 = vpp[3, :]
		# signalAll = vpp[4:, :]

		result = np.vstack((xlists1, ylists1))
		result = np.vstack((result, pps1))
		result = np.vstack((result, thicks1))
		return xlists, ylists, pps, thicks, signalAll, result

	@staticmethod
	def obtainXYranges(xStart,xStep,cols,yStart,yStep,rows):
		xranges = []
		for i in range(cols):
			xranges.append(xStart + i * xStep)

		yranges = []
		for i in range(rows):
			yranges.append(yStart + i * yStep)

		return np.array(xranges),np.array(yranges)


	@staticmethod
	def obtainPPThickImageJX(result, xStart,xStep,xEnd,yStart,yStep,yEnd,xranges,yranges):
		xlists = result[0,:] - np.min(result[0,:]) + xStart
		ylists = result[1,:] - np.min(result[1,:]) + yStart
		pps = result[2,:]
		thicks = result[3,:]
		cols = int((xEnd - xStart) / xStep)
		rows = int((yEnd - yStart) / yStep)
		ppResultJX = np.zeros((rows, cols))
		thickResultJX = np.zeros((rows, cols))


		if len(xlists) > 0:
			for i in range(len(yranges)):
				for j in range(len(xranges)):
					if i%2 == 0:
						x1 = np.where((xlists <= xStart + 0.5 * xStep + j * xStep) & (xlists >= xStart - 0.5*xStep + j * xStep))
						x1 = np.array(x1)
					else:
						x1 = np.where(
							(xlists <= xEnd + 0.5 * xStep - j * xStep) & (xlists >= xEnd - 0.5 * xStep - j * xStep))
						x1 = np.array(x1)
					y1 = np.where((ylists <= yStart + 0.5 * yStep + i * yStep) & (ylists >= yStart - 0.5*yStep + i * yStep))
					y1 = np.array(y1)
					xy = np.intersect1d(x1,y1)
					if len(xy) == 0:
						continue
					else:
						if i % 2 == 0:
							ppResultJX[rows -1 - i,j] = np.mean(pps[xy])
							thickResultJX[rows -1- i, j] = np.mean(thicks[xy])
						else:
							ppResultJX[rows - 1-i,-j] = np.mean(pps[xy])
							thickResultJX[rows -1- i, -j] = np.mean(thicks[xy])

			data1 = np.sum(ppResultJX,axis=1)
			data2 = np.array(np.where(data1 != 0))
			row_index = np.int(np.min(data2))
			ppResultJX = ppResultJX[row_index:,:]
			thickResultJX = thickResultJX[row_index:,:]
			pp1 = np.sort(np.unique(ppResultJX.flatten()))
			if len(pp1) > 1:
				pp1 = pp1[1]
			else:
				pp1 = pp1[0]
			thick1 = np.sort(np.unique(thickResultJX.flatten()))
			if len(thick1) > 1:
				thick1 = thick1[1]
			else:
				thick1 = thick1[0]
			for i in range(ppResultJX.shape[0]):
				for j in range(ppResultJX.shape[1]):
					if ppResultJX[i,j] == 0:
						ppResultJX[i, j] = pp1
			for i in range(thickResultJX.shape[0]):
				for j in range(thickResultJX.shape[1]):
					if thickResultJX[i, j] == 0:
						thickResultJX[i, j] = thick1

			if ppResultJX.shape[1] == cols:
				ppResultJX = ppResultJX[:,1:]
				thickResultJX = thickResultJX[:,1:]

			if ppResultJX.shape[0] > 1:
				ppResultJX = ppResultJX[:-1,:]
				thickResultJX = thickResultJX[:-1,:]

			ppResultJX = np.flipud(ppResultJX)
			thickResultJX = np.flipud(thickResultJX)

		return ppResultJX,thickResultJX





	@staticmethod
	def writeTime(time1,time0):
		with open(os.path.join(os.getcwd(), 'ThirdLib', 'alg.log'), 'a+', encoding='utf-8') as ff:
			ff.write(f'{time.strftime("%Y-%m-%d %X", time.localtime())} Cost time : {time1 - time0} \n')



	@staticmethod
	def averageSignal(xlists,ylists,pps,thicks,signalAll,threshold):
		if len(xlists) > 0:
			x1 = np.vstack((xlists, xlists)).T
			x1[:,1] = 1.0
			x2 = pd.DataFrame(x1)
			x3 = x2.groupby([0], sort=False).sum()
			x3.reset_index(inplace=True)
			x4 = np.array(x3.T)
			a = x4[1,:] >= threshold
			a1 = a.astype(np.int)
			a2 = np.vstack((x4, a1))
			a3 = np.where(a2[2, :] == 1)
			a4 = a2[0, a3]
			a4 = a4.reshape(-1)

			index0 = []

			for i in range(len(xlists)):
				if xlists[i] not in a4:
					index0.append(i)

			xlists1 = np.delete(xlists,index0)
			ylists1 = np.delete(ylists, index0)
			pps1 = np.delete(pps, index0)
			thicks1 = np.delete(thicks, index0)
			signalAll1 = np.delete(signalAll, index0,axis=1)

			vpp = np.vstack((xlists1, ylists1))
			vpp = np.vstack((vpp, pps1))
			vpp = np.vstack((vpp, thicks1))
			vpp = np.vstack((vpp, signalAll1))

			data1 = pd.DataFrame(vpp.T)
			data2 = data1.groupby([0], sort=False).mean()
			data2.reset_index(inplace=True)
			vpp = np.array(data2.T)
			xlists1 = vpp[0, :]
			ylists1 = vpp[1, :]
			pps1 = vpp[2, :]
			thicks1 = vpp[3, :]
			signalAll1 = vpp[4:,:]

			xmax = np.max(xlists)
			ymax = np.max(ylists)
			xmin = np.min(xlists)
			ymin = np.min(ylists)
			x_vec = np.arange(xmin, xmax, 0.1)
			y_vec = np.arange(ymin, ymax, 0.1)
			x, y = np.meshgrid(x_vec, y_vec)
			pps1 = np.array(pps1)
			thicks1 = np.array(thicks1)
			points1 = np.vstack((xlists1, ylists1)).T
			readConfig = AlgConfig()
			_, griddata_method = readConfig.choose_pp()
			pp_image = readConfig.image_change()

			try:
				ppResult, thickResult = np.array([]), np.array([])
				ppResult = griddata(points1, pps1, (x, y), method=griddata_method)
				ppResult = Functions.fillNan(ppResult)
				thickResult = griddata(points1, thicks1, (x, y), method=griddata_method)
				thickResult = Functions.fillNan(thickResult)
				ppResult = ImageFunctions.change_image(ppResult, pp_image)
				thickResult = ImageFunctions.change_image(thickResult, pp_image)

			except Exception as e:
				with open(os.path.join(os.getcwd(), 'ThirdLib', 'alg.log'), 'a+', encoding='utf-8') as ff:
					ff.write(f'{time.strftime("%Y-%m-%d %X", time.localtime())} The error is : {e} \n')
			return ppResult, thickResult,signalAll1[:,-1]








	@staticmethod
	def dealDataAll(xList,yList,pp, thick,signals, xlists,ylists,pps,thicks,signalAll,xStep):
		xlists = np.around(np.append(xlists, xList),4)
		ylists = np.around(np.append(ylists, yList),4)
		pps = np.around(np.append(pps, pp),4)
		thicks = np.around(np.append(thick, thicks), 4)

		if len(signalAll) == 0:
			signalAll = signals.T
		else:
			if len(signals) != 0:
				signalAll = np.hstack((signalAll,signals.T))

		signalAll = np.around(signalAll, 4)

		readConfig = AlgConfig()

		open_mean = readConfig.if_open_mean()

		if open_mean == 1:
			vpp = np.vstack((xlists, ylists))
			vpp = np.vstack((vpp, pps))
			vpp = np.vstack((vpp, thicks))

			data1 = pd.DataFrame(vpp.T)
			data1.columns = ['x', 'y', 'pp','thick']
			data2 = data1.groupby(['x', 'y'], sort=False).mean()
			data2.reset_index(inplace=True)
			vpp = np.array(data2.T)
			xlists = vpp[0,:]
			ylists = vpp[1,:]
			pps = vpp[2,:]
			thicks = vpp[3, :]


		result = np.vstack((xlists, ylists))
		result = np.vstack((result, pps))
		result = np.vstack((result, thicks))
		return xlists,ylists,pps,thicks,signalAll,result

	@staticmethod
	def robotData(xList,pp, thick,signals, xlists,pps,thicks,signalAll, pps_robot,thicks_robot,datax,mean_num):
		xlists = np.append(xlists, xList)
		pps = np.append(pps, pp)
		thicks = np.append(thick, thicks)
		if len(signalAll) == 0:
			signalAll = signals
		else:
			signalAll = np.vstack((signalAll,signals))

		if len(xList) > 0:
			data = np.vstack((xlists, pps))
			data = np.vstack((data, thicks))
			data = np.vstack((data,signalAll.T))

			x1 = np.vstack((xlists, xlists)).T
			x1[:,1] = 1.0
			x2 = pd.DataFrame(x1)
			x3 = x2.groupby([0], sort=False).sum()
			x3.reset_index(inplace=True)
			x4 = np.array(x3.T)
			x5 = np.hstack((np.array([0,0]).reshape(2,1),x4))


			for i in range(1,x5.shape[1]):
				if datax[1,i-1] < mean_num:
					if x5[1,i] < mean_num:
						if datax[1,i-1] + x5[1,i] < mean_num:
							data1 = pd.DataFrame(data[:,int(np.sum(x5[1,0:i])):int(np.sum(x5[1,0:i]) + x5[1,i])].T)
							data2 = data1.groupby([0], sort=False).mean()
							data2.reset_index(inplace=True)
							data3 = np.array(data2.T)
							pps_robot[i-1] = data3[1]
							thicks_robot[i-1] = data3[2]
							signalAll[i-1, :] = data3[3:].reshape(-1, )
							datax[1,i-1] = datax[1,i-1] + x5[1,i]
						else:
							data1 = pd.DataFrame(data[:,int(np.sum(x5[1,0:i])):int(mean_num - datax[1,i-1] + np.sum(x5[1,0:i]))].T)
							data2 = data1.groupby([0], sort=False).mean()
							data2.reset_index(inplace=True)
							data3 = np.array(data2.T)
							pps_robot[i-1] = data3[1]
							thicks_robot[i-1] = data3[2]
							signalAll[i-1, :] = data3[3:].reshape(-1, )
							datax[1,i-1] = mean_num
					else:
						data1 = pd.DataFrame(data[:,int(np.sum(x5[1,0:i])):int(np.sum(x5[1,0:i]) + mean_num)].T)
						data2 = data1.groupby([0], sort=False).mean()
						data2.reset_index(inplace=True)
						data3 = np.array(data2.T)
						pps_robot[i-1] = data3[1]
						thicks_robot[i-1] = data3[2]
						signalAll[i-1, :] = data3[3:].reshape(-1, )
						datax[1,i-1] = mean_num


			xlists = x4[0,:]
			pps = pps_robot[0:x4.shape[1]]
			thicks = thicks_robot[0:x4.shape[1]]
			signalAll = signalAll[0:x4.shape[1],:]

		return xlists,pps,thicks,signalAll,pps_robot,thicks_robot,datax

	@staticmethod
	def robot_data(path):
		if os.path.exists(path):
			data = pd.read_csv(path, header=None)

			data = data.iloc[1:-1, :].values

			x = data[:, 0]
			y = data[:, 1]

			x1 = np.diff(x)
			y1 = np.diff(y)
			dx = np.max(x1)
			dy = np.max(y1)
			if x1[0] == 0:
				x, y = y, x
				dx, dy = dy, dx
				deltx = x[1] - x[0]
				delty = y[0] - y[-1]
				if deltx > 0 and delty > 0:
					num = 4
				elif deltx > 0 and delty < 0:
					num = 5
				elif deltx < 0 and delty > 0:
					num = 6
				else:
					num = 7
			else:
				deltx = x[1] - x[0]
				delty = y[0] - y[-1]
				if deltx > 0 and delty > 0:
					num = 0
				elif deltx > 0 and delty < 0:
					num = 1
				elif deltx < 0 and delty > 0:
					num = 2
				else:
					num = 3
		else:
			raise Exception("Alfconfig.yaml 中没有配置正确的机械臂文件路径，路径错误请重新修改正确路径！")

		return x, y, num, dx, dy

	@staticmethod
	def dealData(xList,yList,pp, thick, xlists,ylists,pps,thicks,xStep):
		xlists = np.around(np.append(xlists, xList),4)
		ylists = np.around(np.append(ylists, yList),4)
		pps = np.around(np.append(pps, pp),4)
		thicks = np.around(np.append(thick, thicks), 4)
		readConfig = AlgConfig()
		open_mean = readConfig.if_open_mean()

		if open_mean == 1:
			vpp = np.vstack((xlists, ylists))
			vpp = np.vstack((vpp, pps))
			vpp = np.vstack((vpp, thicks))

			data1 = pd.DataFrame(vpp.T)
			data1.columns = ['x', 'y', 'pp','thick']
			data2 = data1.groupby(['x', 'y'], sort=False).mean()
			data2.reset_index(inplace=True)
			vpp = np.array(data2.T)
			xlists = vpp[0,:]
			ylists = vpp[1,:]
			pps = vpp[2,:]
			thicks = vpp[3, :]

		result = np.vstack((xlists, ylists))
		result = np.vstack((result, pps))
		result = np.vstack((result, thicks))
		return xlists,ylists,pps,thicks,result

	@staticmethod
	def thickData(xList,yList,thick,xlists,ylists,thicks,xStep):
		xlists = np.around(np.append(xlists, xList),4)
		ylists = np.around(np.append(ylists, yList),4)
		thicks = np.around(np.append(thicks, thick),4)
		readConfig = AlgConfig()
		open_mean = readConfig.if_open_mean()

		if open_mean == 1:
			vpp = np.vstack((xlists, ylists))
			vpp = np.vstack((vpp, thicks))

			data1 = pd.DataFrame(vpp.T)
			data1.columns = ['x', 'y', 'pp']
			data2 = data1.groupby(['x', 'y'], sort=False).mean()
			data2.reset_index(inplace=True)
			vpp = np.array(data2.T)
			xlists = vpp[0,:]
			ylists = vpp[1,:]
			thicks = vpp[2,:]

		xlist_diff = np.diff(xlists)
		delete_d0 = np.array(np.where(np.abs(xlist_diff) < 0.5 * xStep))
		delete_d1 = np.array(np.where(np.abs(xlist_diff) > 4 * xStep))
		delete_x = np.append(delete_d0, delete_d1)
		delete_x = np.unique(delete_x)
		delete_x = delete_x.reshape(-1, )
		xlists = np.delete(xlists, delete_x, 0)
		ylists = np.delete(ylists, delete_x, 0)
		thicks = np.delete(thicks, delete_x, 0)
		result = np.vstack((xlists, ylists))
		result = np.vstack((result, thicks))
		return xlists,ylists,thicks,result

	@staticmethod
	def getPPThicks(xlists,ylists,xStep,yStep,t,data):
		pps = []
		thicks = []
		readConfig = AlgConfig()
		_, griddata_method = readConfig.choose_pp()
		for i in range(data.shape[1]):
			pps.append(np.max(data[:,i]) - np.min(data[:,i]))
			thicks = obtain_thick(data[:,i], 0.3, t, thicks)

		xmax = np.max(xlists)
		ymax = np.max(ylists)
		xmin = np.min(xlists)
		ymin = np.min(ylists)
		x_vec = np.arange(xmin, xmax, xStep)
		y_vec = np.arange(ymin, ymax, yStep)
		x, y = np.meshgrid(x_vec, y_vec)
		pps = np.array(pps)
		thicks = np.array(thicks)
		points = np.vstack((xlists,ylists)).T
		pp_image = readConfig.image_change()

		try:
			ppResult, thickResult = np.array([]),np.array([])
			ppResult = griddata(points, pps, (x, y), method=griddata_method)
			ppResult = Functions.fillNan(ppResult)
			thickResult = griddata(points, thicks, (x, y), method=griddata_method)
			thickResult = Functions.fillNan(thickResult)
			ppResult = ImageFunctions.change_image(ppResult, pp_image)
			thickResult = ImageFunctions.change_image(thickResult, pp_image)

		except Exception as e:
			with open(os.path.join(os.getcwd(), 'ThirdLib','alg.log'), 'a+', encoding='utf-8') as ff:
				ff.write(f'{time.strftime("%Y-%m-%d %X", time.localtime())} The error is : {e} \n')
		return ppResult,thickResult


	@staticmethod
	def obtainPPThickImage(Mpp_Org,dx,dy,cols):
		xmax = np.max(Mpp_Org[0, :])
		ymax = np.max(Mpp_Org[1, :])
		xmin = np.min(Mpp_Org[0, :])
		ymin = np.min(Mpp_Org[1, :])
		x_vec = np.arange(xmin, xmax, dx)
		y_vec = np.arange(ymin, ymax, dy)
		x, y = np.meshgrid(x_vec, y_vec)
		points = np.array(Mpp_Org[0:2, :]).T
		ppValues = np.array(Mpp_Org[2, :])
		thickValues = np.array(Mpp_Org[3, :])
		readConfig = AlgConfig()
		_,griddata_method = readConfig.choose_pp()
		pp_image = readConfig.image_change()


		try:
			ppResult, thickResult = np.array([]),np.array([])
			ppResult = griddata(points, ppValues, (x, y), method=griddata_method)
			ppResult = Functions.fillNan(ppResult)
			thickResult = griddata(points, thickValues, (x, y), method=griddata_method)
			thickResult = Functions.fillNan(thickResult)
			ppResult = ImageFunctions.change_image(ppResult, pp_image)
			thickResult = ImageFunctions.change_image(thickResult, pp_image)

		except Exception as e:
			with open(os.path.join(os.getcwd(), 'ThirdLib','alg.log'), 'a+', encoding='utf-8') as ff:
				ff.write(f'{time.strftime("%Y-%m-%d %X", time.localtime())} The error is : {e} \n')

		return ppResult,thickResult

	@staticmethod
	def obtainRobotImage(xlists, pps, thicks, cols):
		if len(xlists) <= cols:
			return np.array([]),np.array([])
		else:
			num1 = int(np.floor(len(xlists)/cols))
			ppResult = np.zeros((num1,cols))
			thickResult = np.zeros((num1,cols))
			for i in range(num1):
				if i % 2 == 0:
					ppResult[i, :] = pps[i * cols:(i + 1) * cols]
					thickResult[i, :] = thicks[i * cols:(i + 1) * cols]
				else:
					ppResult[i, :] = pps[i * cols:(i + 1) * cols][::-1]
					thickResult[i, :] = thicks[i * cols:(i + 1) * cols][::-1]

		return ppResult,thickResult

	@staticmethod
	def robotImage(xlists,pps,thicks,robot_x,robot_y,robot_num,dx,dy):
		ppResult, thickResult = np.array([]), np.array([])
		if len(xlists) > 0:
			if len(xlists) > len(robot_x):
				num = len(robot_x)
			else:
				num = len(xlists)
			xlists = robot_x[0:num]
			ylists = robot_y[0:num]

			xmax = np.max(xlists)
			ymax = np.max(ylists)
			xmin = np.min(xlists)
			ymin = np.min(ylists)
			x_vec = np.arange(xmin, xmax, 0.1)
			y_vec = np.arange(ymin, ymax, 0.1)
			x, y = np.meshgrid(x_vec, y_vec)
			points = np.vstack((xlists,ylists)).T
			ppValues = pps
			thickValues = thicks
			readConfig = AlgConfig()
			_,griddata_method = readConfig.choose_pp()

			try:

				ppResult = griddata(points, ppValues, (x, y), method=griddata_method)
				ppResult = Functions.fillNan(ppResult)

				thickResult = griddata(points, thickValues, (x, y), method=griddata_method)
				thickResult = Functions.fillNan(thickResult)

				ppResult = ImageFunctions.change_image(ppResult,robot_num)
				thickResult = ImageFunctions.change_image(thickResult, robot_num)
			except Exception as e:
				with open(os.path.join(os.getcwd(), 'ThirdLib','alg.log'), 'a+', encoding='utf-8') as ff:
					ff.write(f'{time.strftime("%Y-%m-%d %X", time.localtime())} The error is : {e} \n')

			if ppResult.shape[0] == 0:
				ppResult = pps.reshape(1,-1)
				thickResult = thicks.reshape(1,-1)
				ppResult = ImageFunctions.change_image(ppResult,robot_num)
				thickResult = ImageFunctions.change_image(thickResult, robot_num)
		return ppResult, thickResult

	@staticmethod
	def fillNan(data):
		mask = np.where(~np.isnan(data))
		interp = NearestNDInterpolator(np.transpose(mask), data[mask])
		filled_data = interp(*np.indices(data.shape))
		return filled_data

	@staticmethod
	def ppImage1(dx,dy,cols,xlists,ylists,pps):
		xmax = np.max(xlists)
		ymax = np.max(ylists)
		xmin = np.min(xlists)
		ymin = np.min(ylists)
		x_vec = np.arange(xmin, xmax, dx)
		y_vec = np.arange(ymin, ymax, dy)
		x, y = np.meshgrid(x_vec, y_vec)
		points = np.array(np.vstack((xlists,ylists))).T
		values = np.array(pps)
		readConfig = AlgConfig()
		_,griddata_method = readConfig.choose_pp()
		result = griddata(points, values, (x, y), method=griddata_method)
		if len(result) > 0:
			result = np.array(Image.fromarray(result).resize((cols,result.shape[0])))
			xlist1 = np.abs(xlists - (np.max(xlists) + np.min(xlists))/2)
			index_x,_ = signal.find_peaks(xlist1)
			if len(index_x) > 0:
				index_x = index_x[-1]
				xlists = xlists[index_x:]
				ylists = ylists[index_x:]
				pps = pps[index_x:]
			else:
				result = np.array([])

		return result,xlists,ylists,pps

	@staticmethod
	def T_thick(t, ref, sample, n):
		t_ref = t[np.argmax(ref)]
		t_sample = t[np.argmax(sample)]
		c = 0.3
		d = c * np.abs(t_sample - t_ref) / (n - 1)
		return d

	@staticmethod
	def R_thick(main_peak, main_t, second_peak, second_t, n, theta):
		t_main = main_t[np.argmax(main_peak)]
		t_second = second_t[np.argmax(second_peak)]
		c = 0.3
		theta = np.pi / 180 * theta
		d = c * np.abs(t_second - t_main) * np.cos(theta) / (2 * n)
		return d

	@staticmethod
	def freq_Range(f,xf,size):
		cov = np.ones(size)
		xf1 = np.convolve(xf,cov,'same')/size

		db1 = np.mean(xf1[(f>=8) & (f<=15)])
		db2 = db1 + 3

		f1_start,f1_end = Functions.obtain_fRange(f, xf1, db1)
		f2_start,f2_end = Functions.obtain_fRange(f, xf1, db2)

		return f1_start,f1_end,f2_start,f2_end,db1,db2

	@staticmethod
	def obtain_fRange(f,xf,db):
		start = 0
		xf[0] = -120
		for i in range(len(xf)):
			if xf[i] - db > 0 and start == 0:
				f1 = f[i]
				start = start + 1
			if xf[i] - db < 0 and start == 1:
				if f[i] > 0.2:
					f2 = f[i]
					break
		return f1,f2

	@staticmethod
	def obtain_fGhz(t):
		delta = t[1] - t[0]
		f_Ghz = 1 / delta * 1000
		return f_Ghz

	@staticmethod
	def obtain_tMax(t):
		t_max  = np.max(t)
		return t_max

	@staticmethod
	def obtain_ts(t1,t2,t3,t4,t,thz_signal):
		t1_index = np.argmin(np.abs(t - t1))
		t2_index = np.argmin(np.abs(t - t2))
		t3_index = np.argmin(np.abs(t - t3))
		t4_index = np.argmin(np.abs(t - t4))
		main_peak = thz_signal[t1_index:t2_index]
		second_peak = thz_signal[t3_index:t4_index]
		main_peak = np.power(main_peak, 2)
		second_peak = np.power(second_peak, 2)
		main_t = t[t1_index:t2_index]
		second_t = t[t3_index:t4_index]
		return main_peak, main_t, second_peak, second_t

	@staticmethod
	def obtain_Thzthick(main_peak, main_t, second_peak, second_t, n, theta):
		t_main = main_t[np.argmax(main_peak)]
		t_second = second_t[np.argmax(second_peak)]
		c = 0.3
		theta = np.pi / 180 * theta
		d = c * np.abs(t_second - t_main) * np.cos(theta) / (2 * n)
		return d



class ImageFunctions():

	@staticmethod
	def ImageChoose(ref_path, image_choose, fast_thz_time, M_thz_sig):
		pass

		return M_thz_sig

	@staticmethod
	def New_3DImage(t_THz, M_THz_sig, platform, compress):
		z = int(t_THz / compress)
		x = M_THz_sig[0, :]
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
				if x[data_pv[i + 1]] < x[data_pv[i]] and inverse_y > 0:
					data3d[i, :, :] = np.array(
						Image.fromarray(M_THz_sig[2:, data_pv[i]:data_pv[i + 1]][:, ::-1]).resize((col_num, z)))
				elif x[data_pv[i + 1]] < x[data_pv[i]] and inverse_y < 0:
					data3d[i, :, :] = np.array(
						Image.fromarray(M_THz_sig[2:, data_pv[i]:data_pv[i + 1]][::-1, ::-1]).resize((col_num, z)))
				elif x[data_pv[i + 1]] > x[data_pv[i]] and inverse_y < 0:
					data3d[i, :, :] = np.array(
						Image.fromarray(M_THz_sig[2:, data_pv[i]:data_pv[i + 1]][::-1, :]).resize((col_num, z)))
				else:
					data3d[i, :, :] = np.array(
						Image.fromarray(M_THz_sig[2:, data_pv[i]:data_pv[i + 1]]).resize((col_num, z)))
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

	@staticmethod
	def Robot3DImage(M_THz_sig, compress, row_num):
		if M_THz_sig.shape[1] <= row_num:
			return np.array([])
		else:
			num1 = int(np.floor(M_THz_sig.shape[1] / row_num))
			data3d = np.zeros((int(row_num),int(M_THz_sig.shape[0]/compress),num1))
			for i in range(num1):
				if i % 2 == 0:
					data3d[:,:,i] = np.array(
					Image.fromarray(M_THz_sig[:,i*row_num:(i+1)*row_num].T).resize((int(M_THz_sig.shape[0]/compress), num1)))
				else:
					data3d[:,:,i] = np.fliplr(np.array(
					Image.fromarray(M_THz_sig[:,i*row_num:(i+1)*row_num].T).resize((int(M_THz_sig.shape[0]/compress), num1))))

		return data3d


	@staticmethod
	def xyThzsgl(x_pos, y_pos, mThz,fast_thz_time):
		if mThz.shape[0] < 1:
			return np.array([])
		orgxy = mThz[0:2, :].copy()
		t_max = np.max(fast_thz_time)

		x_pos1 = x_pos + min(orgxy[0, :])
		y_pos1 = y_pos + min(orgxy[1, :])
		sum_xy = np.abs(orgxy[0, 0]) - x_pos1 + np.abs(orgxy[1, 0] - y_pos1)
		index = 0
		for i in range(1, orgxy.shape[1]):
			if sum_xy > np.abs(orgxy[0, i] - x_pos1) + np.abs(orgxy[1, i] - y_pos1):
				sum_xy = np.abs(orgxy[0, i] - x_pos1) + np.abs(orgxy[1, i] - y_pos1)
				index = i
		sigThzxy = mThz[2:, index].T.copy()
		fast_thz_time = np.linspace(0,t_max,len(sigThzxy))
		return fast_thz_time,sigThzxy

	@staticmethod
	def removeNoise(x):
		t = np.arange(len(x))
		params = np.polyfit(t, x, 1)
		noise = np.polyval(params, t)
		denoised = np.array(x) - np.array(noise)
		return denoised

	@staticmethod
	def obtain_alpha(c, max_range, mode):
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

	@staticmethod
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
			return ndimage.rotate(data, 90)
		elif num == 5:
			return np.fliplr(ndimage.rotate(data, 90))
		elif num == 6:
			return np.flipud(ndimage.rotate(data, 90))
		elif num == 7:
			return ndimage.rotate(data, 270)
		elif num == 8:
			return np.fliplr(ndimage.rotate(data, 270))
		elif num == 9:
			return np.flipud(ndimage.rotate(data, 270))
		else:
			return data

	@staticmethod
	def change_image(data,num):
		if num == 0:
			return data
		elif num == 1:
			return np.fliplr(data)
		elif num == 2:
			return np.flipud(data)
		elif num == 3:
			return np.fliplr(np.flipud(data))
		elif num == 4:
			return ndimage.rotate(data, 90)
		elif num == 5:
			return np.fliplr(ndimage.rotate(data, 90))
		elif num == 6:
			return np.flipud(ndimage.rotate(data, 90))
		elif num == 7:
			return ndimage.rotate(data, 270)
		elif num == 8:
			return np.fliplr(ndimage.rotate(data, 270))
		elif num == 9:
			return np.flipud(ndimage.rotate(data, 270))
		else:
			return data

	@staticmethod
	def convertData(xList, yList, timeSeriesList, unpack_params):
		x = unpack_params[0]
		dx = unpack_params[1]
		x_max = unpack_params[2]
		y = unpack_params[3]
		y_max = unpack_params[5]
		delete_d = unpack_params[6]
		data = np.array(timeSeriesList)
		M_thz_sig = np.vstack((xList, yList))

		M_thz_sig = np.vstack((M_thz_sig, data))
		M_thz_sig = ImageFunctions.cut_Data(M_thz_sig, xList, yList, dx, x_max, x, y_max, y, delete_d)
		return M_thz_sig

	@staticmethod
	def cut_Data(M_thz_sig, xList, yList, dx, x_max, x_min, y_max, y_min, delete_d):
		xlist = np.array(xList)
		ylist = np.array(yList)
		xlist_diff = np.diff(xlist)
		delete_d0 = np.array(np.where(np.abs(xlist_diff) < delete_d * dx))
		delete_d1 = np.array(np.where(np.abs(xlist_diff) > 4 * dx))
		delete_x = np.append(delete_d0, delete_d1)
		delete_x = np.unique(delete_x)
		with open(os.path.join(os.getcwd(), 'ThirdLib', 'alg.log'), 'a+', encoding='utf-8') as ff:
			ff.write(f'{time.strftime("%Y-%m-%d %X", time.localtime())} 3D Image total x cord: {len(xlist)} points! \n')
			ff.write(
				f'{time.strftime("%Y-%m-%d %X", time.localtime())} 3D Image delete x cord: {len(delete_x)} points! \n')
			ff.write(
				f'{time.strftime("%Y-%m-%d %X", time.localtime())} 3D Image input x cord range is : {x_min} - {x_max} \n')
			ff.write(
				f'{time.strftime("%Y-%m-%d %X", time.localtime())} 3D Image solve x cord range is : {np.min(xlist)} - {np.max(xlist)} \n')
			ff.write(
				f'{time.strftime("%Y-%m-%d %X", time.localtime())} 3D Image input y cord range is : {y_min} - {y_max} \n')
			ff.write(
				f'{time.strftime("%Y-%m-%d %X", time.localtime())} 3D Image solve y cord range is : {np.min(ylist)} - {np.max(ylist)} \n')

		delete_x = delete_x.reshape(-1, )
		M_thz_sig = np.delete(M_thz_sig, delete_x, 1)
		return M_thz_sig

	@staticmethod
	def image_filter(M_thz_sig, param1):
		if param1 == 1:
			for i in range(M_thz_sig.shape[1]):
				filter1 = signal.medfilt(M_thz_sig[2:, i], 13)
				n = int(150 / 1)
				baseline = (np.convolve(filter1, np.ones((n,)) / n, mode="same"))
				data1 = filter1 - baseline
				M_thz_sig[2:, i] = data1
		return M_thz_sig

	@staticmethod
	def robotPPThick(signals, row_num):
		if signals.shape[1] <= row_num:
			return np.array([]), np.array([])
		else:
			num1 = int(np.floor(signals.shape[1] / row_num))
			ppResult = np.zeros((num1, row_num))
			thickResult = np.zeros((num1, row_num))
			pps = signals[3, :]
			thicks = signals[4, :]
			for i in range(num1):
				if i % 2 == 0:
					ppResult[i, :] = pps[i * row_num:(i + 1) * row_num]
					thickResult[i, :] = thicks[i * row_num:(i + 1) * row_num]
				else:
					ppResult[i, :] = pps[i * row_num:(i + 1) * row_num][::-1]
					thickResult[i, :] = thicks[i * row_num:(i + 1) * row_num][::-1]
		return ppResult, thickResult

