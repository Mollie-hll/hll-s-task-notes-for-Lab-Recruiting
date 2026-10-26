import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

def get_data_loaders(batch_size=64):
    #定义数据预处理：
    transform = transforms.Compose([
        transforms.ToTensor(),#将图片(28x28)转为张量，并把像素值从 0-255 压缩到 0-1 之间
        transforms.Normalize((0.1307,), (0.3081,))#使用 MNIST 的全局均值和标准差进行标准化，让模型更好收敛
    ])

    #自动下载并加载训练集
    train_dataset = datasets.MNIST(
        root='./data',
        train=True,
        download=True,
        transform=transform
    )

    #自动下载并加载测试集，防止过拟合
    test_dataset = datasets.MNIST(
        root='./data',
        train=False,
        download=True,
        transform=transform
    )

    #使用DataLoader将数据分批次打包
    train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, test_loader

if __name__ == '__main__':
    #测试数据加载是否正常
    train_l, test_l = get_data_loaders()
    print(f"训练集批次数量: {len(train_l)}")
    print(f"测试集批次数量: {len(test_l)}")
