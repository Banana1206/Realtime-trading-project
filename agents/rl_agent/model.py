import torch
import torch.nn as nn

class DQN(nn.Module):
	def __init__(self, state_size, action_size):
		super(DQN, self).__init__()
		self.main = nn.Sequential(
			nn.Linear(state_size, 64),
			nn.LeakyReLU(0.01, inplace=True),
			nn.Linear(64, 32),
			nn.LeakyReLU(0.01, inplace=True),
			nn.Linear(32, 8),
			nn.LeakyReLU(0.01, inplace=True),
			nn.Linear(8, action_size),
		)
  
	def forward(self, input):
		return self.main(input)


class DQNLSTM(nn.Module):
    def __init__(self, state_size, action_size, hidden_size=64):
        super(DQNLSTM, self).__init__()
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(state_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, action_size)
        self.leaky_relu = nn.LeakyReLU(0.01, inplace=True)

    def forward(self, input):
        # input shape: (batch_size, sequence_length, state_size)

        # LSTM layer
        lstm_out, _ = self.lstm(input)  # lstm_out shape: (batch_size, sequence_length, hidden_size)

        # Extract the last time step's output
        last_output = lstm_out[:, -1, :]  # shape: (batch_size, hidden_size)

        # Fully connected layer
        x = self.fc(last_output)  # x shape: (batch_size, action_size)

        # Apply LeakyReLU
        x = self.leaky_relu(x)

        return x
