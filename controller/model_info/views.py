# -*- coding = utf-8 -*-
# @Time : 2022/12/5 9:17
# @Author : 乌贼
# @File : views.py
# @Software : PyCharm
import os

from flask import Blueprint, Response, jsonify, request

from entity.model import *
from methods.token import *

model_blue = Blueprint('model', __name__, url_prefix='/')

upload_path = r'/root/tmp1'  # 模型上传地址


@model_blue.route('/getFaceMdMsg', methods=['GET'])
def get_face_model_msg():
    return_dict = {
        'code': 500,
        'data': {}
    }
    # 验证token
    if validate_token():
        msg = get_face_model()
        if msg:
            return_dict['code'] = 200
            return_dict['data']['modelData'] = msg
        else:
            return_dict = {
                'code': 500,
                'msg': '模型不存在'
            }
    else:
        return_dict = {
            'code': 500,
            'msg': 'token验证失败'
        }

    return jsonify(return_dict)


@model_blue.route('/getFinMdMsg', methods=['GET'])
def get_fingerprint_model_msg():
    return_dict = {
        'code': 500,
        'data': {}
    }
    # 验证token
    if validate_token():
        msg = get_fingerprint_model()
        if msg:
            return_dict['code'] = 200
            return_dict['data']['modelData'] = msg
        else:
            return_dict = {
                'code': 500,
                'msg': '模型不存在'
            }
    else:
        return_dict = {
            'code': 500,
            'msg': 'token验证失败'
        }
    return jsonify(return_dict)


@model_blue.route('/upFaceMd', methods=['POST'])
def upload_face_model():
    # 返回数据
    return_dict = {
        'code': 200,
    }

    # 验证token
    if validate_token():
        # 获取数据
        model = request.files.get('faceMd')
        update_time = request.form.get('updateTime')
        if model is not None:
            # TODO upload_path + fingerprint_model
            model_path = os.path.join(upload_path, "face_model")
            model_path = os.path.join(model_path, model.filename)
            print(model_path)
            try:
                # TODO 去掉后缀
                name = model.filename
                name = os.path.splitext(name)[0]
                if add_face_model(update_time, name, model_path):
                    model.save(model_path)  # 上传文件写入
                else:
                    # 文件上传失败
                    return_dict['code'] = 401
                    return_dict['msg'] = '用户不存在'
            except IOError:
                # 文件上传失败
                return_dict['code'] = 402
                return_dict['msg'] = '文件保存失败'
        else:
            return_dict['code'] = 402
            return_dict['msg'] = '文件上传失败'
    else:
        return_dict['code'] = 500
        return_dict['msg'] = 'token验证失败'

    return jsonify(return_dict)


@model_blue.route('/upFinMd', methods=['POST'])
def upload_fingerprint_model():
    # 返回数据
    return_dict = {
        'code': 200,
    }
    # 验证token
    if validate_token():
        # 获取数据
        model = request.files.get('finMd')
        phone = request.form.get('phone')
        update_time = request.form.get('updateTime')
        if model is not None:
            model_path = os.path.join(upload_path, "fingerprint_model")
            model_path = os.path.join(model_path, model.filename)
            print(model_path)
            try:
                name = model.filename
                name = os.path.splitext(name)[0]
                if add_fingerprint_model(phone, update_time, name, model_path):
                    model.save(model_path)  # 上传文件写入
                else:
                    # 文件上传失败
                    return_dict['code'] = 408
                    return_dict['msg'] = '用户不存在'
            except IOError:
                # 文件上传失败
                return_dict['code'] = 402
                return_dict['msg'] = '文件保存失败'
        else:
            return_dict['code'] = 402
            return_dict['msg'] = '文件上传失败'
    else:
        return_dict['code'] = 500
        return_dict['msg'] = 'token验证失败'

    return jsonify(return_dict)


@model_blue.route('/dwnFaceMd', methods=['POST'])
def download_face_model():
    return_dict = {
        'code': 500
    }
    # 获取数据
    data = request.get_json()
    id = data['id']
    print('[post]/dwnFaceMd,收到的数据为：', data)
    # 查找模型路径
    path = get_path_of_face_model(id)
    print('[模型地址为：', path)
    if not path:
        return_dict['code'] = 500
        return_dict['msg'] = '模型不存在'
        return jsonify(return_dict)
    else:
        return Response(send_chunk(path), content_type='application/octet-stream')


@model_blue.route('/dwnFinMd', methods=['POST'])
def download_fingerprint_model():
    return_dict = {
        'code': 500
    }
    # 获取数据
    data = request.get_json()
    id = data['id']
    print('[post]/dwnFinMd,收到的数据为：', data)
    # 查找模型路径
    path = get_path_of_fingerprint_model(id)
    print('模型地址为：', path)
    if not path:
        return_dict['code'] = 500
        return_dict['msg'] = '模型不存在'
        return jsonify(return_dict)
    else:
        return Response(send_chunk(path), content_type='application/octet-stream')


@model_blue.route('/delFaceMd', methods=['POST'])
def del_face_model():
    # 返回数据
    return_dict = {
        "code": 500,
    }
    # 获取数据
    data = request.get_json()
    id = data['id']
    print('[post]/delFaceMd,收到的数据为：', data)

    # 验证token
    if validate_token():
        if delete_face_model(id):
            return_dict['code'] = 200
        else:
            return_dict['code'] = 500
            return_dict['msg'] = '删除人脸模型失败'
    else:
        return_dict['code'] = 500
        return_dict['msg'] = 'token验证失败'

    return jsonify(return_dict)


@model_blue.route('/delFinMd', methods=['POST'])
def del_fingerprint_model():
    # 返回数据
    return_dict = {
        "code": 500,
    }
    # 获取数据
    data = request.get_json()
    ids = data['id']
    print('[post]/delFinMd,收到的数据为：', data)

    # 验证token
    if validate_token():
        if delete_fingerprint_model(ids):
            return_dict['code'] = 200
        else:
            return_dict['code'] = 500
            return_dict['msg'] = '删除指纹声音模型失败'
    else:
        return_dict['code'] = 500
        return_dict['msg'] = 'token验证失败'
    return jsonify(return_dict)


@model_blue.route('/useFaceMd', methods=['POST'])
def use_face_model():
    # 返回数据
    return_dict = {
        "code": 500,
    }
    # 获取数据
    data = request.get_json()
    id = data['id']
    print('[post]/useFaceMd,收到的数据为：', data)
    # 验证token
    if validate_token():
        if shift_model(id):
            return_dict['code'] = 200
        else:
            return_dict['code'] = 500
            return_dict['msg'] = '切换使用模型失败'
    else:
        return_dict['code'] = 500
        return_dict['msg'] = 'token验证失败'

    return jsonify(return_dict)
