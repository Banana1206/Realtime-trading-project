from rl_agent.memory import Transition, ReplayMemory
from rl_agent.model import DQN

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
            # Transpose the batch (see https://stackoverflow.com/a/19343/3343043 for
            # detailed explanation). This converts batch-array of Transitions
            # to Transition of batch-arrays.
            batch = Transition(*zip(*transitions))

            # Compute a mask of non-final states and concatenate the batch elements
            # (a final state would've been the one after which simulation ended)
            # print("########################################")
            # my_array = np.array(batch.next_state)
            # print('batch.next_state: ',my_array.shape)
            next_state = torch.FloatTensor(np.array(batch.next_state)).to(device)  # Convert to a numpy array first
            non_final_mask = torch.tensor(tuple(map(lambda s: s is not None, batch.next_state)))
            non_final_next_states = torch.cat([s for s in next_state if s is not None])
            state_batch = torch.FloatTensor(np.array(batch.state)).to(device)  # Convert to a numpy array first
            action_batch = torch.LongTensor(np.array(batch.action)).to(device)  # Convert to a numpy array first
            reward_batch = torch.FloatTensor(np.array(batch.reward)).to(device)  # Convert to a numpy array first


            # Compute Q(s_t, a) - the model computes Q(s_t), then we select the
            # columns of actions taken. These are the actions which would've been taken
            # for each batch state according to policy_net
            state_action_values = self.policy_net(state_batch).reshape((self.batch_size, 3)).gather(1, action_batch.reshape((self.batch_size, 1)))

            # Compute V(s_{t+1}) for all next states.
            # Expected values of actions for non_final_next_states are computed based
            # on the "older" target_net; selecting their best reward with max(1)[0].
            # This is merged based on the mask, such that we'll have either the expected
            # state value or 0 in case the state was final.
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
