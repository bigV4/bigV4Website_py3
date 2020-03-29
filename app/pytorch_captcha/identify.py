# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 20:07:17 2019

@author: icetong
"""

import torch
import torch.nn as nn
from torchvision.transforms import Compose, ToTensor
try:
    from models import CNN
except ModuleNotFoundError as e:
    from app.pytorch_captcha.models import CNN
from PIL import Image

model_path = 'data/model.pth'

source = [str(i) for i in range(0, 10)]
source += [chr(i) for i in range(97, 97+26)]
alphabet = ''.join(source)

def identify(img):
    img = img.convert('RGB')
    transforms = Compose([ToTensor()])
    img = transforms(img)
    cnn = CNN()
    if torch.cuda.is_available():
        cnn = cnn.cuda()
    cnn.eval()
    cnn.load_state_dict(torch.load(model_path))
    if torch.cuda.is_available():
        img = img.view(1, 3, 100, 180).cuda()
    else:
        img = img.view(1, 3, 100, 180)
    output = cnn(img)    
    output = output.view(-1, 36)
    output = nn.functional.softmax(output, dim=1)
    output = torch.argmax(output, dim=1)
    output = output.view(-1, 4)[0]
    return ''.join([alphabet[i] for i in output.cpu().numpy()])