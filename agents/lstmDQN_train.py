from lstmDQN_agent.Agent import Agent
from lstmDQN_agent.memory import Transition, ReplayMemory
from function import *
from param import *
import sys
import torch
from tqdm import tqdm


stock_name, window_size, episode_count =  "data_2021", 10, 1000


agent = Agent(window_size*5*5) # 10 sample and each sample is 5x5 
data = getStockDataVec()
l = len(data)

for e in range(episode_count + 1):
	print("#############################################")
	print("Episode " + str(e) + "/" + str(episode_count))
	state = getState(data, window_size-1, window_size)

	total_profit = 0
	agent.inventory = []
	# print(l)
 	# for t in range(window_size-1,l):

	for t in tqdm(range(window_size-1,l)):
		# t= i*5-1
  
		# print(f"i : {i}, t: {t}".format(i,t))

		# print(t)
		action = agent.act(state)

		# sit
		next_state = getState(data, t + 1, window_size)
		reward = 0

		if action == 1: # buy
			agent.inventory.append(data.loc[data.index[t]])
			# print("Buy: " + formatPrice(data[t]))

		elif action == 2 and len(agent.inventory) > 0: # sell
			bought_price = agent.inventory.pop(0)
			
			close_price = data[data['symbol']==BTCUSDT].loc[data.index[t]].close
			profit = close_price - bought_price[bought_price['symbol']==BTCUSDT].close.values.item()
			reward = max(profit, 0)
			total_profit += profit
			# print("Sell: " + formatPrice(data[t]) + " | Profit: " + formatPrice(data[t] - bought_price))
			# print('total_profit: ',total_profit)

		done = True if t == l - 1 else False
		agent.memory.push(state, action, next_state, reward)
		state = next_state

		# if done:
		if t %50==0:
			print("--------------------------------")
			print("Total Profit: " + formatPrice(total_profit))
			print("--------------------------------")

		agent.optimize()
	if e % 2 == 0:
		agent.target_net.load_state_dict(agent.policy_net.state_dict())
		torch.save(agent.policy_net, "models_lstmDQN/policy_model")
		torch.save(agent.target_net, "models_lstmDQN/target_model")