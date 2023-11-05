import gymnasium as gym
import numpy as np
from gymnasium import spaces
from function import formatPrice, getState, getTestStockDataVec, log1p_scaling, getDataFromPath
from param import *
from rl_agent.memory import Transition, ReplayMemory
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import PPO


N_DISCRETE_ACTIONS = 3

class PPOTradingEnv(gym.Env):
    """Custom Environment that follows gym interface."""

    # metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self, data, window_size, initial_balance):
        super(PPOTradingEnv, self).__init__()
        self.data = data  # The financial data
        self.window_size = window_size
        self.initial_balance = initial_balance
        self.current_balance = self.initial_balance
        self.current_step = window_size - 1
        self.lenght = int(len(self.data)/5 -1)
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(3)
        # Example for using image as input (channel-first; channel-last also works):
        self.observation_space = spaces.Box(low=0, high=20, shape=(window_size*25,), dtype=np.float64)
        # self.memory = ReplayMemory(100000)

    def step(self, action):
        # close_price = self.data[self.current_step]['close']
        self.current_step += 1
        # print("Action....: ", action)

        if self.current_step == self.lenght - 1:
            done = True
        close_price = float(self.data[self.data['symbol']==BTCUSDT].loc[self.data.index[self.current_step]].close)
        reward = 0
        done = False

        if action == 1:  # Buy
            if self.current_balance >= close_price:
                self.inventory.append(close_price)
                self.current_balance -= close_price
                # reward = - close_price
                # print("Reward_BUY...: ", self.current_balance)
        elif action == 2 and len(self.inventory) > 0: # sell
            bought_price = self.inventory.pop(0)
            profit = close_price - bought_price
            self.current_balance = self.current_balance + close_price + profit * 1000
            
            # reward = close_price + profit * 1000
            # self.current_balance += close_price
            # print("Reward_SELL...: ", self.current_balance)
            
        reward = self.current_balance
        if self.current_step % 100==0:
            print("Reward...: ", reward, "self.current_step...: ", self.current_step)
        # observation = self._get_observation()
        self.observation = getState(self.data, self.current_step, self.window_size)
        self.observation = np.array(self.observation, dtype=np.float64).flatten()
        

        # # print("self.observation.shape... ", self.observation.shape)
        if self.observation.shape[0] != 250:
            done = True
            
        truncated = False
        
        return self.observation, reward, done, truncated,{}
        
        # return observation, reward, terminated, truncated, info

    def reset(self, seed=None, options=None):
        self.current_step = self.window_size - 1
        self.current_balance = self.initial_balance
        self.inventory = []
        self.observation = getState(self.data, self.current_step, self.window_size)
        self.observation = np.array(self.observation, dtype=np.float64).flatten()
        return self.observation, {}
    

    # def render(self):
    #     ...

    # def close(self):
    #     ...
    
    
data = log1p_scaling(getDataFromPath("./data/data_2022.csv"))
# print(max(data.to_numpy))
# # data = getDataFromPath("./data/data_2022.csv")
# # Instantiate the env
env = PPOTradingEnv(data, 10, 1000)
model =  PPO("MlpPolicy", env, verbose=1)

# print(env.lenght)
# # check_env(env)
# # Define and Train the agent
for _ in range(2):
    # vec_env = model.get_env()
    # env = vec_env.reset()
    model =  model.learn(total_timesteps=10000)
    model.save("./model_PPO/PPO_MultiBinScaling.zip")
    
# model.load("./data/PPO_MultiBinScaling.zip")
vec_env = model.get_env()
obs = vec_env.reset()
# for i in range(1000):
#     action, _state = model.predict(obs, deterministic=True)
#     obs, reward, done, info = vec_env.step(action)
#     print(reward)
#     vec_env.render("human")
