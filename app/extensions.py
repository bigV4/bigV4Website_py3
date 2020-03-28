# coding: utf-8
# 组织扩展(Extensions),一般推荐将所有扩展在app/extensions.py中进行实例化
'''
常用扩展（Extensions）
Flask作为微框架（microframework），在开发过程中会经常使用各种扩展包。以下是一些常用扩展包的简介。

Flask-SQLAlchemy - 封装了SQLAlchemy，提供ORM
Flask-Migrate - 处理SQLAlchemy数据库的迁移（migrations）
Flask-Script - 支持在Flask里编写额外的脚本
Flask-Bootstrap - 封装了Bootstrap框架
Flask-Login - 提供账号session管理
Flask-WTF - 封装了WTForms，提供表单功能
Flask-RESTful - 提供快速构建RESTAPIs的能力
'''
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth_bp.login'