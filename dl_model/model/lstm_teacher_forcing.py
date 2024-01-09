
import torch
import torch.nn as nn
import torch.optim as optim
import random

# Link: https://github.com/ThisuriLekamge/Stock-Price-Prediction-on-Bitcoin-trading-data-using-LSTM-with-PyTorch/blob/master/main.ipynb
# link: https://machinelearningmastery.com/teacher-forcing-for-recurrent-neural-networks/

class LSTM_Forcing(nn.Module):
  def __init__(self, input_size, hidden_size, output_size):
    super(LSTM_Forcing, self).__init__()
    self.input_size = input_size
    self.hidden_size = hidden_size
    self.output_size = output_size
    self.lstm = nn.LSTMCell(self.input_size, self.hidden_size)
    self.linear = nn.Linear(self.hidden_size, self.output_size)

  def forward(self, input, future=0, y=None):
    outputs = []

    #reset the state of LSTM
    #the state is kept till the end of the sequence
    h_t = torch.zeros(input.size(0), self.hidden_size, dtype=torch.float32)
    c_t = torch.zeros(input.size(0), self.hidden_size, dtype=torch.float32)

    for i, input_t in enumerate(input.chunk(input.size(1), dim=1)):
      h_t, c_t = self.lstm(input_t, (h_t,c_t))
      output = self.linear(h_t)
      outputs += [output]

    for i in range(future): #teacher forcing
      if y is not None and random.random()>0.5:
        output = y[:,[i]]
      h_t, c_t = self.lstm(output,(h_t,c_t))
      output = self.linear(h_t)
      outputs += [output]
    outputs = torch.stack(outputs,1).squeeze(2)
    return outputs  