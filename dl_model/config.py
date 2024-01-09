WINDOW_SIZE = 11 # 10 PERIODS OF TIME FOR VARIABLE X AND 1 PERIOD FOR Y
INPUT_DIM = 150 # 3 SYMBOL * 5 ATTRIBUTES * 10 PERIODS OF TIME X
NUM_LAYERS = 2
HIDDEN_DIM = 64

# ====================================
# SYMBOL VALUES
BNBUSDT= 0
BTCUSDT= 1
ETHUSDT= 2

# ====================================
# DATA
PATH_DATA = "../training_data/data_norm_2021_2022.csv"
SAVE_MODEL = "./results/"

#=====================================
# TRAINING
BATCH_SIZE = 64
EPOCHS = 10

# =====================================
# DEVICE CONFIGURATION
import torch
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')