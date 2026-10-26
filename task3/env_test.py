import torch
import torchvision
import sys

print("当前 Python 路径:", sys.executable)
print("PyTorch 版本:", torch.__version__)
print("torchvision 版本:", torchvision.__version__)
print("CUDA 可用:", torch.cuda.is_available())