#coding:utf8
 
from flask import Blueprint , render_template
 
#  创建蓝图 第一个参数为蓝图的名字
login = Blueprint('login',__name__)
 
@login.route('/login_demo')
def login_demo():
    return 'login_demo'