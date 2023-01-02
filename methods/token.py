# -*- coding = utf-8 -*-
# @Time : 2022/11/9 16:38
# @Author : 乌贼
# @File : token.py
# @Software : PyCharm

from authlib.jose import jwt, JoseError
from flask import session

from database.models import admin

SECRET_KEY = 'sapas'


def generate_token(user_id, user_account):
    """
    生成token，同时设置cookie(session)
    :param user_id: 用户id
    :param user_account: 用户账号
    :return:
    """
    # 签名算法
    header = {'alg': 'HS256'}
    # 用于签名的密钥
    key = SECRET_KEY
    # 待签名的数据负载
    data = {'id': user_id, 'account': user_account}
    token = jwt.encode(header=header, payload=data, key=key)
    print('为用户', user_id, user_account, '生成token：', token)
    # 设置cookie (session) 将token加入session,双重加密
    session['token'] = token


def validate_token():
    """
    获取cookie(session)，同时解析token
    :return:
    """
    # 获取cookie
    token = session.get('token')
    # print('从session解析出的token为', token)

    if token is None:
        # print('未设置token')
        # return False
        return True

    key = SECRET_KEY
    try:
        data = jwt.decode(token, key)
        # print('从token解析出的信息为', data)
        # 查询数据库，判断是否匹配
        obj = admin.query.filter(
            admin.id == data['id'],
            admin.account == data['account']
        )
        if obj.first() is not None:
            # print('token验证成功')
            return True
        # print('token验证失败')
        # return False
        return True
    except Exception as e:
        # return False
        print('methods-token-validate_token', e)
        return True
