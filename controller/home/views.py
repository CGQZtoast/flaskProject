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

home_blue = Blueprint('home', __name__, url_prefix='/')


@home_blue.route('/homePage', methods=['GET'])
def user_trend():
    # 返回数据
    return_dict = {
        "code": 500,
        "data": {}
    }

    # 验证token
    if validate_token():
        try:
            return_dict['code'] = 200
            total_user = user.query.count()
            return_dict['data']['totalUser'] = total_user
            # 判断当前日期
            yesterday = datetime.date.today() - datetime.timedelta(days=1)
            increased_user = user.query.filter(
                user.register_time == yesterday
            ).count()
            return_dict['data']['increasedUser'] = increased_user
            increased_feedback = feedback.query.filter(
                feedback.time >= yesterday
            ).count()
            return_dict['data']['increasedFeedback'] = increased_feedback
            unhandled_feedback = feedback.query.filter(
                feedback.is_solve == 0
            ).count()
            return_dict['data']['unhandledFeedback'] = unhandled_feedback
            increased_errorLog = log_error.query.filter(
                log_error.time >= yesterday
            ).count()
            return_dict['data']['increasedErrorLog'] = increased_errorLog
        except Exception as e:
            return_dict = {
                'code': 500,
                'msg': e
            }

    else:
        return_dict = {
            'code': 500,
            'msg': 'token验证失败'
        }

    return jsonify(return_dict)
