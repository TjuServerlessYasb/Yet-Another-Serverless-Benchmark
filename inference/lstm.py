import torch
import torch.nn as nn
import torch.optim as optim

# 确保CuDNN不会被使用
torch.backends.cudnn.enabled = False

# 检查GPU是否可用
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 定义LSTM模型
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])
        return out

# 模型参数
input_size = 10
hidden_size = 20
num_layers = 2
output_size = 1

# 创建模型实例并移到GPU
model = LSTMModel(input_size, hidden_size, num_layers, output_size).to(device)

# 模拟数据
batch_size = 5
seq_length = 15
dummy_input = torch.randn(batch_size, seq_length, input_size).to(device)
dummy_output = torch.randn(batch_size, output_size).to(device)


# 加载模型
model_loaded = LSTMModel(input_size, hidden_size, num_layers, output_size)
model_loaded.load_state_dict(torch.load('lstm_no_cudnn.pkl'))

print(model_loaded)

model_loaded = model_loaded.to(device)

# 在GPU上进行一次推理
model_loaded.eval()
with torch.no_grad():
    test_input = torch.randn(batch_size, seq_length, input_size).to(device)
    test_output = model_loaded(test_input)
    print(test_output)
