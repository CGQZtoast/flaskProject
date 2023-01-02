# -*- coding = utf-8 -*-
# @Time : 2022/12/5 9:11
# @Author : 乌贼
# @File : views.py
# @Software : PyCharm

from flask import Blueprint, jsonify, request

from entity.user import UserManege
from methods.token import validate_token
from utils.api_result import ApiResult

userinfo_blue = Blueprint('userinfo', __name__, url_prefix='/')


@userinfo_blue.route('/showUserMsg', methods=['GET'])
def show_user_msg():
    result = ApiResult()
    # 验证token
    if validate_token():
        user_manege = UserManege()
        if user_manege.get_all_user_information():
            data = {'userMsg': user_manege.get_user_msg()}
            return_dict = result.success(data)
        else:
            return_dict = result.error('获取用户信息失败')
    else:
        return_dict = result.error()

    return jsonify(return_dict)


@userinfo_blue.route('/editUser', methods=['POST'])
def edit_user():
    result = ApiResult()

    # 获取数据
    data = request.get_json()
    id = data['id']
    phone = data['phone']
    sex = data['sex']
    DOB = data['birth']
    region = data['region']
    show_region = data['showRegion']
    print('[post]/editUser,收到的数据为：', data)

    # 验证token
    if validate_token():
        user_manege = UserManege()
        if user_manege.edit_user_info(id, phone, sex, DOB, region):
            return_dict = result.success()
        else:
            return_dict = result.error('修改失败')
    else:
        return_dict = result.error()

    return jsonify(return_dict)


@userinfo_blue.route('/delUser', methods=['POST'])
def del_user():
    result = ApiResult()
    # 获取数据
    data = request.get_json()
    ids = data['id']
    print('[post]/delUser,收到的数据为：', data)

    # 验证token
    if validate_token():
        user_manege = UserManege()
        if user_manege.delete_user(ids):
            return_dict = result.success()
        else:
            return_dict = result.error('删除失败')
    else:
        return_dict = result.error()

    return jsonify(return_dict)

