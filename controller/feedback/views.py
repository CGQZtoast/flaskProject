# -*- coding = utf-8 -*-
# @Time : 2022/12/5 13:23
# @Author : 乌贼
# @File : views.py
# @Software : PyCharm

from flask import Blueprint, jsonify, request

from entity.feedback import *
from methods.token import *
from utils.api_result import ApiResult

feedback_blue = Blueprint('feedback', __name__, url_prefix='/')


@feedback_blue.route('/getFeedbackMsg', methods=['GET'])
def get_feedback_msg():
    result = ApiResult()
    # 验证token
    if validate_token():
        data = {}
        feedback_manege = FeedbackManege()
        msg = feedback_manege.get_feedback()
        data['backMsg'] = msg
        return_dict = result.success(data)
    else:
        return_dict = result.error()
    return jsonify(return_dict)


@feedback_blue.route('/submitFeedback', methods=['POST'])
def submit_feedback():
    result = ApiResult()
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
            return_dict = result.success()
        else:
            return_dict = result.error('处理反馈错误')
    else:
        return_dict = result.error()
    return jsonify(return_dict)


@feedback_blue.route('/delFeedback', methods=['POST'])
def delete_feedback():
    result = ApiResult()

    # 获取数据
    data = request.get_json()
    ids = data['id']
    print('[post]/delFeedback,收到的数据为：', data)

    # 验证token
    if validate_token():
        feedback_manege = FeedbackManege()
        if feedback_manege.delete_feedbacks(ids):
            return_dict = result.success()
        else:
            return_dict = result.error('日志删除失败')
    else:
        return_dict = result.error()
    return jsonify(return_dict)
