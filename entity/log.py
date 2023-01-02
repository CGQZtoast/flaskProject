# -*- coding = utf-8 -*-
# @Time : 2022/11/29 20:01
# @Author : 乌贼
# @File : log.py
# @Software : PyCharm

import datetime

from database.models import *


class LoginLog(object):
    __id = 0  # 登录日志id
    __phone = ''  # 用户手机号
    __time = datetime.date(2022, 1, 1)  # 登录时间
    __longitude_and_latitude = ''  # 经纬度
    __device = ''  # 登录设备

    def __init__(self, id, phone, time, address, device):
        self.__id = id
        self.__phone = phone
        self.__time = time
        self.__longitude_and_latitude = address
        self.__device = device

    def get_dict(self):
        login_log = {'id': self.__id, 'phone': self.__phone, 'time': str(self.__time), 'address': self.__longitude_and_latitude, 'loginDevice': self.__device}
        return login_log


class ErrorLog(object):
    __id = 0  # 错误日志id
    __time = datetime.date(2022, 1, 1)  # 时间
    __info = ''  # 错误信息

    def __init__(self, id, time, info):
        self.__id = id
        self.__time = time
        self.__info = info

    def get_dict(self):
        error_log = {'id': self.__id, 'errorMsg': self.__info, 'time': str(self.__time)}
        return error_log


class LogManege(object):
    __login_logs = []
    __error_logs = []

    def get_login_log(self):
        msgs = db.session.query(
            log_login.id,
            user.phone,
            log_login.time,
            log_login.address,
            log_login.device
        ).filter(
            log_login.user_id == user.id
        ).all()

        self.__login_logs = []

        for msg in msgs:
            login_log = LoginLog(msg.id, msg.phone, msg.time, msg.address, msg.device)
            self.__login_logs.append(login_log.get_dict())

        return self.__login_logs

    def get_error_log(self):
        msgs = log_error.query.filter().all()

        self.__error_logs = []

        for msg in msgs:
            error_log = ErrorLog(msg.id, msg.time, msg.info)
            self.__error_logs.append(error_log.get_dict())

        return self.__error_logs

    def delete_login_logs(self, ids):
        try:
            for id in ids:
                log_login.query.filter(log_login.id == id).delete()
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def delete_error_logs(self, ids):
        try:
            for id in ids:
                log_error.query.filter(log_error.id == id).delete()
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
