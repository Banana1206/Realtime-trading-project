from rl_agent.memory import Transition, ReplayMemory
from rl_agent.model import DQN, GraphNetwork, GraphNetworkLayer

import numpy as np
import random
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import pandas as pd
import os

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Agent: 
    def __init__(self, state_size, is_eval=False) :
        self.state_size = state_size
        self.action_size = 3 # hold, buy, sell
        self.memory = ReplayMemory(100000)
        self.inventory = []
        self.is_eval = is_eval
        """
            is_eval sử dụng để xác định trạng thái của tác tử, \
            liệu tác tử đang ở trong giai đoạn đánh giá (evaluation) hay không. 
            Trong giai đoạn đánh giá, tác tử thường không thực hiện việc khám phá 
            và chỉ tập trung vào khai thác kiến thức đã học để đánh giá hiệu suất của mô hình.
        """
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.batch_size = 32

        if os.path.exists('models/target_model'):
            self.policy_net = torch.load('models/policy_model', map_location=device)
            self.target_net = torch.load('models/target_model', map_location=device)
        else:
            self.policy_net = DQN(state_size, self.action_size)
            self.target_net = DQN(state_size, self.action_size)
        self.optimizer = optim.RMSprop(self.policy_net.parameters(), lr=0.005, momentum=0.9)

    def act(self, state):
        if not self.is_eval and np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)

        tensor = torch.FloatTensor(state).to(device)
        options = self.target_net(tensor)
        return np.argmax(options[0].detach().numpy())

    def optimize(self):
        try:
            if len(self.memory) < self.batch_size:
                    return
            transitions = self.memory.sample(self.batch_size)
            batch = Transition(*zip(*transitions))

            next_state = torch.FloatTensor(np.array(batch.next_state)).to(device)  # Convert to a numpy array first
            non_final_mask = torch.tensor(tuple(map(lambda s: s is not None, batch.next_state)))
            non_final_next_states = torch.cat([s for s in next_state if s is not None])
            state_batch = torch.FloatTensor(np.array(batch.state)).to(device)  # Convert to a numpy array first
            action_batch = torch.LongTensor(np.array(batch.action)).to(device)  # Convert to a numpy array first
            reward_batch = torch.FloatTensor(np.array(batch.reward)).to(device)  # Convert to a numpy array first


            state_action_values = self.policy_net(state_batch).reshape((self.batch_size, 3)).gather(1, action_batch.reshape((self.batch_size, 1)))

            next_state_values = torch.zeros(self.batch_size, device=device)
            next_state_values[non_final_mask] = self.target_net(non_final_next_states).max(1)[0].detach()
            # Compute the expected Q values
            expected_state_action_values = (next_state_values * self.gamma) + reward_batch

            # Compute Huber loss
            loss = F.smooth_l1_loss(state_action_values, expected_state_action_values.unsqueeze(1))

            # Optimize the model
            self.optimizer.zero_grad()
            loss.backward()
            for param in self.policy_net.parameters():
                    param.grad.data.clamp_(-1, 1)
            self.optimizer.step()
        except Exception as e:
            # print("An error occurred during optimization:", e)
            pass


class Graph_Agent:
    def __init__(self, state_size, is_eval=False):
        self.state_size = state_size
        self.action_size = 3  # hold, buy, sell
        self.memory = ReplayMemory(100000)
        self.inventory = []
        self.is_eval = is_eval
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.batch_size = 32

        if os.path.exists('models/target_model'):
            self.policy_net = torch.load('models/policy_model', map_location=device)
            self.target_net = torch.load('models/target_model', map_location=device)
        else:
            self.policy_net = GraphNetwork(state_size, self.action_size).to(device)
            self.target_net = GraphNetwork(state_size, self.action_size).to(device)
        self.optimizer = optim.RMSprop(self.policy_net.parameters(), lr=0.005, momentum=0.9)

    def act(self, state):
        if not self.is_eval and np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)

        # Convert state to appropriate input format for Graph Network
        nodes = torch.FloatTensor(state).to(device)  # Assuming 'state' is a list or numpy array of node features
        edges = None  # Depending on your graph structure, you might have edge features here
        adjacency_matrix = None  # Depending on your graph structure, you might have an adjacency matrix here

        with torch.no_grad():
            options = self.target_net(nodes, edges, adjacency_matrix)
            return np.argmax(options[0].detach().cpu().numpy())

    def optimize(self):
        try:
            if len(self.memory) < self.batch_size:
                return
            transitions = self.memory.sample(self.batch_size)
            batch = Transition(*zip(*transitions))

            next_state = torch.FloatTensor(np.array(batch.next_state)).to(device)
            non_final_mask = torch.tensor(tuple(map(lambda s: s is not None, batch.next_state)))
            non_final_next_states = torch.cat([s for s in next_state if s is not None])
            state_batch = torch.FloatTensor(np.array(batch.state)).to(device)
            action_batch = torch.LongTensor(np.array(batch.action)).to(device)
            reward_batch = torch.FloatTensor(np.array(batch.reward)).to(device)

            state_action_values = self.policy_net(state_batch, None, None)
            state_action_values = state_action_values.gather(1, action_batch.reshape((self.batch_size, 1)))

            next_state_values = torch.zeros(self.batch_size, device=device)
            next_state_values[non_final_mask] = self.target_net(non_final_next_states, None, None).max(1)[0].detach()
            expected_state_action_values = (next_state_values * self.gamma) + reward_batch

            loss = F.smooth_l1_loss(state_action_values, expected_state_action_values.unsqueeze(1))

            self.optimizer.zero_grad()
            loss.backward()
            for param in self.policy_net.parameters():
                param.grad.data.clamp_(-1, 1)
            self.optimizer.step()
        except Exception as e:
            pass