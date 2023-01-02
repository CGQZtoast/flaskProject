# -*- coding = utf-8 -*-
# @Time : 2022/12/5 13:23
# @Author : 乌贼
# @File : views.py
# @Software : PyCharm

from flask import Blueprint, jsonify, request

from entity.feedback import *
from methods.token import *

feedback_blue = Blueprint('feedback', __name__, url_prefix='/')


@feedback_blue.route('/getFeedbackMsg', methods=['GET'])
def get_feedback_msg():
    return_dict = {
        'code': 500,
        'data': {}
    }
    # 验证token
    if validate_token():
        feedback_manege = FeedbackManege()
        msg = feedback_manege.get_feedback()
        return_dict['code'] = 200
        return_dict['data']['backMsg'] = msg
    else:
        return_dict = {
            'code': 500,
            'msg': 'token验证失败，请重新登录'
        }
    return jsonify(return_dict)


@feedback_blue.route('/submitFeedback', methods=['POST'])
def submit_feedback():
    # 返回数据
    return_dict = {
        'code': 500,
    }
    # 获取数据
    data = request.get_json()
    id = data['id']
    msg = data['returnMsg']
    back_time = data['backTime']
    print('[post]/delUser,收到的数据为：', data)

    # 验证token
    if validate_token():
        feedback_manege = FeedbackManege()
        if feedback_manege.handling_feedback(id, msg, back_time):
            return_dict['code'] = 200
        else:
            return_dict['code'] = 500
            return_dict['msg'] = '处理反馈错误'
    else:
        return_dict['code'] = 500
        return_dict['msg'] = 'token验证失败'

    return jsonify(return_dict)


@feedback_blue.route('/delFeedback', methods=['POST'])
def delete_feedback():
    # 返回数据
    return_dict = {
        "code": 500,
    }
    # 获取数据
    data = request.get_json()
    ids = data['id']
    print('[post]/delFeedback,收到的数据为：', data)

    # 验证token
    if validate_token():
        feedback_manege = FeedbackManege()
        if feedback_manege.delete_feedbacks(ids):
            return_dict['code'] = 200
        else:
            return_dict['code'] = 500
            return_dict['msg'] = '日志删除失败'
    else:
        return_dict['code'] = 500
        return_dict['msg'] = 'token验证错误'

    return jsonify(return_dict)
