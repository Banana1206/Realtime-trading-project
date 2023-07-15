# Cài !pip install python-binance
from binance.enums import *
# from functions import *
from binance.client import Client
from confluent_kafka import Producer
import pandas as pd
import numpy as np
# from faker import Faker
import time
import json
import random


TEST_API_KEY = '38a8NZYdoKTqdQBvztjSDVI0kZUSuvA6tC0LDKohH5hPfE5S6QTxJWIe9FMZFj2q'
TEST_API_SECRET = 'bTEGJyrHWKpPHSxfF3nXAu8ruZsbcXqYwlKnHDiI4mRKRNqH6VbB9ILsmTbQRYXc'
client = Client(api_key=TEST_API_KEY, api_secret=TEST_API_SECRET, testnet=True)

def create_data_dict(data):
    data_dict = {
        "Open time": data[0],
        # "Open": data[1],
        # "High": data[2],
        # "Low": data[3],
        "Close": data[4],
        "Volume": data[5],
        # "Close time": data[6],
        # "Quote asset volume": data[7],
        "Number of trades": data[8],
        "Taker buy base asset volume": data[9],
        # "Taker buy quote asset volume": data[10],
        # "Ignore": data[11],
        # "Symbol": data[12],
        # Add more key-value pairs as needed
    }
    if data[12] == "BTCUSDT":
        data_dict['Symbol'] = 0
    elif data[12] == "ETHUSDT":
        data_dict['Symbol'] = 1
    elif data[12] == "BNBUSDT":
        data_dict['Symbol'] = 2
    elif data[12] == "XRPUSDT":
        data_dict['Symbol'] = 3
    else:
     data_dict['Symbol'] = 4
        
    
    return data_dict

def create_train_data(data):
    listData = []
    listData.append(round(float(data[4]), 3))
    listData.append(round(float(data[5]), 3))
    listData.append(round(float(data[8]), 3))
    listData.append(round(float(data[9]), 3))

    if data[12] == "BTCUSDT":
        listData.append(0)
    elif data[12] == "ETHUSDT":
        listData.append(1)
    elif data[12] == "BNBUSDT":
        listData.append(2)
    elif data[12] == "XRPUSDT":
        listData.append(3)
    else:
        listData.append(4)

    return listData

    


def save_to_json(data, pairs):
    file_name = "data.json"
    data_all = {}  # Create an empty dictionary to store all data_dict dictionaries
    with open(file_name, 'a') as file:
        for pair, pair_data in zip(pairs, data):
            data_dict = create_data_dict(pair_data)
            data_all[pair] = data_dict  # Add data_dict to data_all dictionary

        json.dump(data_all, file)
        file.write('\n')



# def producer():
#     # Khởi tạo Kafka producer
#     bootstrap_servers = 'localhost:9091'
#     topic = 'trading3'
#     producer = Producer({'bootstrap.servers': bootstrap_servers})

#     data = getStockDataVec()
#     index = data.index
   

#     # Gửi dữ liệu giả lập đến Kafka
#     for i in range(len(data/5)):
#         stream_data = getState(data.loc[index[i]])
#         print("Thu tu: ", i)
#         print(stream_data)
#         # print(stream_data.tobytes())
#         # print(np.frombuffer(stream_data.tobytes(), dtype=np.float64))
#         send_data_to_kafka(producer, topic, stream_data)

#         # Thời gian chờ giữa các lần gửi dữ liệu
#         time.sleep(5)

def send_data_to_kafka(producer, topic, stream_data):
    producer.produce(topic, value=stream_data)
    producer.flush()
        
if __name__ == "__main__":

    trading_pairs = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "LTCUSDT"]
    api_key = '38a8NZYdoKTqdQBvztjSDVI0kZUSuvA6tC0LDKohH5hPfE5S6QTxJWIe9FMZFj2q'
    api_secret = 'bTEGJyrHWKpPHSxfF3nXAu8ruZsbcXqYwlKnHDiI4mRKRNqH6VbB9ILsmTbQRYXc'
    # Initialize Binance client
    client = Client(api_key, api_secret)
    
     # Initialize producer
    bootstrap_servers = 'localhost:9091'
    topic = 'thao_loz'
    producer = Producer({'bootstrap.servers': bootstrap_servers},)

    data = [] # contain data with windowsize =5
    while True:

        sub_data =[] # contain data for each day
        for pair in trading_pairs:
            pair_data = client.get_historical_klines(pair, Client.KLINE_INTERVAL_3MINUTE, "3 min ago UTC")
            pair_data[0].append(pair)
            sub_data.append(create_train_data(pair_data[0]))
  
        if(len(data)==5):
            data.pop(0)
            data.append(sub_data)
            send_data = json.dumps(data).encode('utf-8')
            send_data_to_kafka(producer, topic, send_data)
            print(send_data)
            
        else:
            data.append(sub_data)
        
        
        
        # send_data_to_kafka(producer, topic, df)
        # print(json.dumps(data).encode('utf-8'))
        # break
        
        # break
        time.sleep(1)
