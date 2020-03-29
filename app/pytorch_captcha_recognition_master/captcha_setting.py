# -*- coding: UTF-8 -*-
import os
# 验证码中的字符
# string.digits + string.ascii_uppercase
NUMBER = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
ALPHABET_L = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

ALL_CHAR_SET = NUMBER + ALPHABET + ALPHABET_L
ALL_CHAR_SET_LEN = len(ALL_CHAR_SET)
MAX_CAPTCHA = 4 # 每个验证码最大字符数

# 样本大小
TRAIN_DATASET_SIZE = 20000 # 创建训练用的验证码数量
TEST_DATASET_SIZE = 2000 # 创建测试识别率用的验证码数量
PREDICT_DATASET_SIZE = 100 # 创建预测用的验证码数量

# 图像大小
IMAGE_HEIGHT = 60
IMAGE_WIDTH = 160
PATH_SEPARATOR = os.path.sep
TRAIN_DATASET_PATH = 'dataset' + PATH_SEPARATOR + 'train'
TEST_DATASET_PATH = 'dataset' + PATH_SEPARATOR + 'test'
PREDICT_DATASET_PATH = 'dataset' + PATH_SEPARATOR + 'predict'