# -*- coding: UTF-8 -*-
import torch.nn as nn
import captcha_setting

# CNN Model (2 conv layer)
class CNN(nn.Module):
    # 定义 Convolution Network 模型。卷积网络模型。
    # #定义CNN Net的初始化函数，这个函数定义了该神经网络的基本结构
    def __init__(self):
        super(CNN, self).__init__() #复制并使用CNN的父类的初始化方法，即先运行nn.Module的初始化函数
        # 函数nn.Sequential()这个表示将一个有序的模块写在一起，也就相当于将神经网络的层按顺序放在一起，这样可以方便结构显示。
        self.layer1 = nn.Sequential(
            # 函数nn.Conv2d()这个是卷积层，里面常用的参数有四个，in_channels, out_channels, kernel_size, stride, padding
            nn.Conv2d(1, 32, kernel_size=3, padding=1), # 定义函数的是图像卷积函数：输入为图像（1个频道，即灰度图）,输出为32张特征图, 卷积核为3x3正方形
            nn.BatchNorm2d(32),
            nn.Dropout(0.5),  # drop 50% of the neuron
            nn.ReLU(),
            nn.MaxPool2d(2)) # 这个是最大池化层
        
        self.layer2 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.Dropout(0.5),  # drop 50% of the neuron
            nn.ReLU(),
            nn.MaxPool2d(2))

        self.layer3 = nn.Sequential(
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.Dropout(0.5),  # drop 50% of the neuron
            nn.ReLU(),
            nn.MaxPool2d(2))

        self.fc = nn.Sequential(
            nn.Linear((captcha_setting.IMAGE_WIDTH//8)*(captcha_setting.IMAGE_HEIGHT//8)*64, 1024),
            nn.Dropout(0.5),  # drop 50% of the neuron
            nn.ReLU())

        self.rfc = nn.Sequential(
            nn.Linear(1024, captcha_setting.MAX_CAPTCHA*captcha_setting.ALL_CHAR_SET_LEN),
        )
        
    #定义该神经网络的向前传播函数，该函数必须定义，一旦定义成功，向后传播函数也会自动生成（autograd）
    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = self.layer3(out)
        out = out.view(out.size(0), -1)
        out = self.fc(out)
        out = self.rfc(out)
        return out

'''
# 1、nn.Sequential()
这个表示将一个有序的模块写在一起，也就相当于将神经网络的层按顺序放在一起，这样可以方便结构显示

# 2、nn.Conv2d()
这个是卷积层，里面常用的参数有四个，`in_channels`, `out_channels`, `kernel_size`, `stride`, `padding`

* in_channels表示的是输入卷积层的图片厚度
* out_channels表示的是要输出的厚度
* kernel_size表示的是卷积核的大小，可以用一个数字表示长宽相等的卷积核，比如kernel_size=3，也可以用不同的数字表示长宽不同的卷积核，比如kernel_size=(3, 2) stride表示卷积核滑动的步长
* padding表示的是在图片周围填充0的多少，padding=0表示不填充，padding=1四周都填充1维

# 3、nn.ReLU()
这个表示使用`ReLU`激活函数，里面有一个参数`inplace`，默认设置为`False`，表示新创建一个对象对其修改，也可以设置为`True`，表示直接对这个对象进行修改

# 4、nn.MaxPool2d() 这个是最大池化层，当然也有平均池化层，里面的参数有`kernel_size`, `stride`, `padding`

* `kernel_size`表示池化的窗口大小，和卷积层里面的 kernel_size是一样的

* `stride`也和卷积层里面一样，需要自己设置滑动步长

* `padding`也和卷积层里面的参数是一样的，默认是0

模型需要传入的参数是输入的图片维数以及输出的种类数
'''