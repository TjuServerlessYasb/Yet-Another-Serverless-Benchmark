import torch
import torch_npu
import torchvision.models as models
import time
import torch.nn as nn


start_time = time.time() 
device = "npu:1"
# 加载预训练的ResNet50模型
model = models.resnet50(pretrained=False).to(device)
# 将模型设置为评估模式
model.eval()
# 这里创建的是一个批次大小为1的模拟输入
inputs = torch.randn(200, 3, 224, 224).to(device)
# 使用NPU执行一次前向推理
with torch.no_grad():
    for i in range(300):
        start_time = time.time() 
        outputs = model(inputs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Iteration {i+1}, Execution Time: {elapsed_time:.6f} seconds")
