# -*- coding: utf-8 -*-
"""
@Create Time: 2022/2/16 9:08
@Author: Kevin
@Python Version：3.7.6
"""
import os
import time
import numpy as np
import yaml
#获取算法配置文件的参数和参数初始化,与C#版本的配置文件一样
class AlgConfig():
    def __init__(self):
        self.pp_method = 1
        self.open_mean = 0
        self.griddata_method = 'nearest'
        self.align = 0
        self.thz_max = 6
        self.sg = 0
        self.medianf = 0
        self.filter_name = 'none'
        self.lowpass = 0.8
        self.highpass = 0.006
        self.dwt = 0
        self.wave_name = 'db13'
        self.align_signal = 0
        self.xy, self.xz, self.yz = 1, 2, 2
        self.delete_d = 0.1
        self.min_threshold ,self.max_threshold,self.use_threshold = -1000000,1000000,0
        self.platform = 1
        self.precision = 2
        self.delay_line = 2
        self.delay_length = 0.5
        self.shine_length = 6
        self.pp_image = 0
        self.if_moveAverage = 0
        self.config_path = os.path.join(os.getcwd(), 'ThirdLib', 'Algconfig.yaml')

    def read_moveAverage(self):

        if not os.path.exists(self.config_path):
            raise Exception("Can't find alg Algconfig.yaml!")
        with open(self.config_path, 'r', encoding='utf-8') as f:
            data = yaml.load(f,Loader=yaml.FullLoader)
        try:
            if 'Signal_configs' in data.keys():
                self.if_moveAverage = int(data['Signal_configs']['if_moveAverage'])
                if self.if_moveAverage < 0 :
                    self.if_moveAverage = 0

        except Exception as e:
            with open(os.path.join(os.getcwd(), 'ThirdLib', 'alg.log'), 'a+', encoding='utf-8') as ff:
                ff.write(
                    f'{time.strftime("%Y-%m-%d %X", time.localtime())} Error is  {e} \n')
        return self.if_moveAverage

    def choose_pp(self):

        if not os.path.exists(self.config_path):
            raise Exception("Can't find alg Algconfig.yaml!")
        with open(self.config_path, 'r', encoding='utf-8') as f:
            data = yaml.load(f,Loader=yaml.FullLoader)
        try:
            if 'Signal_configs' in data.keys():
                self.pp_method = data['Signal_configs']['pp_method']
            if 'Signal_configs' in data.keys():
                self.griddata_method = data['Signal_configs']['griddata_method']
        except Exception as e:
            with open(os.path.join(os.getcwd(), 'ThirdLib', 'alg.log'), 'a+', encoding='utf-8') as ff:
                ff.write(
                    f'{time.strftime("%Y-%m-%d %X", time.localtime())} Error is  {e} \n')

        return self.pp_method,self.griddata_method

    def image_change(self):
        if not os.path.exists(self.config_path):
            raise Exception("Can't find alg Algconfig.yaml!")
        with open(self.config_path, 'r', encoding='utf-8') as f:
            data = yaml.load(f,Loader=yaml.FullLoader)
        try:
            if 'Imaging_configs' in data.keys():
                self.pp_image = data['Imaging_configs']['pp_image']
                if self.pp_image not in np.arange(10):
                    self.pp_image = 0
        except Exception as e:
            with open(os.path.join(os.getcwd(), 'ThirdLib', 'alg.log'), 'a+', encoding='utf-8') as ff:
                ff.write(
                    f'{time.strftime("%Y-%m-%d %X", time.localtime())} Error is  {e} \n')

        return self.pp_image

    def read_align(self):

        if not os.path.exists(self.config_path):
            raise Exception("Can't find alg Algconfig.yaml!")

        with open(self.config_path, 'r', encoding='utf-8') as f:
            data = yaml.load(f,Loader=yaml.FullLoader)

        try:
            if 'Signal_configs' in data.keys():
                self.align = data['Signal_configs']['align']
        except Exception as e:
            with open(os.path.join(os.getcwd(), 'ThirdLib', 'alg.log'), 'a+', encoding='utf-8') as ff:
                ff.write(
                    f'{time.strftime("%Y-%m-%d %X", time.localtime())} Error is {e} \n')

        with open(os.path.join(os.getcwd(), 'ThirdLib' , 'alg.log'), 'a+', encoding='utf-8') as ff:
            ff.write(
                f'{time.strftime("%Y-%m-%d %X", time.localtime())} Alg whether read align signal choose {self.align} \n')
        return self.align

    def getParams(self):
        if not os.path.exists(self.config_path):
            raise Exception("Can't find alg Algconfig.yaml!")

        with open(self.config_path, 'r', encoding='utf-8') as f:
            data = yaml.load(f,Loader=yaml.FullLoader)
            self.sg = data['Signal_configs']['SG']
            self.dwt = data['Signal_configs']['dwt']
            self.medianf = data['Signal_configs']['medianf']
            self.filter_name = data['Signal_configs']['filter_name']
            self.dwt_name = data['Signal_configs']['wave_name']
            self.lowpass = data['Signal_configs']['lowpass_value']
            self.highpass = data['Signal_configs']['highpass_value']

        return self.sg, self.medianf, self.dwt, self.dwt_name, self.filter_name, self.lowpass, self.highpass

    def getParamsF(self):
        if not os.path.exists(self.config_path):
            raise Exception("Can't find alg Algconfig.yaml!")
        with open(self.config_path, 'r', encoding='utf-8') as f:
            data = yaml.load(f,Loader=yaml.FullLoader)
            self.platform = data['System_configs']['platform']
            self.precision = data['System_configs']['precision']
            self.delete_d = data['System_configs']['delete_d']

        params = [self.platform, self.precision, self.delete_d]
        return params

    def if_open_mean(self):
        if not os.path.exists(self.config_path):
            raise Exception("Can't find alg Algconfig.yaml!")
        with open(self.config_path, 'r', encoding='utf-8') as f:
            data = yaml.load(f,Loader=yaml.FullLoader)
        try:
            if 'Signal_configs' in data.keys():
                self.open_mean = data['Signal_configs']['open_mean']
        except Exception as e:
            with open(os.path.join(os.getcwd(), 'ThirdLib', 'alg.log'), 'a+', encoding='utf-8') as ff:
                ff.write(
                    f'{time.strftime("%Y-%m-%d %X", time.localtime())} Error is {e} \n')
        return self.open_mean


