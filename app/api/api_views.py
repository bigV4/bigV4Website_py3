# coding: utf-8
# coding: utf-8
# 将RESTful-api注册为蓝图

from flask import render_template, make_response, request,jsonify
from flask_restful import Api, Resource
from flask import Blueprint

from werkzeug.utils import secure_filename
from app.pytorch_captcha import identify
import base64
import os
import time
from PIL import Image
tmp_api = Blueprint('tmp_api', __name__)

api = Api()

imgfortlist = list(set(['png','jpg','jpeg',"gif","bmp","tif","pcx","tga","exif","fpx","svg","psd","wmf","webp"]))
imgfortlist += [str.upper() for str in imgfortlist]
ALLOWED_EXTENSIONS = set(imgfortlist)
 
# 用于判断文件后缀
def allowed_file(filename):
    return ('.' in filename) and (filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS)

@tmp_api.route('/tmp_api')
class TmpApiResource(Resource):
    def get(self):
        return '/tmp_api'
        pass

@tmp_api.route('/captcha/', methods=['GET','POST'])
@tmp_api.route('/captcha.html', methods=['GET','POST'])
def api_captcha():
    if request.method == 'POST':
        f = request.files['file']
        fname = f.filename
        if not (f and allowed_file(f.filename)):
            return '''<!DOCTYPE html>
            <html lang="en"><head><meta charset="UTF-8"><title>验证码识别</title></head>
                <body><div><a href="/">返回首页</a><br><h3>上传验证码图片，进行识别</h3>
                        <i>Please check the type of image uploaded, only {}</i>
                        <form method="post" action="/captcha/" enctype="multipart/form-data">
                        <input type="file" size="30" name="file" style="margin-top:20px;"/><br>
                        <input type="submit" value="提交图片" class="button-new" style="margin-top:15px;"/>
                        </form></div>
                </body>
            </html>
            '''.format(str(imgfortlist))
        upload_path = os.path.join('static/up_photo/', 'test.png')  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        img = Image.open(upload_path)
        img=img.resize((180,100),Image.ANTIALIAS)
        #img.show()
        print(fname,img.format)
        img.save(upload_path)
        with open(upload_path, 'rb') as ff:  # 以二进制读取图片
            data = ff.read()
            encodestr = base64.b64encode(data) # 得到 byte 编码的数据
            AfterImgBase64 =str(encodestr,'utf-8') # 重新编码数据
        img = Image.open(upload_path)
        (imgW, imgH) = img.size
        identifytext =identify.identify(img)
        return '''<!DOCTYPE html>
        <html lang="en"><head><meta charset="UTF-8"><title>验证码识别</title></head>
            <body><div><a href="/">返回首页</a><br><h3>上传验证码图片，进行识别</h3>
                    <form method="post" action="/captcha/" enctype="multipart/form-data">
                    <input type="file" size="30" name="file" style="margin-top:20px;"/><br>
                    <input type="submit" value="提交图片" class="button-new" style="margin-top:15px;"/>
                    </form></div>
                <h3>提交的文件名是：{fname}</h3>
                <h3>识别的验证码是：{identifytext}！</h3>
                <img src=data:image/png;base64,{AIB64} width="{imgW}" height="{imgH}" alt="你的图片被外星人劫持了～～"/>
            </body>
        </html>
        '''.format(fname=fname,identifytext=identifytext,imgW=imgW,imgH=imgH,AIB64=AfterImgBase64)
 
    return '''<!DOCTYPE html>
        <html lang="en"><head><meta charset="UTF-8"><title>验证码识别</title></head>
            <body><div><a href="/">返回首页</a><br><h3>上传验证码图片，进行识别</h3>
                    <form method="post" action="/captcha/" enctype="multipart/form-data">
                    <input type="file" size="30" name="file" style="margin-top:20px;"/><br>
                    <input type="submit" value="提交图片" class="button-new" style="margin-top:15px;"/>
                    </form></div>
            </body>
        </html>
        '''

@tmp_api.route('/tmp_api/captcha/2/', methods=['GET','POST'])
def api_captcha_2():
    if request.method == 'POST':
        f = request.files['file']
        fname = f.filename
        if not (f and allowed_file(f.filename)):
            return jsonify({"Error": 1001, "msg": "Please check the type of image uploaded, only %s"%".".join(list(imgfortset))})
        upload_path = os.path.join('static/up_photo/', 'test.png')  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        with open(upload_path, 'rb') as ff:  # 以二进制读取图片
            data = ff.read()
            encodestr = base64.b64encode(data) # 得到 byte 编码的数据
            BeforImgBase64 =str(encodestr,'utf-8') # 重新编码数据
        img = Image.open(upload_path)
        (imgW0, imgH0) = img.size
        img=img.resize((180,100),Image.ANTIALIAS)
        imgformat = fname,img.format
        img.save(upload_path)
        with open(upload_path, 'rb') as ff:  # 以二进制读取图片
            data = ff.read()
            encodestr = base64.b64encode(data) # 得到 byte 编码的数据
            AfterImgBase64 =str(encodestr,'utf-8') # 重新编码数据
        img = Image.open(upload_path)
        (imgW1, imgH1) = img.size
        identifytext =identify.identify(img)
        msg = {"Method":"POST",
        "FileName":fname,
        "ImgFormat":imgformat,
        "Identifytext":identifytext,
        "BeforSize":"Height=%spx , Width=%spx"%(imgH0, imgW0),
        "AfterSize":"Height=%spx , Width=%spx"%(imgH1, imgW1),
        "BeforImgBase64":"data:image/%s;base64,%s"%(fname.rsplit('.', 1)[1],BeforImgBase64),
        "AfterImgBase64":"data:image/png;base64,%s"%AfterImgBase64}
        return jsonify(msg)
        '''
        1.将图片转换为Base64编码，可以很方便地在没有上传文件的条件下将图片插入其它的网页、编辑器中。
        2.加入图片在线转base64的结果为"data:image/png;base64,iVBORw0KGgo=..."，那么你只需要全部复制，然后在插入图片的时候，src地址填写这段代码即可。
        3.CSS中使用：background-image: url("data:image/png;base64,iVBORw0KGgo=...");
        4.HTML中使用：src="data:image/png;base64,iVBORw0KGgo=..."
        5.将图片转换成base64编码的，一般用于小图片上，不仅可以减少图片的请求数量（集合到js、css代码中），还可以防止因为一些相对路径等问题导致图片404错误。
        '''
    if request.method == 'GET':
        msg = {"Error": 1002,
        "Method":"GET",
        "Msg":"Does not support the GET method!",
        "Exp.":'curl -F "file=@./75bm_1585469502.png" http://172.16.95.1:8089/tmp_api/captcha/2/'}
        return jsonify(msg)