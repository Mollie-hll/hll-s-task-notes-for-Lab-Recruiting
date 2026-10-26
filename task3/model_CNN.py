import torch.nn as nn
import torch.nn.functional as F


class MyCNN(nn.Module):
    def __init__(self):
        super(MyCNN, self).__init__()
        #第1层卷积：输入通道1(灰度图)，输出通道16，卷积核大小3x3
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, padding=1)
        #第2层卷积：输入通道16，输出通道32，卷积核大小3x3
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, padding=1)

        #最大池化层：窗口大小2x2
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

        #全连接层：28x28经过两次2x2池化后，尺寸变为7x7；展平后的特征维度是32(通道数)*7*7
        self.fc1 = nn.Linear(32 * 7 * 7, 128)
        #输出层：10个类别（0-9）
        self.fc2 = nn.Linear(128, 10)

        #Dropout层：防止过拟合（随机丢弃 25% 的神经元）
        self.dropout = nn.Dropout(0.25)

    def forward(self, x):
        #前向传播：手动将各层连接起来
        #1.卷积->ReLU激活->池化
        x = self.pool(F.relu(self.conv1(x)))#此时尺寸：14x14
        #2.卷积->ReLU激活->池化
        x = self.pool(F.relu(self.conv2(x)))#此时尺寸：7x7
        #3.展平操作：将多维张量拉平成一维向量，以便输入全连接层
        x = x.view(-1, 32 * 7 * 7)
        #4.全连接->ReLU->Dropout->全连接输出
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)

        return x