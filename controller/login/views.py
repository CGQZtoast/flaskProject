# -*- coding = utf-8 -*-
# @Time : 2022/11/11 20:27
# @Author : 乌贼
# @File : views.py
# @Software : PyCharm


from flask import request, jsonify
from flask import Blueprint

# from login import login_blue
from entity.admins import *
from methods.token import *


login_blue = Blueprint('login', __name__, url_prefix='/')


@login_blue.route('/login', methods=['POST'])
def login():
    # 返回数据
    return_dict = {
        'code': 500,
        'data': {}
    }

    # 获取数据
    data = request.get_json()
    user_account = data['userAccount']
    user_password = data['userPassword']
    print('[post]/login,收到的数据为：', data)

    # 创建管理员对象
    administrator = Admins(user_account, user_password)

    try:
        # 验证账号密码
        if administrator.verify():  # 验证通过
            print('验证通过')
            administrator.set_info()  # 设置管理员信息

            return_dict['code'] = 200

            # 设置cookie
            generate_token(administrator.get_id(), administrator.get_account())
            validate_token()

        else:  # 账号或密码错误
            print('账号或密码错误')
            return_dict['code'] = 401
    except Exception as e:
        print('/login error: ', e)
        return_dict = {
            'code': 500,
            'msg': e
        }

    return jsonify(return_dict)