class ImageConfig():
    color_path = os.path.join(os.getcwd(),'ThirdLib','color')
    def init(self):
        self.THzsig_intp = np.array([])
        self.w ,self.h = 1530,850
        self.x_min ,self.y_min,self.z_min = 1 ,1 ,1
        self.dx ,self.dy,self.dz= 1,1,1
        self.shapex,self.shapey ,self.shapez = 100,100,100
        self.fast_thz_time,self.M_thz_sig = np.array([]),np.array([])
        self.config_path =os.path.join(os.getcwd(),'ThirdLib','Algconfig.yaml')
        self.log_path = os.path.join(os.getcwd(),'ThirdLib','alg.log')
        self.xy,self.xz,self.yz = 0,0,0
        self.platform = 1
        self.precision = 1
        self.delay_line = 2
        self.max_range = 1000
        self.mode = 'gray'
        self.compress = 2
        self.medianfilter,self.medianfilternum = 0,15
        self.min_threshold ,self.max_threshold,self.use_threshold = -1000000,1000000,0
        self.cutxyzlineEdit = ''
        self.use_mayavi = 1
        self.use_qda = 0
        self.qda_path = ''
        self.use_align = 0
        self.roll_delay = 0
        self.image_choose = 0
        self.image_filter = 0
        self.ref_path = ''
        self.delay_length = 0.5
        self.shine_length = 6
        self.delete_d = 0.5
        self.robot_xyz = ''
        self.robot_delete = 1

    def updateParams(self):
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = yaml.load(f,Loader=yaml.FullLoader)
                    self.xy = data['Imaging_configs']['xy']
                    self.xz = data['Imaging_configs']['xz']
                    self.yz = data['Imaging_configs']['yz']
                    self.platform = data['System_configs']['platform']
                    self.precision = data['System_configs']['precision']
                    self.delay_line = data['System_configs']['delay_line']
                    self.min_threshold = data['Imaging_configs']['min_threshold']
                    self.max_threshold = data['Imaging_configs']['max_threshold']
                    self.use_threshold = data['Imaging_configs']['use_threshold']
                    self.robot_xyz = data['Imaging_configs']['robot_xyz']
                    self.robot_delete = data['Imaging_configs']['robot_delete']
                    self.delay_length = data['System_configs']['delay_length']
                    self.shine_length = data['System_configs']['shine_length']
                    self.delete_d = data['Imaging_configs']['delete_d']

        except Exception as e:
            with open(self.log_path, 'a+', encoding='utf-8') as ff:
                ff.write(str(time.strftime("%Y-%m-%d %X", time.localtime())) + "3D Image 参数配置失败！" + '\n')
                ff.write(str(time.strftime("%Y-%m-%d %X", time.localtime())) + str(e))
