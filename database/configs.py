# -*- coding = utf-8 -*-
# @Time : 2022/10/18 21:17
# @Author : 乌贼
# @File : configs.py
# @Software : PyCharm

# 数据库配置

# HOST = '127.0.0.1'
# PORT = '3306'
# DATABASE = 'sapas'
# USERNAME = 'root'
# PASSWORD = '123456'

HOST = '1.15.114.189'
PORT = '3306'
DATABASE = 'sapas'
USERNAME = 'remote'
PASSWORD = '123456'

DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(
    username=USERNAME,
    password=PASSWORD,
    host=HOST,
    port=PORT,
    db=DATABASE
)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False  # 设置为false时将不会显示sql语句
