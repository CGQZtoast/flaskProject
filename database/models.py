# -*- coding = utf-8 -*-
# @Time : 2022/10/18 21:22
# @Author : 乌贼
# @File : models.py
# @Software : PyCharm

# 表对象
# 建表写在models.py文件里面

from database.ext import db


# ==============================================================
#  Table: admin
# ==============================================================
class admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.String(11), primary_key=True)
    password = db.Column(db.String(20), nullable=False)


# ==============================================================
#  Table: classic_problem                                       
# ==============================================================
class classic_problem(db.Model):
    __tablename__ = 'classic_problem'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(200), nullable=False)


# ==============================================================
#  Table: feedback                                              
# ==============================================================
class feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'), nullable=False)
    time = db.Column(db.Date, nullable=False)
    info = db.Column(db.Text, nullable=False)
    is_solve = db.Column(db.SmallInteger, nullable=False)
    admin_feedback = db.Column(db.String(200))
    admin_feedback_time = db.Column(db.Date)


# ==============================================================
#  Table: log_error                                             
# ==============================================================
class log_error(db.Model):
    __tablename__ = 'log_error'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.Date, nullable=False)
    info = db.Column(db.Text, nullable=False)


# ==============================================================
#  Table: log_login                                             
# ==============================================================
class log_login(db.Model):
    __tablename__ = 'log_login'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'), nullable=False)
    time = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(50), nullable=False)
    device = db.Column(db.String(50), nullable=False)


# ==============================================================
#  Table: model_face                                            
# ==============================================================
class model_face(db.Model):
    __tablename__ = 'model_face'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    path = db.Column(db.String(500), nullable=False)
    upload_time = db.Column(db.Date, nullable=False)
    used = db.Column(db.SmallInteger, nullable=False)


# ==============================================================
#  Table: model_fingerprint                                     
# ==============================================================
class model_fingerprint(db.Model):
    __tablename__ = 'model_fingerprint'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    path = db.Column(db.String(500), nullable=False)
    update_time = db.Column(db.Date)


# ==============================================================
#  Table: permissions                                           
# ==============================================================
class permissions(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)


# ==============================================================
#  Table: pwd_face                                              
# ==============================================================
class pwd_face(db.Model):
    __tablename__ = 'pwd_face'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    image_path = db.Column(db.String(500), nullable=False)


# ==============================================================
#  Table: pwd_fingerprint                                       
# ==============================================================
class pwd_fingerprint(db.Model):
    __tablename__ = 'pwd_fingerprint'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    path = db.Column(db.String(500), nullable=False)


# ==============================================================
#  Table: role
# ==============================================================
class role(db.Model):
    __tablename__ = 'role'
    name = db.Column(db.String(20), nullable=False)
    id = db.Column(db.Integer, primary_key=True, nullable=False)


# ==============================================================
#  Table: role_permission                                       
# ==============================================================
class role_permission(db.Model):
    __tablename__ = 'role_permission'
    role_id = db.Column(db.Integer, db.ForeignKey("role.id", ondelete='CASCADE'), primary_key=True)
    permission_id = db.Column(db.Integer, db.ForeignKey("permissions.id", ondelete='CASCADE'), primary_key=True)


# ==============================================================
#  Table: user
# ==============================================================
class user(db.Model):
    __tablename__ = 'user'
    phone = db.Column(db.String(11), nullable=False)
    DOB = db.Column(db.Date)
    sex = db.Column(db.SmallInteger)
    province = db.Column(db.String(50))
    city = db.Column(db.String(50))
    district = db.Column(db.String(50))
    register_time = db.Column(db.Date)
    image_path = db.Column(db.String(500))
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    fingerprint_model_id = db.Column(db.Integer, db.ForeignKey("model_fingerprint.id", ondelete='CASCADE'), nullable=False)


# ==============================================================
#  Table: user_role                                             
# ==============================================================
class user_role(db.Model):
    __tablename__ = 'user_role'
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'), primary_key=True, nullable=False)
    id = db.Column(db.Integer, db.ForeignKey("role.id", ondelete='CASCADE'), primary_key=True, nullable=False)


# ==============================================================
#  Table: notice
# ==============================================================
class notice(db.Model):
    __tablename__ = 'notice'
    notice_id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_ids = db.Column(db.Text)
    notice_info = db.Column(db.Text)
    notice_time = db.Column(db.Date)
    notice_title = db.Column(db.String(255))
