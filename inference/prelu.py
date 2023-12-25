import torch
import torch.nn as nn
import time

# 检查CUDA（GPU支持）是否可用
if torch.cuda.is_available():

    # # x1
    # x1 = torch.tensor([[11,21,31],[21,31,41]],dtype=torch.int)
    # x1.shape # torch.Size([2, 3])
    # # x2
    # x2 = torch.tensor([[12,22,32],[22,32,42]],dtype=torch.int)
    # x2.shape  # torch.Size([2, 3])
    # inputs = [x1, x2]
    # print(inputs)
    # x3 = torch.cat(inputs, dim=0).shape
    # print(x3)
    
    device = torch.device("cuda") 
    
    # input = torch.arange(0, 12,device=device).view(1,3,2,2).float()
    input = torch.randn(1, 3, 2, 2,device=device)
    print(input.shape)
    print(input)
    m = nn.PReLU(3,device=device)
    output = m(input)
    print(output)
else:
    result = "CUDA不可用，无法在GPU上执行。"
    

