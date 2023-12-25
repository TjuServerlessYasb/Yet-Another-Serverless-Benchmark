import os
import torch
# 确保CuDNN不会被使用
torch.backends.cudnn.enabled = False
# 检查CUDA（GPU支持）是否可用
if torch.cuda.is_available():
# if True:
    # 设置设备为GPU
    device = torch.device("cuda") 

    # 在GPU上创建两个随机矩阵
    matrix1 = torch.rand(10, 20, device=device)
    matrix2 = torch.rand(20, 30, device=device)

    # 执行矩阵乘法
    result = torch.matmul(matrix1, matrix2)
    print(result)
else:
    result = "CUDA不可用,无法在GPU上执行。"
