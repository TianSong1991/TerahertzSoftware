#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import time
import threading
from datetime import datetime

from Entity.models import User, Role, SysLog


def init():
    global sys_map
    global exit_event
    global appMainWnd
    sys_map = {}
    appMainWnd = None
    exit_event = threading.Event()
    exit_event.set()


def release():
    del exit_event


def waitOne(cost):
    if exit_event is None:
        print('You may call init first!')
        return False
    return exit_event.wait(cost / 1000.0)


def waitTime(cost):
    time.sleep(cost / 1000.0)


def set():
    exit_event.set()


def reset():
    exit_event.clear()


def toHex(data, length=2):
    data = hex(int(data))
    data = data[2:]
    if len(data) > length * 2:
        data = data[-4:]
    if len(data) < 2 * length:
        for i in range(2 * length - len(data)):
            data = '0' + data
    result = ''
    for i in range(length):
        result = result + data[i * 2:i * 2 + 2] + ' '
    return result[:-1]


def isStrNoneOrEmpty(_str):
    return _str is None or bool(_str.strip()) is False


def isFileExist(file):
    return os.path.exists(file)


# 获取用户权限 key:功能名称 如 光谱扫描 成像光谱 等
def GetUserRightInfo(Id, key):
    user = User.select().where(User.Id == Id)
    if len(user) > 0:
        r = Role.select().where(Role.Id == user.RoleId)
        if len(r) > 0:
            r = json.loads(r[0].Rights)
            item = r.get(key)
            if item is not None:
                if item.isChecked > 0:
                    return 1
                else:
                    return 0
    return 0


def Debug(LogType, Id, Content):
    SysLog.create(Type=LogType, UserId=Id, Context=Content, Level=LOG_DEBUG,
                  AddDate=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))


def ERROR(LogType, Id, Content):
    SysLog.create(Type=LogType, UserId=Id, Context=Content, Level=LOG_ERROR,
                  AddDate=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))


def INFO(LogType, Id, Content):
    SysLog.create(Type=LogType, UserId=Id, Context=Content, Level=LOG_ERROR,
                  AddDate=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))


FAILED = 0
SUCCESS = 1
MANUAL_EXIT = 2
NOT_READY_READ = 3
ERR_USB_OPEN = 4
ERR_USB_READ_WRITE = 5
ERR_READY_READ = 6
ERR_LASER_ON = 7
ERR_LASER_LOCK = 8
ERR_LASER_OFF = 9
ERR_BAISSRC_ON = 10
ERR_BAISSRC_OFF = 11
ERR_YINQ_CONFIG = 12
ERR_YINQ_OPEN = 13
ERR_YINQ_OFF = 14
ERR_YINQ_ZERO = 15
ERR_COM_OPEN = 16
ERR_COM_DLY = 17
ERR_COM_LBA = 18
ERR_MOTOR_DEVICE = 10
ERR_MOTOR_OPEN = 20
ERR_MOTOR_INITPOS = 21
ERR_DELAYLINE_RESET = 22
ERR_AMPLIFIER_DATA = 23
ERR_AMPLIFIER_MAGNIFY = 24
ERR_AMPLIFIER_PHASE_SET = 25

NONE = 100
OFF = 101
ON = 102
WORKING = 103
STARTING = 104

LOG_DEBUG = 1000
LOG_INFO = 1001
LOG_ERROR = 1002
