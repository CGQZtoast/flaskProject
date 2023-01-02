# -*- coding = utf-8 -*-
# @Time : 2022/12/15 15:16
# @Author : 乌贼
# @File : views.py
# @Software : PyCharm
import datetime

from flask import Blueprint
from flask import jsonify

from database.models import *
from methods.token import *
from utils.api_result import ApiResult

home_blue = Blueprint('home', __name__, url_prefix='/')


# @home_blue.route('/homePage', methods=['GET'])
# def user_trend():
#     # 返回数据
#     return_dict = {
#         "code": 500,
#         "data": {}
#     }
#
#     # 验证token
#     if validate_token():
#         try:
#             return_dict['code'] = 200
#             total_user = user.query.count()
#             return_dict['data']['totalUser'] = total_user
#             # 判断当前日期
#             yesterday = datetime.date.today() - datetime.timedelta(days=1)
#             increased_user = user.query.filter(
#                 user.register_time == yesterday
#             ).count()
#             return_dict['data']['increasedUser'] = increased_user
#             increased_feedback = feedback.query.filter(
#                 feedback.time >= yesterday
#             ).count()
#             return_dict['data']['increasedFeedback'] = increased_feedback
#             unhandled_feedback = feedback.query.filter(
#                 feedback.is_solve == 0
#             ).count()
#             return_dict['data']['unhandledFeedback'] = unhandled_feedback
#             increased_errorLog = log_error.query.filter(
#                 log_error.time >= yesterday
#             ).count()
#             return_dict['data']['increasedErrorLog'] = increased_errorLog
#         except Exception as e:
#             return_dict = {
#                 'code': 500,
#                 'msg': e
#             }
#
#     else:
#         return_dict = {
#             'code': 500,
#             'msg': 'token验证失败'
#         }
#
#     return jsonify(return_dict)

@home_blue.route('/homePage', methods=['GET'])
def user_trend():
    result = ApiResult()

    # 验证token
    if validate_token():
        try:
            data = {}
            total_user = user.query.count()
            data['totalUser'] = total_user
            # 判断当前日期
            yesterday = datetime.date.today() - datetime.timedelta(days=1)
            increased_user = user.query.filter(
                user.register_time == yesterday
            ).count()
            data['increasedUser'] = increased_user
            increased_feedback = feedback.query.filter(
                feedback.time >= yesterday
            ).count()
            data['increasedFeedback'] = increased_feedback
            unhandled_feedback = feedback.query.filter(
                feedback.is_solve == 0
            ).count()
            data['unhandledFeedback'] = unhandled_feedback
            increased_errorLog = log_error.query.filter(
                log_error.time >= yesterday
            ).count()
            data['increasedErrorLog'] = increased_errorLog
            return_dict = result.success(data)
        except Exception as e:
            return_dict = result.error(e)
    else:
        return_dict = result.error()
    print(str(return_dict))
    return jsonify(return_dict)
