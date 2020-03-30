# -*- coding: UTF-8 -*-
# 训练模型
import torch
import torch.nn as nn
from torch.autograd import Variable
import my_dataset
from captcha_cnn_model import CNN
import captcha_setting

# Hyper Parameters
num_epochs = 200 # step不能大于num_epochs。也许num_epochs是训练次数的上限，而steps是实际训练次数。
batch_size = 128 # 训练样本的子集大小（例如1000个样本中的100个），该样本将用于在学习过程中训练网络。针对所有样本的一次迭代
learning_rate = 0.001 # 学习率作为监督学习以及深度学习中重要的超参，其决定着目标函数能否收敛到局部最小值以及何时收敛到最小值。

def main():
    cnn = CNN()
    use_gpu = torch.cuda.is_available()  # 判断是否有GPU加速
    print("torch.cuda.is_available() use_gpu: %s"%use_gpu)
    if use_gpu:
        cnn = cnn.cuda()
    cnn.train()
    print('init net')
    criterion = nn.MultiLabelSoftMarginLoss()
    optimizer = torch.optim.Adam(cnn.parameters(), lr=learning_rate)

    # Train the Model
    train_dataloader = my_dataset.get_train_data_loader()
    for epoch in range(num_epochs):
        for i, (images, labels) in enumerate(train_dataloader):
            images = Variable(images)
            labels = Variable(labels.float())
            predict_labels = cnn(images)
            loss = criterion(predict_labels, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            if (i+1) % 10 == 0:
                print("epoch:", epoch, "step:", i, "loss:", loss.item())
                print("epoch:%s step:%s loss:%s")
            if (i+1) % 100 == 0:
                torch.save(cnn.state_dict(), "./captcha_%s_model.pkl"%captcha_setting.MAX_CAPTCHA)   #current is model.pkl
                print("save model")
        print("epoch:", epoch, "step:", i, "loss:", loss.item())
    torch.save(cnn.state_dict(), "./captcha_%s_model.pkl"%captcha_setting.MAX_CAPTCHA)   #current is model.pkl
    print("save last model")

if __name__ == '__main__':
    main()


'''
e_poch:
首先，我们把让计算机进行”学习“的过程称为训练，联想到训练动物进行杂技表演，只练一次是不会达到目的的，因此我们会训练很多次，每一次训练，称为一次e_poch。
具体进行几轮训练，需要我们人为地进行规定，一般根据经验和模型的反馈进行调整.

batch_size：
计算机的计算能力很强，我们一次只传入一张图片实在太过寒酸，计算机资源无法得到有效利用。因此，我们每次向网络中传入batch_size张图片，这样不仅更大的利用计算机的资源，还让计算机更好地对图像特征进行分析。
其具体数值地大小，需要我们人为地进行设置，一般根据经验和模型的反馈进行调整.

宽度和高度：
我们进行图片识别时，传入神经网络的是图片，既然是图片，那么就会有尺寸，即为图片的宽度和高度，这其实就是图片的像素大小，我们右键图片，在属性中的详细信息就可以查看，如下图：
针对这张图片，我们将其理解成由100*38个像素点构成的，每一个点上都包含着图片的信息（主要是颜色），这个信息就是图片的特征，我们神经网络的自变量即为这个特征的倍数，卷积神经网络中卷积、池化、全连接均涉及特征维度的运算，即涉及对尺寸的修改。

channels：
翻译为通道数，我们进行图片识别时，传入神经网络的图片是(R,G,B)(R,G,B)(R,G,B)三通道的，我将其理解为三张图片叠在一起。
而只有卷积运算涉及通道层面，卷积运算通过卷积核与图片做Hadamard乘积，将图片的通道数增加，提升计算机对图片特征的辨识能力。因此，对于我们的项目，卷积神经网络第一层卷积的in_channel，即输入的通道数一定为3。
out_channel即为经过这一层卷积运算希望得到的通道数，这个参数只能靠经验和模型的反馈进行设置；同时，第 n−1n-1n−1 层卷积的out_channel一定等于第 nnn 层的in_channel。

kernel_size
意为卷积（池化）核的尺寸，通常设置为一个数是因为默认卷积核为方阵，我们也可以指定其为(M∗N)(M*N)(M∗N)的矩阵。
其具体数值地大小，需要我们人为地进行设置，一般根据经验和模型的反馈进行调整

stride
意为卷积（池化）核每进行一次运算后移动的步长。
其具体数值地大小，需要我们人为地进行设置，一般根据经验和模型的反馈进行调整

padding
意为在特征图边框补零的个数，通常设置为一个数是默认各边补一样多个数。
其具体数值地大小，需要我们人为地进行设置，一般根据经验和模型的反馈进行调整
经历卷积、池化后图片的尺寸计算公式：

'''