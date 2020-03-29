import torch
import torchvision
#import tensorboard
import numpy
import matplotlib.pyplot as plot
from alphabet import alphabet
from PIL import Image
from torch import nn,optim
from torchvision import datasets
from torchvision import transforms
from torch.utils.data import DataLoader,Dataset
import os
import sys
import re
'''
https://blog.csdn.net/namespace_Pt/article/details/104488258
'''
def preprocessing():

    #声明图片路径
    dir_train = 'data/train/'
    dir_test = 'data/test/'

    #列出所有图片的名字
    fileDist_train = os.listdir(dir_train)
    fileDist_test = os.listdir(dir_test)

    train = open('dists/train.txt','a')                   #a为追加模式
    test = open('.dists/test.txt','a')                     

    for file in fileDist_train:
        #取qwqwqw_20121218281.png前的部分，作为标签，将路径和标签中间隔一个空格后逐行写入.txt文件中
        name = dir_train + file + ' ' + re.split('_',file)[0] + '\n'
        train.write(name)

    for file in fileDist_test:
        name = dir_test + file + ' ' + re.split('_',file)[0] + '\n'
        test.write(name)

    test.close()
    train.close()


#定义loader，需要将图片转换成RGB三通道的模式
def default_loader(path):
    return Image.open(path).convert('RGB')

def myEncode(string):
    #string为验证码
    result = []
    for char in string:
        #对每一位验证码，创造一个26位均为0的列表，将其在字母表中对应的位置改为1
        vec = [0] * 26
        vec[ord(char) - 97] = 1
        #每一位验证码都对应这样一个仅有一位为1的列表，将这些列表连在一起，成为最终26*4的一维数组，之后转换成tensor
        result += vec
    return result

def myDecode(pred,label):
    #每次传入的是尺寸为[1,4*26]的tensor,这里先将其转为每行26列的形式，即每行代表一个字母
    pred,label = pred.view(-1,26),label.view(-1,26)
    #得到每一行最大的数的列序号，即得到这一行代表的字母;注意转换成cpu()形式后再转为numpy数组，这样才能解码  
    pred = torch.argmax(pred,dim=1).cpu().numpy()
    label = torch.argmax(label,dim=1).cpu().numpy()
    #创建空字符串
    pre_str = ''
    tar_str = ''
    #把每一行的数字转换为字母
    for pre_num,tar_num in zip(pred,label):
        #97是'a'的ascii值,用chr()方法得到对应字母,加入预测码和真实码的字符串中
        pre_str += chr(pre_num+97)
        tar_str += chr(tar_num+97)
    #这样就得到了一对预测验证码和真是验证码
    return pre_str,tar_str        

def getAcc(pred,label):
    #每次神经网络的输出和标准的验证码尺寸均为[batch_size,26*4],这里先将其转为每行26列的形式，即每行代表一个字母
    pred,label = pred.view(-1,26),label.view(-1,26)

    #pred = nn.functional.softmax(pred,dim=1)  
               
    #得到每一行最大的数的列序号，即得到这一行代表的字母    
    pred = torch.argmax(pred,dim=1)                         
    label = torch.argmax(label,dim=1)

    #再转为一行四个字母，即一行代表一个验证码                      
    pred,label = pred.view(-1,4),label.view(-1,4)
    #记录是否正确的列表
    correct_list = []
    
    for i in range(pred.size(0)):

        #如果有pred和label的相应行相等，代表四个字母都相同，验证码预测正确
        if torch.equal(pred[i],label[i]):
            correct_list.append(1)

        #反之错误
        else:
            correct_list.append(0)

    #计算正确率
    acc = sum(correct_list)/len(correct_list)
    
    return acc

class MyDataset(Dataset):
    #初始化，transform缺省为None
    def __init__(self,txt,transform=None,target_transform=None,loader=default_loader):
        #先调用基类的__init__()方法
        super().__init__()
        #创建空列表
        imgs = []
        with open(txt,'r') as f:
            #逐行读入.txt文件内容
            for line in f:
                #去除末尾的换行符
                line = line.rstrip('\n')
                #找到路径和标签间隔的空格，将字符串一分为二，前者为图片路径，后者为标签
                attrs = line.split(' ')
                #编码
                label = myEncode(attrs[1].lower())
                #加入列表
                imgs.append((attrs[0],label))
        #添加属性，这里的imgs是元组构成的列表，每一个元组有两个元素，前者为图片路径，后者为编码后的标签
        self.imgs = imgs        
        #添加属性                            
        self.transform = transform
        #添加属性
        self.target_transform = target_transform
        #添加属性
        self.loader = loader
        
    def __getitem__(self,index):
        #分别取得图片路径和标签
        src,label = self.imgs[index]
        #加载图片
        img = self.loader(src)
        #在取出图片时根据设定的transform方式进行预变换
        if self.transform is not None:                      
            img = self.transform(img)
        #在取出图片时根据设定的target_transform方式进行预变换
        if self.target_transform is not None:
            label = self.target_transform(label)
        return img,torch.tensor(label)

    def __len__(self):
        #数据集的长度即为imgs的长度
        return len(self.imgs)

#定义预变换
tf = transforms.Compose([
    transforms.ToTensor()                                   
])

#调用类进行数据存入
data_train = MyDataset('dists/train.txt',transform=tf)
data_test = MyDataset('dists/test.txt',transform=tf)

batch_size = 64
train_loader = DataLoader(data_train,batch_size=batch_size,shuffle=True)
test_loader = DataLoader(data_test,batch_size=batch_size,shuffle=False)

