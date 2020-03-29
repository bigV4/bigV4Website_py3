# -*- coding: UTF-8 -*-
from captcha.image import ImageCaptcha  # pip install captcha
from PIL import Image
import random
import time
import captcha_setting
import os
import shutil

def random_captcha():
    captcha_text = []
    for i in range(captcha_setting.MAX_CAPTCHA):# MAX_CAPTCHA每个验证码最大字符数
        c = random.choice(captcha_setting.ALL_CHAR_SET)
        captcha_text.append(c)
    return ''.join(captcha_text) # 列表并成字符串

# 生成字符对应的验证码
def gen_captcha_text_and_image():
    image = ImageCaptcha()
    captcha_text = random_captcha()
    captcha_image = Image.open(image.generate(captcha_text))
    return captcha_text, captcha_image

def main():
    count = 2000000 #生成训练用的验证码数量
    path = captcha_setting.TRAIN_DATASET_PATH    #通过改变此处目录，以生成 训练、测试和预测用的验证码集

    try:
        print(os.path.exists(path)) # 文件夹不存在，返回False。文件夹存在，返回Ture。
        if len(os.listdir(path)) > 2000000:
            print(len(os.listdir(path)))
            geshu = len(os.listdir(path))
            for i in range(0,geshu-2000000):
                os.remove(os.listdir(path)[i]) 
        #shutil.rmtree(path)  #清空指定文件夹下所有文件并删除了该文件夹
        print(len(os.listdir(path)))
    except Exception as e:
        os.makedirs(path)
        pass
    print(len(os.listdir(path))) #文件夹下无文件，返回0
    for i in range(0, count):
        now = str(int(time.time()))
        text, image = gen_captcha_text_and_image()
        filename = text+'_'+now+'.png'
        image.save(path  + os.path.sep +  filename)
        print('saved %d : %s  to  %s' % (i+1,filename,path))

if __name__ == '__main__':
    main()