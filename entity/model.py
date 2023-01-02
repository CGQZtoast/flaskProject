# -*- coding = utf-8 -*-
# @Time : 2022/11/21 8:17
# @Author : 乌贼
# @File : model.py
# @Software : PyCharm

from database.models import *


def send_chunk(path):  # 流式读取
    store_path = path
    try:
        with open(store_path, 'rb') as target_file:
            while True:
                chunk = target_file.read(20 * 1024 * 1024)  # 每次读取20M
                if not chunk:
                    break
                yield chunk
    except FileNotFoundError:
        print('该路径下不存在模型文件')



# 查找模型路径
def get_path_of_fingerprint_model(id):
    path = db.session.query(
        model_fingerprint.path
    ).filter(
        model_fingerprint.id == id
    ).first()
    if path is not None:
        return path[0]
    else:
        return False


def get_path_of_face_model(id):
    path = db.session.query(
        model_face.path
    ).filter(
        model_face.id == id
    ).first()
    if path is not None:
        return path[0]
    else:
        return False


def get_face_model():
    model_data = []
    model_msg = db.session.query(
        model_face.id,
        model_face.name,
        model_face.upload_time,
        model_face.used
    ).all()
    for msg in model_msg:
        model = {}
        print(msg)
        model['id'] = msg[0]
        model['modelNo'] = msg[1]
        model['updateTime'] = str(msg[2])
        model['isUse'] = msg[3]
        model_data.append(model)
    return model_data


def get_fingerprint_model():
    model_data = []
    model_msg = db.session.query(
        model_fingerprint.id,
        model_fingerprint.name,
        user.phone,
        model_fingerprint.update_time
    ).filter(
        model_fingerprint.user_id == user.id
    ).all()
    for msg in model_msg:
        model = {}
        print(msg)
        model['id'] = msg[0]
        model['modelNo'] = msg[1]
        model['phone'] = msg[2]
        model['updateTime'] = str(msg[3])
        model_data.append(model)
    return model_data


def add_fingerprint_model(phone, update_time, name, file_path):
    # 查找数据库，用户是否存在模型
    model1 = model_fingerprint.query.filter(
        user.phone == phone,
        user.id == model_fingerprint.user_id
    ).first()
    if model1 is not None:
        model1.update_time = update_time
        model1.name = name
        model1.path = file_path
        db.session.commit()
        return True
    else:
        temp_user = user.query.filter(user.phone == phone).first()
        if temp_user is None:
            print(phone, '用户不存在')
            return False
        else:
            try:
                id = temp_user.id
                model = model_fingerprint(user_id=id, name=name,path=file_path,update_time=update_time)
                db.session.add(model)
                db.session.commit()
                return True
            except Exception as e:
                print('error:', e)
                return False


def add_face_model(update_time, name, file_path):
    try:
        model = model_face(name=name, path=file_path, upload_time=update_time,
                           used=0)
        db.session.add(model)
        db.session.commit()
        return True
    except Exception as e:
        print('error:', e)
        return False


def delete_face_model(id):
    try:
        model_face.query.filter(model_face.id == id).delete()
        db.session.commit()
        return True
    except Exception as e:
        print('删除模型人脸错误：', e)
        return False


def delete_fingerprint_model(ids):
    try:
        for id in ids:
            model_fingerprint.query.filter(model_fingerprint.id == id).delete()
            db.session.commit()
        return True
    except Exception as e:
        print('删除模型指纹声音错误：', e)
        return False


def shift_model(id):
    try:
        model = model_face.query.filter(model_face.used == 1).first()
        if model is not None:
            model.used = 0

        model1 = model_face.query.filter(model_face.id == id).first()
        model1.used = 1
        db.session.commit()
        return True
    except Exception as e:
        print('切换人脸模型使用失败：', e)
        return False
