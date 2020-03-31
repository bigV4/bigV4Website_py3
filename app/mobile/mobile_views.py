# coding: utf-8
# coding: utf-8
# 将RESTful-api注册为蓝图

from flask import render_template, make_response, request,jsonify
from flask_restful import Api, Resource
from flask import Blueprint
from werkzeug.utils import secure_filename
import base64
import os
import time
import json
mobile = Blueprint('mobile', __name__)


@mobile.route('/mobile/', methods=['GET','POST'])
def mobilemain():
    return '/mobile/'
    pass



userInfo = {
            'feifei': {'user_name': 'feifei', 'age': '30', 'sex': 'male', 'Tel': '13867239769', 'amount': '10000'},
            'qiqi': {'user_name': 'qiqi', 'age': '25', 'sex': 'female', 'Tel': '17788127747', 'amount': '30000'},
            'liyi': {'user_name': 'liyi', 'age': '20', 'sex': 'male', 'Tel': '18862379965', 'amount': '22000'},
            'lili': {'user_name': 'lili', 'age': '56', 'sex': 'female', 'Tel': '13934081287', 'amount': '20030'},
            'zhangdm': {'user_name': 'zhangdm', 'age': '27', 'sex': 'male', 'Tel': '16691839283', 'amount': '60000'},
            'limumu': {'user_name': 'limumu', 'age': '21', 'sex': 'male', 'Tel': '13199238746', 'amount': '70000'},
            'limu': {'user_name': 'limu', 'age': '29', 'sex': 'male', 'Tel': '138618397712', 'amount': '77000'}
            }

userPasswdDic = {
            'feifei': "PassWord",
            'qiqi': "123456",
            'liyi': "666666",
            'lili': "mimajiushi1",
            'zhangdm': "123321",
            'limumu': "qazwsx",
            'limu': "qwe123"
            }

@mobile.route("/mobile/userdetail/", methods=['GET', 'POST'])
def mobile_userDetail():
    user = ""
    if request.method == 'GET':
        user = request.args.get("user")
    elif request.method == 'POST':
        if request.form is not None and len(request.form) > 0:
            user = request.form.get("user")

    resp = make_response(json.dumps(userInfo.get(user, ""), ensure_ascii=False))
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp


@mobile.route("/mobile/register/", methods=['GET', 'POST', 'OPTIONS', 'HEAD'])
@mobile.route("/mobile/login/", methods=['GET', 'POST', 'OPTIONS', 'HEAD'])
@mobile.route("/mobile/login", methods=['GET', 'POST', 'OPTIONS', 'HEAD'])
@mobile.route("/mobile/userinfo.do", methods=['GET', 'POST', 'OPTIONS', 'HEAD'])
def mobile_register():
    user = ""
    name = ""
    password = ""
    argslist =[]
    if request.method == 'POST':
        try:
            if request.json is not None:
                #请求的Content-Type: application/json
                #curl -H "Content-Type:application/json" -X POST -d '{"uid":"admin", "passw":"12345678"}' http://127.0.0.1:8089/mobile/login
                data = request.json
                print("request.json",type(request.json), request.json)
                name = data["uid"]
                password = data["passw"]
                print("name",name)
                print("password",password)
            elif request.form is not None and len(request.form) > 0:
                #请求的Content-Type: application/x-www-form-urlencoded
                data = request.form
                print("request.form",type(request.form), request.form)
                for key in data:
                    argslist.append(key)
                print(argslist)
                if ""!=data.getlist(argslist[0])[0]:
                    #data为uid=qiqi&passw=123456的情况
                    #curl -d "uid=admin&passw=12345678" http://127.0.0.1:8089/mobile/login
                    name = data.getlist("uid")[0]
                    password = data.getlist("passw")[0]
                else:
                    #data为qiqi&123456的情况
                    #curl -d "admin&12345678" http://127.0.0.1:8089/mobile/login
                    for key in data:
                        if not name:
                            name = key
                        elif not password:
                            password = key
                    
            elif type(request.data) == str:
                data = json.dumps(request.data, ensure_ascii=False)

            user = data.get("user_name")
        except Exception as e:
            print("Json does not exist!!")
            print(e)
            return str(e)
    elif request.method == 'GET':
        name = request.args.get("uid")
        password = request.args.get("passw")

    info = ""
    if name in userInfo.keys():
        if password == userPasswdDic.get(name):
            info = userInfo.get(name)
        else:
            info = {'error': u'密码错误!'}

    if not info:
        info = {'error': u'用户不存在!'}

    resp = make_response(json.dumps(info, ensure_ascii=False))
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS,HEAD'
    return resp

