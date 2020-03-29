# -*- coding: UTF-8 -*-
'''
用于生成训练用的验证码图片
'''
from captcha.image import ImageCaptcha  # pip install captcha
from PIL import Image
import random
import time
import captcha_setting
import os
import shutil


def random_captcha():
    # 生成随机的验证码字符
    captcha_text = []
    for i in range(captcha_setting.MAX_CAPTCHA):  # MAX_CAPTCHA每个验证码最大字符数
        c = random.choice(captcha_setting.ALL_CHAR_SET)
        captcha_text.append(c)
    return ''.join(captcha_text)  # 列表并成字符串


def gen_captcha_text_and_image():
    # 生成字符对应的验证码
    image = ImageCaptcha()
    captcha_text = random_captcha()
    captcha_image = Image.open(image.generate(captcha_text))
    return captcha_text, captcha_image


def main():
    count = captcha_setting.TRAIN_DATASET_SIZE   # 生成训练用的验证码数量
    path = captcha_setting.TRAIN_DATASET_PATH    # 此处目录，以生成训练用的验证码集
    separator = captcha_setting.PATH_SEPARATOR   # 路径分隔符
    if os.path.exists(path):
        print(len(os.listdir(path)))
        existinglist = os.listdir(path)
        existinglistsize = len(existinglist)
        rmlist = random.sample(existinglist, int(existinglistsize/4)) # 随机删除四分之一的图片
        for i in rmlist:
            try:
                os.remove(str(path)+str(os.path.sep)+str(i)) # 随机删除四分之一的图片
            except Exception as e:
                print(e)
        if len(os.listdir(path)) > count:
            for n in range(0,count-len(os.listdir(path))):
                os.remove(os.listdir(path)[n]) # 删除超出count数量的图片
        # shutil.rmtree(path)  # 清空指定文件夹下所有文件并删除了该文件夹
    else:
        os.makedirs(path)
        pass
    existinglistsize = len(os.listdir(path))
    print(existinglistsize)  # 文件夹下现有文件数量
    for i in range(0, count-existinglistsize):
        now = str(int(time.time()))
        text, image = gen_captcha_text_and_image()
        filename = text+'_'+now+'.png'
        image.save(path + os.path.sep + filename)
        Remaining = count-existinglistsize-i-1
        print('saved %d : %s  to  \'%s%s\'  !  Remaining: %r ' % (i+1, filename, path, separator, Remaining))
    print(len(os.listdir(path)))

if __name__ == '__main__':
    main()
