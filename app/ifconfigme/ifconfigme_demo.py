from flask import Blueprint , render_template, make_response, request
import json

#  创建蓝图 第一个参数为蓝图的名字
ifconfigme = Blueprint('ifconfigme',__name__)

@ifconfigme.route('/ifconfig/', methods=['GET','POST'])
@ifconfigme.route('/ifconfig')
def ifconfig_me():
    ip = request.remote_addr
    port = request.environ.get('REMOTE_PORT')
    try:
        ua = str(request.user_agent)
    except Exception as e_ua:
        ua = None
    try:
        xff = request.headers['X-Forwarded-For']
    except Exception as e_xff:
        xff = None
    try:
        host = request.headers['Host']
    except Exception as e_host:
        host = None
    return render_template('ifconfig_me.html', 
    user_ip=ip, 
    ua=ua, 
    xff=xff,
    host=host,
    port=port)

@ifconfigme.route('/ifconfig/ip/', methods=['GET','POST'])
@ifconfigme.route('/ifconfig/ip')
def ifconfig_ip():
    if request.method == 'GET' or request.method == 'POST':
        ip = request.remote_addr
        resp = make_response(ip, 200)
        return resp
    elif request.method == 'HEAD':
        resp = make_response("HEAD", 200)
        return resp

@ifconfigme.route('/ifconfig/port/', methods=['GET','POST'])
@ifconfigme.route('/ifconfig/port')
def ifconfig_port():
    if request.method == 'GET' or request.method == 'POST':
        post = request.environ.get('REMOTE_PORT')
        resp = make_response(port, 200)
        return resp
    elif request.method == 'HEAD':
        resp = make_response("HEAD", 200)
        return resp

@ifconfigme.route('/ifconfig/ua/', methods=['GET','POST'])
@ifconfigme.route('/ifconfig/ua')
def ifconfig_ua():
    if request.method == 'GET' or request.method == 'POST':
        UA = request.user_agent.string    
        resp = make_response(UA, 200)
        return resp
    elif request.method == 'HEAD':
        resp = make_response("HEAD", 200)
        return resp

@ifconfigme.route('/ifconfig/ua.json', methods=['GET','POST'])
def ifconfig_ua_json():
    if request.method == 'GET' or request.method == 'POST':
        UA = request.user_agent
        data = {
            "User-Agent" : UA.string,
            "ua_browser" :UA.browser,
            "ua_version" : UA.version,
            "ua_platform" : UA.platform,
            "ua_language" : UA.language,
        }
        json_str = json.dumps(data, ensure_ascii=False)
        
        resp = make_response(json_str, 200)
        return resp
    elif request.method == 'HEAD':
        resp = make_response("HEAD", 200)
        return resp

@ifconfigme.route('/ifconfig/xff/', methods=['GET','POST'])
@ifconfigme.route('/ifconfig/xff')
def ifconfig_xff():
    if request.method == 'GET' or request.method == 'POST':
        try:
            xff = request.headers['X-Forwarded-For']
        except Exception as e_xff:
            xff = None
        resp = make_response(xff, 200)
        return resp
    elif request.method == 'HEAD':
        resp = make_response("HEAD", 200)
        return resp

@ifconfigme.route('/ifconfig/host/', methods=['GET','POST'])
@ifconfigme.route('/ifconfig/host')
def ifconfig_host():
    if request.method == 'GET' or request.method == 'POST':
        try:
            host = request.headers['Host']
        except Exception as e_xff:
            host = None
        resp = make_response(host, 200)
        return resp
    elif request.method == 'HEAD':
        resp = make_response("HEAD", 200)
        return resp
