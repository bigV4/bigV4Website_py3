# --** coding="UTF-8" **--
# 
# author:SueMagic  time:2019-01-01
import os
import re
import sys
import time
    
def cheagename(path):  
    # 输出此文件夹中包含的文件名称
    fileList = os.listdir(path)
    print("修改前：\n" + str(fileList))
    num = 1
    # 遍历文件夹中所有文件
    for fileName in fileList:
        now = str(int(time.time()))
        # 匹配文件名正则表达式
        pat = "^[A-Za-z0-9]{3,9}\.(png|jpg|jepg|gif)$"
        # 进行匹配
        pattern = re.findall(pat, fileName)
        # 文件重新命名
        beforname = path+"/"+ fileName
        aftername = path+"/"+ fileName.split('.')[0]+ '_' + now + '.' + fileName.split('.')[1]
        os.rename(beforname, (aftername))
    print("***************************************")
    # 刷新
    sys.stdin.flush()
    fileList = os.listdir(path)
    # 输出修改后文件夹中包含的文件名称
    print("修改后：\n" + str(fileList))

cheagename("data/test")
cheagename("data/train")