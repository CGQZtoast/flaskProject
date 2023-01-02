# -*- coding = utf-8 -*-
# @Time : 2022/10/18 21:20
# @Author : 乌贼
# @File : exts.py
# @Software : PyCharm

# db对象

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def db_init():
    # db.drop_all()
    db.create_all()


