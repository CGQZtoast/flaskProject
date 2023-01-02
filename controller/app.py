# -*- coding = utf-8 -*-
# @Time : 2022/11/8 23:24
# @Author : 乌贼
# @File : app.py
# @Software : PyCharm

import os
from flask import Flask
from flask_cors import CORS
import sys
from database import configs
from database.ext import *


# 蓝图导入
from login.views import login_blue
from home.views import home_blue
from statistical.views import statistical_blue
from userinfo.views import userinfo_blue
from model_info.views import model_blue
from feedback.views import feedback_blue
from log_info.views import log_blue
from notice.views import notice_blue

sys.path.append(r'../')

app = Flask(__name__)

# 配置跨域
CORS(app, resources=r'/*')
# CORS(app, supports_credentials=True)

# 加载配置文件
app.config.from_object(configs)
# db绑定app
db.init_app(app)

app.secret_key = os.urandom(24)	 # secret_key一般是长度为24的随机字符串（token）

# 注册蓝图
app.register_blueprint(login_blue)  # 登录（管理员）
app.register_blueprint(home_blue)  # 主界面
app.register_blueprint(statistical_blue)  # 用户数据统计（人数、趋势）
app.register_blueprint(userinfo_blue)  # 用户信息（查看、编辑、删除用户信息）
app.register_blueprint(model_blue)  # 模型信息
app.register_blueprint(feedback_blue)  # 反馈信息
app.register_blueprint(log_blue)  # 日志信息（登录日志、错误日志）
app.register_blueprint(notice_blue)  # 发送通知


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
