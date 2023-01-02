# -*- coding = utf-8 -*-
# @Time : 2022/12/5 9:00
# @Author : 乌贼
# @File : views.py
# @Software : PyCharm

from flask import request, jsonify
from flask import Blueprint

from entity.user import *
from methods.token import *
from utils.api_result import ApiResult

statistical_blue = Blueprint('statistical', __name__, url_prefix='/')


@statistical_blue.route('/userTrend', methods=['GET'])
def user_trend():
    result = ApiResult()

    # 获取数据
    total_user_time_slot = request.args.get('totalUserTimeSlot')
    increased_user_time_slot = request.args.get('increasedUserTimeSlot')

    print('[GET]/userTrend,收到的数据为：', total_user_time_slot + ' ' + increased_user_time_slot)

    # 验证token
    if validate_token():
        # 创建用户管理对象
        user_manege = UserManege()
        if user_manege.count_statistics(total_user_time_slot, increased_user_time_slot):
            data = {}
            # 获取总人数
            data['totalUserDateList'] = user_manege.get_total_user_date_list()
            data['totalUser'] = user_manege.get_total_user()

            # 获取新增人数
            data['increasedUserDateList'] = user_manege.get_increased_user_date_list()
            data['increasedUser'] = user_manege.get_increased_user()

            return_dict = result.success(data)
        else:
            return_dict = result.error('统计出错')
    else:
        return_dict = result.error()

    return jsonify(return_dict)


@statistical_blue.route('/userMsg', methods=['GET'])
def user_msg():
    result = ApiResult()
    # 验证token
    if validate_token():
        user_manege = UserManege()
        if user_manege.distribution_statistics():
            data = {}
            data['ageData'] = user_manege.get_age_distribution()
            data['sexData'] = user_manege.get_gender_distribution()
            data['areaData'] = user_manege.get_provinces_distribution()
            return_dict = result.success(data)
        else:
            return_dict = result.error('统计出错')
    else:
        return_dict = result.error()

    return jsonify(return_dict)
