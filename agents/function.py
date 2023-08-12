import numpy as np
import math
import pandas as pd

# prints formatted price
def formatPrice(n):
	return ("-$" if n < 0 else "$") + "{0:.2f}".format(abs(n))

# returns the vector containing stock data from a fixed file
# def getStockDataVec():
#     df=pd.read_csv("./data/full_data.csv")
#     df = df[['open_time', 'close', 'volume','count', 'taker_buy_volume','symbol']]
#     df.set_index('open_time', inplace=True)
#     df['symbol'][df['symbol']=='ADABUSD'] =0
#     df['symbol'][df['symbol']=='ETHBUSD'] =1
#     df['symbol'][df['symbol']=='BNBBUSD'] =2
#     df['symbol'][df['symbol']=='BTCBUSD'] =3
#     df['symbol'][df['symbol']=='DOTBUSD'] =4
#     return df

def getStockDataVec():
    df = pd.read_csv("./data/data_2021.csv")
    df = df[['open_time', 'close', 'volume', 'count', 'taker_buy_volume', 'symbol']]
    df.set_index('open_time', inplace=True)
    symbol_mapping = {'BNBUSDT': 0, 'BTCUSDT': 1, 'ETHUSDT': 2, 'LTCUSDT': 3, 'XRPUSDT': 4}
    df['symbol'] = df['symbol'].map(symbol_mapping).fillna(df['symbol'])
    return df

def getTestStockDataVec(path):
    df = pd.read_csv(path)
    df = df[['open_time', 'close', 'volume', 'count', 'taker_buy_volume', 'symbol']]
    df.set_index('open_time', inplace=True)
    symbol_mapping = {'BNBUSDT': 0, 'BTCUSDT': 1, 'ETHUSDT': 2, 'LTCUSDT': 3, 'XRPUSDT': 4}
    df['symbol'] = df['symbol'].map(symbol_mapping).fillna(df['symbol'])
    return df



def getState(data, t, n):
    d = t - n + 1
    index = data.index.unique()
    block = data.loc[index[d:t + 1]]
    return np.array(block).reshape(1,-1)