#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtCore import QIODevice, QByteArray
from PyQt5.QtSerialPort import QSerialPortInfo, QSerialPort
from PyQt5.QtWidgets import QWidget
import time
import binascii
import serial
import serial.tools.list_ports

class ComHelper(QWidget):
    def __init__(self, name, parent=None):
        super(ComHelper, self).__init__(parent)
        self.devName = name
        self.serial = QSerialPort(self)  # 用于连接串口的对象
        # self._serial.readyRead.connect(self.onReadyRead)  # 绑定数据读取信号

    def open(self, name=None, baudRate=9600, timeOut=500):
        if name is None:
            return False
        elif self.serial.isOpen():
            return True
        else:
            if self.devName == "Motor":
                find=False
                for port in serial.tools.list_ports.comports():
                    try:
                        serialport = serial.Serial()

                        serialport.port = port.device
                        print(port.device)
                        serialport.baudrate = baudRate
                        serialport.parity = 'N'
                        serialport.bytesize = 8
                        serialport.stopbits = 1
                        serialport.timeout = 0.5
                        serialport.open()
                        serialport.read(50)
                        cmd = '96 41 01 01 55 aa 0d 0a'
                        bys = bytes.fromhex(cmd)
                        serialport.write(bys)
                        time.sleep(0.2)
                        result = serialport.read(10)
                        if len(result) <= 0:
                            serialport.write(bys)
                            time.sleep(0.2)
                            result = serialport.read(10)
                        if len(result) > 0 and result[0] == 0x96:
                            find = True
                            self.serial = serialport
                    except Exception as err:
                        pass
                return find
            self.serial.setPortName(name)
            self.serial.setBaudRate(baudRate)
            self.serial.setParity(QSerialPort.NoParity)
            self.serial.setDataBits(QSerialPort.Data8)
            self.serial.setStopBits(QSerialPort.OneStop)
            self.serial.setReadBufferSize(512)
            self._serial.setFlowControl(QSerialPort.NoFlowControl)
            return self._serial.open(QIODevice.ReadWrite)  # 读写方式打开串口

    def close(self):
        if self.serial.isOpen():
            self.serial.close()

    def isEnable(self):
        return self.serial.isOpen()

    def writeData(self, buff, wLen, wait_time=0.02):
        try:
            time.sleep(wait_time)
            self.serial.clear(QSerialPort.AllDirections)
            self.serial.writeData(buff, wLen)
            return True
        except:
            print(f"{self.devName}写串口命令：{buff}失败！")
            return False

    def readData(self, buff, rLen, wait_time=500):
        try:
            if self.serial.waitForReadyRead(wait_time):
                time.sleep(0.02)
                len = self.serial.readData(buff, rLen)
                rLen = len
                return True
            else:
                rLen = 0
                return False
        except:
            print(f"{self.devName}读串口命令：{buff}失败！")
            rLen = 0
            return False

    def writeDataReturn(self, buff, wLen, rLen, wait_time=0.005):
        if self.writeData(buff, wLen, wait_time):
            return self.readData(buff, rLen)
        else:
            return False

    def writeStrReturn(self, strCmd, buff, isReturn=False):
        try:
            self.serial.clear(QSerialPort.AllDirections)
            text = QByteArray(strCmd.encode('gb2312'))  # emmm windows 测试的工具貌似是这个编码
            self.serial.write(text)
            if isReturn:
                time.sleep(0.02)
                buff += self.serial.readAll().data()
                return True
            else:
                buff.extend(['0', 'K'])
                return True
        except:
            print(f"{self.devName}写串口命令：{strCmd}失败！")
            return False

    def writeReturn(self, cmd, rLen=20, wait_time=0.1, isLog=True):
        bys = bytes.fromhex(cmd)
        self.serial.write(bys)
        time.sleep(wait_time)
        if rLen == 0:
            result = b''
        else:
            result = self.serial.read(rLen)
        # if isLog:
        #     print(round(time.time() % 10, 3), 'write:', cmd, 'return:', str(binascii.b2a_hex(result)).upper())
        return result

    @staticmethod
    def getInfoByName(name):
        arr = QSerialPortInfo.availablePorts()
        for item in arr:
            if item.portName() == name:
                return item
        return None
