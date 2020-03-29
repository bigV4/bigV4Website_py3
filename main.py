# -*-coding:utf8 -*-
# python3
import os
import sqlite3
import json
import os.path
import sys
import time

from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, Response, make_response, jsonify, current_app, \
    send_from_directory, after_this_request


import functools
from functools import wraps
import gzip
from io import StringIO as IO
import io as StrIO   

from werkzeug import utils

from login_demo import login    # 从分路由倒入路由函数
from app.ifconfigme.ifconfigme_demo import ifconfigme # 从分路由倒入路由函数
from app.api.api_views import tmp_api # 从分路由倒入路由函数
app = Flask(__name__,template_folder='templates')


# 注册蓝图 第一个参数 是蓝图对象
app.register_blueprint(ifconfigme) # 注册蓝图ifconfigme 第一个参数 是蓝图对象
app.register_blueprint(tmp_api) # 注册蓝图tmp_api 第一个参数 是蓝图对象

app.config.from_object(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'bank.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def get_response_data(data):
    return_dict = {'records': data}
    try:
        resp_data = json.dumps(return_dict).decode('unicode-escape').encode('utf-8')
    except Exception as e:
        print(e)
        resp_data = json.dumps(return_dict, ensure_ascii=False)

    return resp_data


def get_request_data(request, for_key):
    data = dict
    if request.method == 'GET':
        data = request.args
    else:
        try:
            if request.json is not None:
                data = request.json
                data = json.dumps(json.loads(data), ensure_ascii=False)
            elif request.form is not None and len(request.form) > 0:
                data = json.dumps(request.form, ensure_ascii=False)
            else:
                data = request.data

        except Exception as e:
            print("Request data does not exist!")
            print(str(e))
            return str(e)

    if for_key and for_key in data:
        return data.get(for_key, "")

    return data


def jsonp(func):
    """Wraps JSONified output for JSONP requests."""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            data = str(func(*args, **kwargs).data)
            content = str(callback) + '(' + data + ')'
            mimetype = 'application/javascript'
            return current_app.response_class(content, mimetype=mimetype)
        else:
            return func(*args, **kwargs)

    return decorated_function


def gzipped(f):
    """
    只支持POST、PUT请求
    """

    @functools.wraps(f)
    def view_func(*args, **kwargs):
        @after_this_request
        def zipper(response):
            accept_encoding = request.headers.get('Accept-Encoding', '')
            print("Request Accept-Encoding {0}".format(accept_encoding))

            if 'gzip' not in accept_encoding.lower():
                return response

            response.direct_passthrough = False

            if (response.status_code < 200 or
                    response.status_code >= 300 or
                    'Content-Encoding' in response.headers):
                return response

            if request.method not in ["POST", "PUT"]:
                return response

            try:
                if not response.data:
                    return response

                gzip_buffer = IO()
                gzip_file = gzip.GzipFile(mode='wb', fileobj=gzip_buffer)
                gzip_file.write(response.data)
                gzip_file.close()

                response.data = gzip_buffer.getvalue()
                gzip_buffer.close()
                print("Gzip response data successfully.")
                response.headers['Content-Encoding'] = 'gzip'
                response.headers['Vary'] = 'Accept-Encoding'

                return response
            except Exception as e:
                return response

        return f(*args, **kwargs)

    return view_func


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """
    Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    if os.path.isfile(app.config['DATABASE']):
        print("os.path.isfile(app.config['DATABASE'])")
        pass
        #return
    with app.app_context():
        db = get_db()
        print
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
    print("init_db()")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/", methods=['GET', 'POST'])
@app.route("/index/")
@app.route("/index.jsp")
@app.route("/index.asp")
@app.route("/index.aspx")
@app.route("/index.php")
@app.route("/index.html")
@app.route("/index.htm")
@app.route("/index.mhtml")
def home():
    return render_template('index.html')


@app.route("/large_page/", methods=['GET', 'POST'])
def large_page():
    return render_template('large_page.html')


@app.route('/sync_conf/', methods=['GET', 'POST', 'DELETE'])
@app.route('/api/', methods=['GET', 'POST', 'DELETE'])
@gzipped
def show_entries():
    db = get_db()
    if request.method == 'DELETE':
        db.execute('DELETE FROM bank')
        db.commit()
        try:
            if request.json is not None:
                data = request.json

            elif request.form is not None:
                data = request.form
            else:
                data = request.data
            data = json.dumps(data)

        except Exception as e:
            print("Json does not exist!!")
            print(str(e))
            return str(e)

    if request.method == 'POST':
        try:
            if request.json is not None:
                data = request.json
                data = json.dumps(json.loads(data), ensure_ascii=False)
            elif request.form is not None and len(request.form) > 0:
                data = json.dumps(request.form, ensure_ascii=False)
            else:
                data = request.data

        except Exception as e:
            print("Json does not exist!!")
            print(str(e))
            return str(e)
        cur = db.execute('SELECT * FROM bank ORDER BY id DESC LIMIT 1')
        entry = cur.fetchall()

        if data and type(data) == dict:
            summary = data.get('trans')
            trans = data.get('trans')
            trans_type = data.get('type')

            if summary is None or trans is None or trans_type is None:
                pass
            else:
                db.execute('INSERT INTO bank (type, trans, sum) VALUES (?, ?, ?)',
                           [trans_type, trans, summary])
                db.commit()

    if request.method == 'GET':
        data = request.args
        cur = db.execute('SELECT * FROM bank ORDER BY id DESC LIMIT 1')
        entry = cur.fetchall()

        if data:
            if data.get("trans") and data.get("type"):
                summary = data.get('trans')
                db.execute('INSERT INTO bank (type, trans, sum) VALUES (?, ?, ?)',
                           [data.get('type'), data.get('trans'), summary])
                db.commit()
            else:
                print("Request with no trans & type.")
        else:
            print("Request with no args.")

    cur = db.execute('SELECT * FROM bank ORDER BY id DESC LIMIT 1')
    entries = cur.fetchall()

    try:
        buf = StrIO.StringIO(data)
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
        buf.close()
        f.close()
    except Exception as ex:
        print("Request data: ", ex)

    resp_data = get_response_data(data)
    resp = make_response(resp_data)
    resp.headers["Content-type"] = "application/json"
    resp.headers["Content-Length"] = len(resp_data)
    return resp


@app.route('/api/gzip/', methods=['POST', 'GET'])
def api_gzip():
    accept_encoding = request.headers.get('Accept-Encoding', '')
    print("accept_encoding: ", accept_encoding)
    print("Request Data: ", request.data)
    print("Request Args: ", request.args)
    if request.data:
        request_body = request.data
    elif request.args and len(request.args) > 0:
        request_body = request.args.get("data", "")
    elif request.form and len(request.form) > 0:
        request_body = request.form.get("data", "")
    else:
        request_body = ""

    DEFAULT_RESPONSE = "Can not get any request body, this is default response."
    body = DEFAULT_RESPONSE if request_body == "" else request_body
    try:
        buf = StrIO.StringIO(body)
        f = gzip.GzipFile(fileobj=buf)
        body = f.read()
        buf.close()
        f.close()
    except Exception as ex:
        print("Request data: {0}, needn't to unzip.".format(ex))

    data = json.dumps({'records': body}).decode('unicode-escape').encode('utf-8')

    gzip_buffer = IO()
    gzip_file = gzip.GzipFile(mode='wb', fileobj=gzip_buffer)
    gzip_file.write(data)
    gzip_file.close()

    zip_data = gzip_buffer.getvalue()
    gzip_buffer.close()

    print("Response Data: ", zip_data)

    response = make_response(zip_data)
    response.headers["Content-type"] = "application/json"
    response.headers['Content-Encoding'] = 'gzip'
    response.headers['Vary'] = 'Accept-Encoding'

    return response


@app.route('/test/api/test/', methods=['GET', 'POST', 'DELETE'])
def show_entries2():
    db = get_db()

    if request.method == 'DELETE':
        db.execute('DELETE FROM bank')
        db.commit()

    if request.method == 'POST':
        print(request.data)
        print(request.json)
        data = request.json
        cur = db.execute('SELECT * FROM bank ORDER BY id DESC LIMIT 1')
        entry = cur.fetchall()

        if data:
            summary = data['trans']
            # if len(entry) is not 0:
            #     r = entry[0]
            #     trans_type = data['type']
            #     if trans_type is 1:
            #         summary += r[3]
            #     elif trans_type is 2:
            #         summary = r[3] - summary

            db.execute('INSERT INTO bank (type, trans, sum) VALUES (?, ?, ?)',
                       [data['type'], data['trans'], summary])
            db.commit()

    # cur = db.execute('select * from bank order by id desc')
    cur = db.execute('SELECT * FROM bank ORDER BY id DESC LIMIT 1')
    entries = cur.fetchall()
    data = list()
    for row in entries:
        r = dict()
        r['type'] = row[1]
        r['trans'] = row[2]
        r['sum'] = row[3]
        data.append(r)
    return json.dumps({'records': data})


@app.route('/test/test/', methods=['GET', 'POST', 'DELETE'])
def show_entries3():
    db = get_db()

    if request.method == 'DELETE':
        db.execute('DELETE FROM bank')
        db.commit()

    if request.method == 'POST':
        print(request.data)
        print(request.json)
        data = request.json
        cur = db.execute('SELECT * FROM bank ORDER BY id DESC LIMIT 1')
        entry = cur.fetchall()

        if data:
            summary = data['trans']
            db.execute('INSERT INTO bank (type, trans, sum) VALUES (?, ?, ?)',
                       [data['type'], data['trans'], summary])
            db.commit()

    # cur = db.execute('select * from bank order by id desc')
    cur = db.execute('SELECT * FROM bank ORDER BY id DESC LIMIT 1')
    entries = cur.fetchall()
    data = list()
    for row in entries:
        r = dict()
        r['type'] = row[1]
        r['trans'] = row[2]
        r['sum'] = row[3]
        data.append(r)
    return json.dumps({'records': data})


@app.route('/custom_code/')
def generate_bad_gateway():
    return '', request.args.get('status')


@app.route('/api/large_data/', methods=['GET', 'POST'])
def show_large_data():
    data = list()
    for i in range(1, 1000):
        r = dict()
        r['type'] = i
        r['trans'] = 'trans'
        data.append(r)
    resp = make_response(json.dumps({'records': data}))
    resp.headers["Content-type"] = "application/json"
    return resp


@app.route('/large_data/', methods=['GET'])
def show_large_data2():
    data = list()
    for i in range(1, 1000):
        r = dict()
        r['type'] = i
        r['trans'] = 'trans'
        data.append(r)
    return json.dumps({'records': data})


@app.route('/api/minimal/', methods=['GET'])
def get_min_response():
    return json.dumps({})


@app.route('/api/upload/', methods=['POST'])
def api_upload():
    file_dir = os.path.join(app.root_path, 'upload')
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['upload_file']
    if f:
        f.save(os.path.join(file_dir, f.filename))
        return json.dumps({"msg": "upload succeeded!"})
    else:
        abort(400)


@app.route('/api/upload_with_app/', methods=['POST'])
def api_upload_app():
    file_dir = os.path.join(app.root_path, 'upload')
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    filename = request.headers["filename"]
    print("receive filename:", filename)
    if filename is None:
        return json.dumps({"msg": "no filename!"})
    try:
        with open(os.path.join(file_dir, filename), "w") as f:
            f.write(request.stream.read())
            f.close()
            return json.dumps({"msg": "upload succeeded!"})
        abort(400)
    except Exception as e:
        print(e)
        abort(400)


@app.route('/api/download/<path:filename>')
def api_download(filename):
    dirpath = os.path.join(app.root_path, 'upload')
    if os.path.isfile(os.path.join(dirpath, filename)):
        return send_from_directory('upload', filename, as_attachment=True)
    abort(404)


@app.route("/about/", methods=['GET'])
def show_about():
    return render_template('about.html')

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

@app.route("/detail/", methods=['GET', 'POST'])
def userDetail():
    user = ""
    if request.method == 'GET':
        user = request.args.get("user")
    elif request.method == 'POST':
        if request.form is not None and len(request.form) > 0:
            user = request.form.get("user")

    resp = make_response(json.dumps(userInfo.get(user, ""), ensure_ascii=False))
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp


@app.route("/register/", methods=['GET', 'POST', 'OPTIONS', 'HEAD'])
@app.route("/login/", methods=['GET', 'POST', 'OPTIONS', 'HEAD'])
@app.route("/login", methods=['GET', 'POST', 'OPTIONS', 'HEAD'])
@app.route("/userinfo.do", methods=['GET', 'POST', 'OPTIONS', 'HEAD'])
def register():
    user = ""
    name = ""
    password = ""
    argslist =[]
    if request.method == 'POST':
        try:
            if request.json is not None:
                #请求的Content-Type: application/json
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
                    name = data.getlist("uid")[0]
                    password = data.getlist("passw")[0]
                else:
                    #data为qiqi&123456的情况
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


@app.route(
    "/api/testestestestestestestestestestestestestestestestestestest/test",
    methods=['GET', 'POST'])
def show_long_url_path():
    if request.method == 'GET':
        return json.dumps({'records': 'GET'})
    if request.method == 'POST':
        return json.dumps({'records': 'POST'})


@app.route("/world_languages/", methods=['GET', 'POST', 'OPTIONS', 'HEAD'])
def world_languages():
    if request.method == 'GET':
        resp = render_template('world_languages.html')
    else:
        text = render_template('world_languages.html')
        resp = make_response(text)
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS,HEAD'
        resp.headers["Access-Control-Allow-Headers"] = "x-requested-with,content-type,test-expose-header"
    return resp


@app.route("/inner_page/", methods=['GET', 'POST', 'OPTIONS', 'HEAD'])
def inner_page():
    if request.method == 'GET':
        text = render_template('inner_page.html')
    else:
        text = render_template('inner_page.html')
    resp = make_response(text)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS,HEAD'
    resp.headers["Access-Control-Allow-Headers"] = "x-requested-with,content-type,test-expose-header"
    resp.headers["Access-Control-Expose-Headers"] = "test-expose-header"
    resp.headers["test-expose-header"] = "response-test-expose-header"
    return resp


def test_ajax():
    data = ""
    if request.method == "POST" and request.json and "data" in request.json:
        data = request.json.get("data")
    elif request.method == "GET" and request.args.get("data"):
        data = request.args.get("data")
    resp = make_response(json.dumps({"remoteDataJson": "Ajax request success!", "request_data": data}))
    #resp.headers["Content-Type"] =  "text/html; charset=utf-8"
    resp.headers["Content-Type"] =  "application/json"
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS,HEAD'
    resp.headers["Access-Control-Allow-Headers"] = "x-requested-with,content-type,test-expose-header"
    resp.headers["Access-Control-Expose-Headers"] = "test-expose-header"
    resp.headers["test-expose-header"] = "response-test-expose-header"
    print("ajax",resp)
    return resp


@app.route("/test_ajax/", methods=['GET', 'POST', 'OPTIONS', 'HEAD'])
@gzipped
def test_ajax_all():
    return test_ajax()


@app.route("/test_ajax_get/", methods=['GET', 'OPTIONS', 'HEAD'])
@gzipped
def test_ajax_get():
    return test_ajax()


@app.route("/test_ajax_post/", methods=['POST', 'OPTIONS', 'HEAD'])
@gzipped
def test_ajax_post():
    return test_ajax()


@app.route("/test_jsonp/")
def test_jsonp():
    callback_name = request.args['callback']
    resp = make_response(
        "{0}({1})".format(callback_name, json.dumps({"jsonpData": "Correct jsonp response data from server."})))
    resp.headers["Content-type"] = "application/javascript"
    return resp


@app.route("/test_form/", methods=['GET', 'POST', 'DELETE', 'PUT', 'OPTIONS', "HEAD"])
def test_form():
    data = request.args.to_dict()
    temp = render_template('form_commit.html', redata=data)
    resp = make_response(temp)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS,HEAD'
    resp.headers["Access-Control-Allow-Headers"] = "Origin,x-requested-with,content-type"
    return resp


@app.route("/redirect/", methods=['GET', 'POST'])
def redirect():
    data = dict()
    if request.method == 'GET':
        data = request.args.to_dict()
    if request.method == 'POST':
        try:
            if request.json is not None:
                data = request.json
                data = json.loads(data)
            elif request.form is not None:
                data = request.form
            elif request.values and "location_host" in adictrequest.values:
                data = request.values
            else:
                data = request.data
            print(request.get_data())


        except Exception as e:
            print("Json does not exist!!")
            print(str(e))
            return str(e)

    resp = make_response((json.dumps({'records': data}, ensure_ascii=False), 302))
    resp.headers["Content-type"] = "application/json"
    location_host = data.get('location_host')
    if location_host:
        resp.headers["location"] = "http://{0}/".format(location_host)
    else:
        resp.headers["location"] = "http://{0}/".format(request.host)
    return resp

@app.route("/make_redirect", methods=['GET'])
def make_redirect():
    resp = make_response("302", 302)
    resp.headers["location"] = "http://{0}/make_redirect".format(request.host)
    time.sleep(1)
    #return resp
    return render_template('AutoRefresh.html'), 302

@app.route("/make_reload", methods=['GET'])
def make_reload():
    time.sleep(1)
    #return resp
    return render_template('Reload.html'), 202

@app.route('/mydict', methods=['GET', 'POST'])
def mydict():
    d = {'name': 'xmr', 'age': 18}
    return jsonify(d)


@app.route('/show/j', methods=['GET'])
def show_photo():
    file_dir = 'static/'
    if request.method == 'GET':
        image_data = open(os.path.join(file_dir, '%s' % 'j.jpeg'), "rb").read()
        response = make_response(image_data)
        response.headers['Content-Type'] = 'image/png'
        return response
    abort(404)


@app.route("/hook.html")
def hookHtml():
    return render_template('hook.html')


@app.route("/not_html/")
@app.route("/not_html.html")
def not_html():
    response = make_response("Just text, not the html page.")
    response.headers['Content-Type'] = 'text/plain'
    return response


@app.route("/test_result/", methods=['GET', 'POST'])
def test_result():
    if request.method == "POST":
        db = get_db()
        data = request.json
        if data:
            platform = data.get("platform")
            model = data.get("model")
            sys_version = data.get("sys_version")
            manufacturer = data.get("manufacturer")
            case_name = data.get("case_name")
            result = data.get("result")
            error = data.get("error")
            device_id = data.get("device_id")

            try:
                db.execute(
                    'INSERT INTO test_results (platform, model, sys_version, manufacturer, case_name, result, error, device_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                    [platform, model, sys_version, manufacturer, case_name, result, error, device_id])
                db.commit()
                db.close()
                return json.dumps({'result': True})
            except Exception as e:
                print(e)
                return json.dumps({'result': False})
        else:
            form = request.form
            if form.get('request_type') == "load_results":
                results = []
                cur = db.execute('SELECT * FROM test_results ORDER BY id DESC')
                entry = cur.fetchall()
                for row in entry:
                    re = dict((cur.description[idx][0], v) for idx, v in enumerate(row))
                    results.append(re)
                db.close()
                return json.dumps(results)
            else:
                db.execute('DELETE FROM test_results')
                db.commit()
                db.close()
                return json.dumps({"result": True})

    if request.method == "GET":
        return render_template('test_results.html')

@app.route('/<path>')
def today(path):
    base_dir = os.path.dirname(__file__)
    resp = make_response(open(os.path.join(base_dir, path)).read())
    resp.headers["Content-type"]="text/plan;charset=UTF-8"
    return resp

@app.route('/pac', methods = ['GET'])
def returnpac():
    resp = make_response(open('static/pac').read())
    resp.headers["Content-type"]="text/html;charset=UTF-8"
    return resp

if __name__ == "__main__":
    init_db()
    try:
        a = 0
        if sys.argv:
            for i in sys.argv:
                print(type(sys.argv[a]),"sys.argv[%r] = %r"%(a,i))
                a+=1
            if 1<=int(sys.argv[1])<=65535:
                app.run(host='::', port=sys.argv[1], threaded=True, debug=True)
            else:
                app.run(host='::', port=8089, threaded=True, debug=True)
    except  IndexError as e1:
        print(e1)
        app.run(host='::', port=8089, threaded=True, debug=True)
    except  ValueError as e2:
        print(e2)
        app.run(host='::', port=8089, threaded=True, debug=True)
    
    # server = pywsgi.WSGIServer(('::', 5001), app)
    # server.serve_forever()
