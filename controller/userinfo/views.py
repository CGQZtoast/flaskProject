# -*- coding = utf-8 -*-
# @Time : 2022/12/5 9:11
# @Author : 乌贼
# @File : views.py
# @Software : PyCharm

from flask import Blueprint, jsonify, request

from entity.user import UserManege
from methods.token import validate_token

userinfo_blue = Blueprint('userinfo', __name__, url_prefix='/')


@userinfo_blue.route('/showUserMsg', methods=['GET'])
def show_user_msg():
    # 返回数据
    return_dict = {
        "code": 500,
        "data": {}
    }
    # 验证token
    if validate_token():
        user_manege = UserManege()
        if user_manege.get_all_user_information():
            return_dict['code'] = 200
            return_dict['data']['userMsg'] = user_manege.get_user_msg()
        else:
            return_dict = {
                'code': 500,
                'msg': '获取用户信息失败'
            }
    else:
        return_dict = {
            'code': 500,
            'msg': 'token验证失败'
        }

    return jsonify(return_dict)


@userinfo_blue.route('/editUser', methods=['POST'])
def edit_user():
    # 返回数据
    return_dict = {
        'code': 500
    }

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
            return_dict['code'] = 200
        else:
            return_dict['code'] = 500
            return_dict['msg'] = '修改失败'
    else:
        return_dict['code'] = 500
        return_dict['msg'] = 'token验证失败'

    return jsonify(return_dict)


@userinfo_blue.route('/delUser', methods=['POST'])
def del_user():
    # 返回数据
    return_dict = {
        "code": 500,
    }
    # 获取数据
    data = request.get_json()
    ids = data['id']
    print('[post]/delUser,收到的数据为：', data)

    # 验证token
    if validate_token():
        user_manege = UserManege()
        if user_manege.delete_user(ids):
            return_dict['code'] = 200
        else:
            return_dict['code'] = 500
            return_dict['msg'] = '删除失败'
    else:
        return_dict['code'] = 500
        return_dict['msg'] = 'token验证错误'

    return jsonify(return_dict)

