import torch.nn as nn
import torch.nn.functional as F

class MyMLP(nn.Module):
    def __init__(self):
        super(MyMLP, self).__init__()
        self.fc1 = nn.Linear(28 * 28, 256)#输入层：784个像素
        self.fc2 = nn.Linear(256, 128)#隐藏层
        self.fc3 = nn.Linear(128, 10)#输出层

    def forward(self, x):
        x = x.view(-1, 28 * 28)#将二维图片拉平
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x