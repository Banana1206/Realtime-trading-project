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
	

class GraphNetworkLayer(nn.Module):
    def __init__(self, input_size, output_size):
        super(GraphNetworkLayer, self).__init__()
        self.message_function = nn.Sequential(
            nn.Linear(input_size, 16), 
            nn.LeakyReLU(0.01, inplace=True)
        )
        self.aggregation_function = nn.Sequential(
            nn.Linear(16, 8), 
            nn.LeakyReLU(0.01, inplace=True)
        )
        self.update_function = nn.Sequential(
            nn.Linear(8, output_size),
            nn.LeakyReLU(0.01, inplace=True)
        )

    def forward(self, node_inputs, edge_inputs, adjacency_matrix):
        node_messages = self.message_function(node_inputs)

        aggregated_messages = torch.matmul(adjacency_matrix, node_messages)

        aggregated_messages = self.aggregation_function(aggregated_messages)

        updated_nodes = self.update_function(torch.cat([node_inputs, aggregated_messages], dim=-1))

        return updated_nodes


class GraphNetwork(nn.Module):
    def __init__(self, state_size, action_size):
        super(GraphNetwork, self).__init__()
        self.node_encoder = nn.Sequential(
            nn.Linear(state_size, 64),
            nn.LeakyReLU(0.01, inplace=True)
        )

        self.graph_layer1 = GraphNetworkLayer(64, 32)
        self.graph_layer2 = GraphNetworkLayer(32, 8)
        self.output_layer = nn.Linear(8, action_size)

    def forward(self, nodes, edges, adjacency_matrix):
        encoded_nodes = self.node_encoder(nodes)

        updated_nodes = self.graph_layer1(encoded_nodes, edges, adjacency_matrix)
        updated_nodes = self.graph_layer2(updated_nodes, edges, adjacency_matrix)

        output = self.output_layer(updated_nodes)

        return output
