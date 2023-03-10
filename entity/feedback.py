# -*- coding = utf-8 -*-
# @Time : 2022/11/28 7:59
# @Author : 乌贼
# @File : feedback.py
# @Software : PyCharm

import datetime

import userinfo.views
from database.models import *


class Feedback(object):
    __id = 0  # 反馈的id
    __user_id = 0  # 用户id
    __phone = ""  # 用户的手机号
    __time = datetime.date(2022, 1, 1)  # 反馈id
    __info = ""  # 反馈信息
    __is_solve = 0  # 是否解决
    __feedback = ""  # 管理员的反馈

    def __init__(self, id, phone, msg, time, is_solve):
        self.__id = id
        self.__phone = phone
        self.__info = msg
        self.__time = time
        self.__is_solve = is_solve

    def get_dict(self):
        # temp_feedback = {'id': self.__id, 'phone': self.__phone, 'msg': self.__info, 'time': str(self.__time), 'isSolve': self.__is_solve, 'images': self.__image_path}
        temp_feedback = {'id': self.__id, 'phone': self.__phone, 'msg': self.__info, 'time': str(self.__time), 'isSolve': self.__is_solve}
        return temp_feedback


class FeedbackManege(object):
    __feedback_msg = []

    def __init__(self):
        self.__feedback_msg.clear()

    def get_feedback(self):
        msgs = db.session.query(
            feedback.id,
            user.phone,
            feedback.info,
            feedback.time,
            feedback.is_solve
        ).filter(
            feedback.user_id == user.id,
            feedback.deleted != 1
        ).all()
        if msgs is not None:
            for msg in msgs:
                temp_feedback = Feedback(msg.id, msg.phone, msg.info, msg.time, msg.is_solve)
                self.__feedback_msg.append(temp_feedback.get_dict())
        self.__feedback_msg.reverse()
        return self.__feedback_msg

    def handling_feedback(self, id, msg, time):
        try:
            edit_feedback = feedback.query.filter(feedback.id == id).first()
            if edit_feedback is not None:
                edit_feedback.admin_feedback = msg
                edit_feedback.admin_feedback_time = time
                edit_feedback.is_solve = 1
                db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def delete_feedbacks(self, ids):
        try:
            for id in ids:
                # feedback.query.filter(feedback.id == id).delete()
                temp_feedback = feedback.query.filter(feedback.id == id).first()
                if temp_feedback is not None:
                    temp_feedback.deleted = 1
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