class CNN(nn.Module):
    def __init__(self):
        #先调用父类的__init__()方法
        super().__init__()
        #####ORIGINAL-----batch_size * channels * width * height = 64*3*100*38-----#####
        self.net = nn.Sequential(
            nn.Conv2d(3,16,kernel_size=3,padding=(1,1)),nn.MaxPool2d(kernel_size=2,stride=2),nn.BatchNorm2d(16),nn.ReLU(),
            #batch_size * channels * width * height = 64*16*50*19
            nn.Conv2d(16,64,kernel_size=3,padding=(1,1)),nn.MaxPool2d(kernel_size=2,stride=2),nn.BatchNorm2d(64),nn.ReLU(),
            #batch_size * channels * width * height = 64*64*25*9
            nn.Conv2d(64,512,kernel_size=3,padding=(1,1)),nn.MaxPool2d(kernel_size=2,stride=2),nn.BatchNorm2d(512),nn.ReLU()
            #batch_size * channels * width * height = 64*512*12*4
        )
        
        self.fc = nn.Sequential( 
            #这里只传入channels*width*height
            #全连接层得到的应该是最终的分类数，验证码每个位置有四种可能，符合加法原理
            nn.Linear(512*12*4,26*4)
        )
            
    def forward(self,x):
        #先进行卷积和池化
        x = self.net(x)
        #将tensor展成一维
        x = x.view(-1,512*12*4)
        #全连接
        x = self.fc(x)
        return x       

def train():
    #定义模型
    model = CNN()
    if torch.cuda.is_available():
        #转移到gpu，加速运算
        model = model.cuda()
    #采用pytorch自带的多标签多分类的损失函数
    lossFunc = nn.MultiLabelSoftMarginLoss()       
    #采用Adam算法进行权重参数的调整            
    optimizer = optim.Adam(model.parameters())
    #训练60波
    for e_poch in range(1,60):
        #开启训练模式，激活BatchNorm2d函数
        model.train()
        #每一波训练的loss值
        loss_train = 0.0

        loss_test = 0.0
        acc_train = 0.0
        acc_test = 0.0

        #每一波训练的总图片数
        count = 0

        #从train_loader即Dataloader中加载数据
        for each in train_loader:
            #因定义的时候是元组，这里也要分别取出元组的元素
            img = each[0]
            label = each[1]
            #转移到gpu上
            if torch.cuda.is_available():
                img = img.cuda()
                label = label.cuda()
            
            #前向传播，这里隐式调用了forward()方法，输出尺寸是[batch_size,26*4]
            out = model(img)
            #计算loss
            loss = lossFunc(out,label)  
            #将梯度置0                           
            optimizer.zero_grad()
            #后向传播
            loss.backward()
            #用Adam算法优化权重参数
            optimizer.step()

            accuracy = getAcc(out,label)

            #总loss
            loss_train+=loss
            acc_train += accuracy

            #总图片数
            count += 1
        #每进行一波训练，打印一次    
        print('e_poch:{},loss_train:{:.4},acc_train:{:.4}'.format(e_poch,loss_train/count,acc_train/count)) 

        #记录每一波训练的图片总数    
        count = 0
        #进入测试模式,关闭BatchNorm2d.
        model.eval()
        #加载测试集中数据，一次加载batch_size张图片
        for each in test_loader:
            #因定义的时候是元组，这里也要分别取出元组的元素
            img = each[0]
            label = each[1]

            if torch.cuda.is_available():
                #转移到gpu
                img = img.cuda()
                label = label.cuda()
            
            #前向传播
            out = model(img)
            #计算loss
            loss = lossFunc(out,label)
            #计算准确率
            accuracy = getAcc(out,label)
            #一波训练总loss
            loss_test+=loss
            #一波训练总准确率
            acc_test += accuracy
            #更新图片个数
            count += 1
        #输出这一波训练的平均loss和平均准确率
        print('e_poch:{},loss_test:{:.4},acc_test:{:.4}'.format(e_poch,loss_test/count,acc_test/count)) 
        torch.save(model,'dists/modules/code_recognition_vruc.pth')  

def test():
    count = 0
    accuracy = 0
    acc_test = 0
    model = torch.load('dists/modules/code_recognition_vruc.pth')


    for each in test_loader:
        img = each[0]
        label = each[1]

        if torch.cuda.is_available():
            img = img.cuda()
            label = label.cuda()
                
        out = model(img)
        accuracy = getAcc(out,label)

        acc_test += accuracy
        count += 1

    print('acc_test:{:.4}'.format(acc_test/count)) 

def predict_visibal():
    #加载模型
    cnn = torch.load('dists/modules/code_recognition_vruc.pth')
    cnn.dump_patches = True
    #每次加载batch_size张图片tensor
    for each in test_loader:
        #分别取元组的第一、第二个元素作为图片和标签
        imgs,labels = each[0],each[1]
        #转移到gpu
        if torch.cuda.is_available():
            imgs = imgs.cuda()
            labels = labels.cuda()
        #前向传播
        preds = cnn(imgs)
        #将batch_size个tensor分开进行可视化和解码
        for i in range(1,batch_size):
            #用permute方法改变tensor的维度顺序，从batch_size*channels*width*height转为batch_size*width*height*channels
            #取四维数组的第一维第i个元素，即width*height*channels得图片，并将其转移到cpu上后转换为numpy数组
            plot.imshow(imgs.permute((0,2,3,1))[i].cpu().numpy())
            #显示图片
            plot.show()
            #解码
            pre_str,tar_str = myDecode(preds[i],labels[i])
            #打印
            print('pre_str:{}||tar_str:{}'.format(pre_str,tar_str))

preprocessing()
train()
test()