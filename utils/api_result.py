# -*- coding = utf-8 -*-
# @Time : 2023/1/2 14:58
# @Author : 乌贼
# @File : api_result.py
# @Software : PyCharm

from utils.status_code_constant import *


class ApiResult(object):
    __code = 200
    __data = ''
    __error_msg = ''

    def __init__(self):
        pass

    def get_result(self):
        if self.__code == 200:
            if self.__data != '':
                return {'code': self.__code, 'data': self.__data}
            else:
                return {'code': self.__code}
        else:
            return {'code': self.__code, 'msg': self.__error_msg}

    def success(self, data=None):
        self.__code = STATUS_200
        if data is not None:
            self.__data = data
        return self.get_result()

    def error(self, error_msg=None, code=None):
        self.__code = STATUS_500
        if error_msg is not None:
            self.__error_msg = error_msg
        else:
            self.__error_msg = 'token验证失败'
        return self.get_result()

    def error_401(self, error_msg=None):
        self.__code = STATUS_401
        if error_msg is not None:
            self.__error_msg = error_msg
        else:
            self.__error_msg = '账号或密码错误'
        return self.get_result()


