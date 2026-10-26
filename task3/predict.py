import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
import torch
import matplotlib.pyplot as plt
from torchvision import datasets, transforms
from model_CNN import MyCNN
import random


def predict_single_image():
    device = torch.device("cpu")#设置设备为 CPU
    model = MyCNN().to(device) #实例化模型
    model.load_state_dict(torch.load('mnist_model.pth', map_location=device))#加载保存的“大脑”参数
    model.eval()  #设置为评估模式

    #加载测试集数据
    transform = transforms.Compose([transforms.ToTensor()])
    test_dataset = datasets.MNIST(root='./data', train=False, download=True, transform=transform)

    #随机挑一张图片
    random_idx = random.randint(0, len(test_dataset) - 1)
    image, true_label = test_dataset[random_idx]

    #输入图片进行预测
    image_input = image.unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(image_input)
        _, predicted_label = torch.max(output.data, 1)# 取出概率最大的那个类别的索引

    predicted_label = predicted_label.item()

    #画出图片
    plt.imshow(image.squeeze(), cmap='gray')
    plt.title(f"True Label: {true_label} | Predicted: {predicted_label}")
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    predict_single_image()