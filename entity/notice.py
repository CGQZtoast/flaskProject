# -*- coding = utf-8 -*-
# @Time : 2022/12/5 14:09
# @Author : 乌贼
# @File : notice.py.py
# @Software : PyCharm

from database.ext import db
from database.models import notice


def sent_notice(ids, msg, title, send_time):
    try:
        # TODO 去掉空格
        ids = ids.replace(' ', '')
        msg = notice(notice_info=msg, user_ids=ids, notice_title=title, notice_time=send_time)
        db.session.add(msg)
        db.session.commit()
        return True
    except Exception as e:
        print('error', e)
        return False
