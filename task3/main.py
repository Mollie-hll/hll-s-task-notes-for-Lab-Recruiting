import torch
import torch.nn as nn
import torch.optim as optim
from data import get_data_loaders
from model_MLP import MyMLP


def train_and_test():
    #超参数设置
    batch_size = 64
    learning_rate = 0.001
    epochs = 3  #训练轮数（3轮基本就能达到98%以上的准确率）

    #检查有无GPU可用
    device = torch.device("cpu")
    print(f"当前使用的计算设备: {device}")

    #加载数据
    train_loader, test_loader = get_data_loaders(batch_size)

    #实例化模型，并移动到对应设备上
    model = MyMLP().to(device)

    #定义损失函数（交叉熵）和优化器（Adam）
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    #训练模型
    print("\n--- 开始训练 ---")
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0

        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.to(device), target.to(device)
            optimizer.zero_grad()#清空上一轮的梯度
            output = model(data)#前向传播：输入图片，得到预测结果
            loss = criterion(output, target)#计算损失
            loss.backward()#反向传播：计算梯度
            # 更新参数
            optimizer.step()
            running_loss += loss.item()
            #打印进度
            if batch_idx % 300 == 299:
                print(
                    f"[Epoch {epoch + 1}/{epochs}, Batch {batch_idx + 1}/{len(train_loader)}] 当前 Loss: {running_loss / 300:.4f}")
                running_loss = 0.0

    #开始测试
    print("\n--- 开始测试 ---")
    model.eval()  # 设置为评估模式（关闭 Dropout）
    correct = 0
    total = 0

    #测试时不需要计算梯度，关闭梯度计算可以加速并节省内存
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)

            outputs = model(data)#前向传播得到结果

            _, predicted = torch.max(outputs.data, 1)#取概率最大的类别的索引作为预测结果

            total += target.size(0)#统计总数
            correct += (predicted == target).sum().item()#统计预测正确的数量

    #计算最终准确率
    accuracy = 100 * correct / total
    print(f"\n")
    print(f"模型在测试集上的准确率: {accuracy:.2f}%")
    print(f"\n")

    #保存模型参数
    torch.save(model.state_dict(), 'mnist_model.pth')
    print("模型已保存为： mnist_model_CNN.pth")

if __name__ == '__main__':
    train_and_test()