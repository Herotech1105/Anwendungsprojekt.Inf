import torch
import torch.nn as nn

class ManualLSTMCell(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(ManualLSTMCell, self).__init__()
        self.hidden_size = hidden_size

        # Initialize weights and biases for all gates in one matrix for efficiency
        self.W = nn.Parameter(torch.randn(4 * hidden_size, input_size + hidden_size) * 0.1)
        self.b = nn.Parameter(torch.zeros(4 * hidden_size, 1))

    def forward(self, x_t, h_prev, c_prev):
        
        # Combine input and previous hidden state
        combined = torch.cat((x_t, h_prev), dim=0)

        # Calculate gates in one matrix
        gates = torch.matmul(self.W, combined) + self.b

        i_gate = torch.sigmoid(gates[0:self.hidden_size])
        f_gate = torch.sigmoid(gates[self.hidden_size : 2*self.hidden_size])
        o_gate = torch.sigmoid(gates[2*self.hidden_size : 3*self.hidden_size])
        g_gate = torch.tanh(gates[3*self.hidden_size : 4*self.hidden_size])

        # Update cell state and hidden state
        c_t = f_gate * c_prev + i_gate * g_gate
        h_t = o_gate * torch.tanh(c_t)

        return h_t, c_t