# -*- coding: UTF-8 -*-
import os
import shutil
import time
from captcha.image import ImageCaptcha  # pip install captcha
from torch.utils.data import DataLoader,Dataset
import torchvision.transforms as transforms
from PIL import Image
import one_hot_encoding as ohe
import captcha_setting
import random

class mydataset(Dataset):
    def creattestpng(self,folder):
        for i in range(1000):
                now = str(int(time.time()))
                captcha_text = []
                for i in range(captcha_setting.MAX_CAPTCHA):# MAX_CAPTCHA每个验证码最大字符数
                    c = random.choice(captcha_setting.ALL_CHAR_SET)
                    captcha_text.append(c)
                captcha_text_str = ''.join(captcha_text)
                image = ImageCaptcha()
                text = captcha_text_str
                captcha_image = Image.open(image.generate(captcha_text))
                filename = text+'_'+now+'.png'
                captcha_image.save(folder  + os.path.sep +  filename)
                print('saved %d : %s  to  %s' % (i+1,filename,folder ))

    def __init__(self, folder, transform=None):
        try:
            print(os.path.exists(folder))
            shutil.rmtree(folder)  #清空指定文件夹下所有文件并删除了该文件夹
            print(len(os.listdir(folder)))
        except Exception as e:
            os.makedirs(folder)
            pass
        self.creattestpng(folder)
        print(len(os.listdir(folder))) #文件夹下无文件，返回0
        self.train_image_file_paths = [os.path.join(folder, image_file) for image_file in os.listdir(folder)]
        self.transform = transform

    def __len__(self):
        return len(self.train_image_file_paths)

    def __getitem__(self, idx):
        image_root = self.train_image_file_paths[idx]
        image_name = image_root.split(os.path.sep)[-1]
        image = Image.open(image_root)
        if self.transform is not None:
            image = self.transform(image)
        label = ohe.encode(image_name.split('_')[0]) # 为了方便，在生成图片的时候，图片文件的命名格式 "4个数字或者数字_时间戳.PNG", 4个字母或者即是图片的验证码的值，字母大写,同时对该值做 one-hot 处理
        #print(label)
        return image, label

transform = transforms.Compose([
    # transforms.ColorJitter(),
    transforms.Grayscale(),
    transforms.ToTensor(),
    # transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
def get_train_data_loader():

    dataset = mydataset(captcha_setting.TRAIN_DATASET_PATH, transform=transform)
    return DataLoader(dataset, batch_size=64, shuffle=True)

def get_test_data_loader():
    dataset = mydataset(captcha_setting.TEST_DATASET_PATH, transform=transform)
    return DataLoader(dataset, batch_size=1, shuffle=True)

def get_predict_data_loader():
    dataset = mydataset(captcha_setting.PREDICT_DATASET_PATH, transform=transform)
    return DataLoader(dataset, batch_size=1, shuffle=True)