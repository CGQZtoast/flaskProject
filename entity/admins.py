# -*- coding = utf-8 -*-
# @Time : 2022/11/7 22:53
# @Author : 乌贼
# @File : admins.py
# @Software : PyCharm

from sqlalchemy import func, null
from sqlalchemy.exc import DataError, OperationalError

from database.models import *
from methods.get_date import *


# 管理员类
class Admins(object):
    # private_data
    __id = 0  # id
    __account = ''  # 账号
    __password = ''  # 密码

    # 初始化管理员对象
    def __init__(self, account, password=None):
        """
        初始化管理员对象
        :param account:
        :param password:
        """
        self.__account = account
        self.__password = password

    # 验证账号密码
    def verify(self):
        """
        验证账号密码
        :return: True or False
        """
        # 在数据库中查找该账号和对应的密码是否存在
        obj = admin.query.filter(
            admin.account == self.__account,
            admin.password == self.__password
        )
        if obj.first() is not None:
            return True
        return False

    # 设置管理员信息
    def set_info(self):
        """
        设置管理员信息
        :return:
        """
        info = db.session.query(
            admin.id
        ).filter(
            admin.account == self.__account,
            admin.password == self.__password
        ).first()
        user_id = info[0]
        self.__id = user_id

    # 获取id
    def get_id(self):
        """
        获取id
        :return: self.__id
        """
        return self.__id

    # 获取账号
    def get_account(self):
        """
        获取账号
        :return: self.__account
        """
        return self.__account

    # 写入数据库
    def add_admin(self):
        administrator = admin(
            account=self.__account,
            password=self.__password,
        )
        # 添加
        db.session.add(administrator)
        # 提交保存
        db.session.commit()
        return True
