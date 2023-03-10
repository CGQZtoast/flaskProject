# -*- coding = utf-8 -*-
# @Time : 2022/12/5 14:05
# @Author : 乌贼
# @File : views.py
# @Software : PyCharm

from flask import Blueprint, request, jsonify

from entity.notice import sent_notice
from methods.token import validate_token
from utils.api_result import ApiResult

notice_blue = Blueprint('notice', __name__, url_prefix='/')


@notice_blue.route('/sendMsg', methods=['POST'])
def sent_msg():
    result = ApiResult()
    # 获取数据
    data = request.get_json()
    ids = data['id']
    msg = data['sendMsg']
    title = data['title']
    send_time = data['sendTime']
    print('[post]/sendMsgr,收到的数据为：', data)

    # 验证token
    if validate_token():
        if sent_notice(str(ids), msg, title, send_time):
            return_dict = result.success()
        else:
            return_dict = result.error('发送失败')
    else:
        return_dict = result.error()

    return jsonify(return_dict)
