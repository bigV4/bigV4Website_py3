# coding: utf-8
# coding: utf-8
# 将RESTful-api注册为蓝图

from flask import render_template, make_response, request,jsonify
from flask_restful import Api, Resource
from flask import Blueprint

from werkzeug.utils import secure_filename
from app.pytorch_captcha import identify
import os
import time
from PIL import Image
tmp_api = Blueprint('tmp_api', __name__)

api = Api()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in set(['png', 'jpg', 'JPG', 'PNG'])



@tmp_api.route('/tmp_api')
class TmpApiResource(Resource):
    def get(self):
        return '/tmp_api'
        pass

@tmp_api.route('/tmp_api/captcha/', methods=['GET','POST'])
def api_captcha():
    if request.method == 'POST':
        f = request.files['file']
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "Please check the type of image uploaded, only .png、.PNG、.jpg、.JPG"})
        user_input = request.form.get("name")
        upload_path = os.path.join('static/up_photo/', 'test.jpg')  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        img = Image.open(upload_path)
        (imgH, imgW) = img.size
        infile = './python.jpg'
        outfile = './python_new.jpg'
        img=img.resize((180,100),Image.ANTIALIAS)
        img.save(upload_path)
        identifytext =identify.identify(img)
        return render_template('index.html',userinput=user_input,val1=time.time(),identifytext=identifytext)
 
    return render_template('index.html')