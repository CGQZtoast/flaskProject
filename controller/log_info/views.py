# -*- coding = utf-8 -*-
# @Time : 2022/12/5 13:27
# @Author : 乌贼
# @File : views.py
# @Software : PyCharm

from flask import Blueprint, jsonify, request

from entity.log import *
from methods.token import *
from utils.api_result import ApiResult

log_blue = Blueprint('log', __name__, url_prefix='/')


@log_blue.route('/getLoginLog', methods=['GET'])
def login_log():
    result = ApiResult()
    # 验证token
    if validate_token():
        log_manege = LogManege()
        msg = log_manege.get_login_log()
        data = {'LoginLogData': msg}
        return_dict = result.success(data)
    else:
        return_dict = result.error()

    return jsonify(return_dict)


@log_blue.route('/getErrorLog', methods=['GET'])
def error_log():
    result = ApiResult()
    # 验证token
    if validate_token():
        log_manege = LogManege()
        msg = log_manege.get_error_log()
        data = {'errorData': msg}
        return_dict = result.success(data)
    else:
        return_dict = result.error()
    return jsonify(return_dict)


@log_blue.route('/delLoginLog', methods=['POST'])
def delete_login_log():
    result = ApiResult()
    # 获取数据
    data = request.get_json()

    print('[post]/delLoginLog,收到的数据为：', data)
    ids = data['id']
    # 验证token
    if validate_token():
        log_manege = LogManege()
        if log_manege.delete_login_logs(ids):
            return_dict = result.success()
        else:
            return_dict = result.error('删除登录日志失败')
    else:
        return_dict = result.error()

    return jsonify(return_dict)


@log_blue.route('/delErrorLog', methods=['POST'])
def delete_error_log():
    result = ApiResult()
    # 获取数据
    data = request.get_json()
    ids = data['id']
    print('[post]/delErrorLog,收到的数据为：', data)

    # 验证token
    if validate_token():
        log_manege = LogManege()
        if log_manege.delete_error_logs(ids):
            return_dict = result.success()
        else:
            return_dict = result.error('删除错误日志失败')
    else:
        return_dict = result.error()

    return jsonify(return_dict)

