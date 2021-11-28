from flask import Flask
from flask import render_template  # 引入方法

# 默认静态文件目录为static
app = Flask(__name__)  # 创建Flask对象，把当前文件名作为参数传入。


@app.route('/')  # 注册路由
def hello_world():
    return 'Hello World!'


@app.route('/feedback.jsp')  # 注册路由
def feedback():
    return '''<html>

<head>
<meta charset="utf-8">
<title>一个简单的测试页面</title>
</head>

<body style="background-color:#00E090;">
<h1>一个简单的测试页</h1>
<p>一个简单的测试页</p>
</body>

</html>'''


@app.route('/index/<string:name>/<int:page>')
def index(name: str, page: int) -> str:
    return "name:{} page:{}".format(name, page)


@app.route('/page/<string:name>')
def page():
    # homepage.html在static文件夹下
    return app.send_static_file('/htdocs/homepage.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088)  # 框架运行，请求来，执行__call__方法
