import torch
import torch.nn as nn

# Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class RNN(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim, device):
        super(RNN, self).__init__()
        # Hidden dimension
        self.hidden_dim = hidden_dim
        
        self.device = device

        # Number of hidden layers
        self.layer_dim = num_layers

        # Recurrent layer
        self.rnn = nn.RNN(input_dim, hidden_dim, num_layers, batch_first=True, nonlinearity='relu').to(self.device)

        # Output layer
        self.fc = nn.Linear(hidden_dim, output_dim).to(self.device)

    def forward(self, x):
        # Initialize hidden state with zeros
        h0 = torch.zeros(self.layer_dim, x.size(0), self.hidden_dim).to(self.device)

        # Forward propagate RNN
        out, hn = self.rnn(x, h0.detach())

        # Decode the hidden state of the last time step
        out = self.fc(out[:, -1, :])

        return out
    