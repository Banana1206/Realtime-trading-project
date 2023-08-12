from rl_agent.linearDQNAgent import Agent as linearDQNAgent
from rl_agent.lstmDQNAgent import Agent as lstmDQNAgent

from rl_agent.memory import Transition, ReplayMemory
from function import formatPrice, getState, getTestStockDataVec
from param import *
from tqdm import tqdm
import pandas as pd

window_size = 10
path = "./data/data_2022.csv"


agent = linearDQNAgent(window_size*5*5) # 10 sample and each sample is 5x5 
data = getTestStockDataVec(path).head(2000)
l = len(data)
time = []
closes = []
buys = []
sells = []
capital = 100000
history_capital = []
history_profit = []


state = getState(data, window_size-1, window_size)

total_profit = 0
agent.inventory = []
# print(l)
# for t in range(window_size-1,l):

for t in range(window_size-1,l-1):


	action = agent.act(state)
 
	close_price = float(data[data['symbol']==BTCUSDT].loc[data.index[t]].close)
	# print(close_price)
 
	closes.append(close_price)
	time.append(data.index[t])
	# print(close_price)b

	# sit
	next_state = getState(data, t + 1, window_size)
	reward = 0

	if action == 1: # buy
		if capital > close_price:
			agent.inventory.append(data.loc[data.index[t]])
			buys.append(close_price)
			sells.append(None)
			capital -= close_price
		else:
			buys.append(None)
			sells.append(None)
		
	elif action == 2: # sell
		if len(agent.inventory) > 0:
      
			bought_price = agent.inventory.pop(0)
		
			# close_price = data[data['symbol']==BTCBUSD].loc[data.index[t]].close
			profit = close_price - float(bought_price[bought_price['symbol']==BTCUSDT].close.values.item())
			reward = max(profit, 0)
			total_profit += profit
			sells.append(close_price)
			buys.append(None)
			capital += close_price
		else:
			buys.append(None)
			sells.append(None)	
		# print("Sell: " + formatPrice(data[t]) + " | Profit: " + formatPrice(data[t] - bought_price))
		# print('total_profit: ',total_profit)
	elif action == 0:
		buys.append(None)
		sells.append(None)
	
	history_capital.append(capital)
	history_profit.append(total_profit)


	done = True if t%20 == 0 else False
	agent.memory.push(state, action, next_state, reward)
	state = next_state

	if done:
		print("--------------------------------")
		print("Total Profit: " + formatPrice(total_profit))
		print("--------------------------------")