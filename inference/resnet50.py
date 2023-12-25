import torch
import torch.nn as nn
import torchvision.models as models
import torch.optim as optim
import time



# 确保CuDNN不会被使用
torch.backends.cudnn.enabled = False

# 检查GPU是否可用
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)
# 创建一个预训练的ResNet50模型
model = models.resnet50(pretrained=False).to(device)

# 创建一些模拟数据
# 假设我们有一个小批量的3通道图像，大小为224x224
batch_size = 3
dummy_input = torch.randn(batch_size, 3, 224, 224).to(device)
dummy_output = torch.randn(batch_size, 1000).to(device)  # 1000是ResNet50的输出维度

# 加载模型
model_loaded = models.resnet50()
model_loaded.load_state_dict(torch.load('resnet50_no_cudnn.pkl'))

# print(model_loaded)

model_loaded = model_loaded.to(device)

# 在GPU上进行一次推理
model_loaded.eval()
with torch.no_grad():
    test_input = torch.randn(batch_size, 3, 224, 224).to(device)
    # 开始计时
    start_time = time.time()
    test_output = model_loaded(test_input)
    # 结束计时
    end_time = time.time()
    print(test_output)
    # 打印推理时间
    print(f"推理执行时间: {end_time - start_time} 秒")
