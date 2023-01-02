# -*- coding = utf-8 -*-
# @Time : 2022/12/5 9:00
# @Author : 乌贼
# @File : views.py
# @Software : PyCharm

from flask import request, jsonify
from flask import Blueprint

from entity.user import *
from methods.token import *

statistical_blue = Blueprint('statistical', __name__, url_prefix='/')


@statistical_blue.route('/userTrend', methods=['GET'])
def user_trend():
    # 返回数据
    return_dict = {
        "code": 500,
        "data": {}
    }

    # 获取数据
    total_user_time_slot = request.args.get('totalUserTimeSlot')
    increased_user_time_slot = request.args.get('increasedUserTimeSlot')

    print('[GET]/userTrend,收到的数据为：', total_user_time_slot + ' ' + increased_user_time_slot)

    # 验证token
    if validate_token():
        # 创建用户管理对象
        user_manege = UserManege()
        if user_manege.count_statistics(total_user_time_slot, increased_user_time_slot):
            return_dict['code'] = 200
            # 获取总人数
            return_dict['data']['totalUserDateList'] = user_manege.get_total_user_date_list()
            return_dict['data']['totalUser'] = user_manege.get_total_user()

            # 获取新增人数
            return_dict['data']['increasedUserDateList'] = user_manege.get_increased_user_date_list()
            return_dict['data']['increasedUser'] = user_manege.get_increased_user()
        else:
            return_dict = {
                'code': 500,
                'msg': '统计出错'
            }
    else:
        return_dict = {
            'code': 500,
            'msg': 'token验证失败'
        }

    return jsonify(return_dict)


@statistical_blue.route('/userMsg', methods=['GET'])
def user_msg():
    # 返回数据
    return_dict = {
        "code": 500,
        "data": {}
    }
    # 验证token
    if validate_token():
        user_manege = UserManege()
        if user_manege.distribution_statistics():
            return_dict['code'] = 200
            return_dict['data']['ageData'] = user_manege.get_age_distribution()
            return_dict['data']['sexData'] = user_manege.get_gender_distribution()
            return_dict['data']['areaData'] = user_manege.get_provinces_distribution()
        else:
            return_dict = {
                'code': 500,
                'msg': '统计出错'
            }
    else:
        return_dict = {
            'code': 500,
            'msg': 'token验证失败'
        }

    return jsonify(return_dict)
