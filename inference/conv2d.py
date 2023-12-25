
# import time
# time.sleep(50)
import torch
print(torch.__version__)
# 确保CuDNN不会被使用
torch.backends.cudnn.enabled = False
# 检查是否有可用的 GPU，如果有，则使用它
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 创建 Conv2d 层并将其移动到 GPU
conv1 = torch.nn.Conv2d(3, 3, 3, stride=(1, 1), padding=(1, 1), bias=False).to(device)

# 创建输入张量并将其移动到 GPU
inp = torch.randn(1, 3, 5, 5).to(device)

# 在 GPU 上执行前向传播
a = conv1(inp)

# 将输出从 GPU 移回 CPU 并打印
print(a.cpu())
