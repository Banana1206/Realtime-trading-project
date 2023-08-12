import asyncio
from binance.enums import *
from binance.client import Client
from confluent_kafka import Producer
import json


async def send_data_to_kafka(producer, topic, stream_data):
    producer.produce(topic, value=stream_data)
    producer.flush()
    
def create_train_data(data):
    listData = []
    listData.append(float(data[4]))
    listData.append(float(data[5]))
    listData.append(float(data[8]))
    listData.append(float(data[9]))
    listData.append(get_symbol(data[12]))
    return listData

def get_symbol(pair):
    if pair == "BTCUSDT":
        return 0
    elif pair == "ETHUSDT":
        return 1
    elif pair == "BNBUSDT":
        return 2
    elif pair == "XRPUSDT":
        return 3
    else:
        return 4

async def main():
    trading_pairs = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "LTCUSDT"]
    api_key = '38a8NZYdoKTqdQBvztjSDVI0kZUSuvA6tC0LDKohH5hPfE5S6QTxJWIe9FMZFj2q'
    api_secret = 'bTEGJyrHWKpPHSxfF3nXAu8ruZsbcXqYwlKnHDiI4mRKRNqH6VbB9ILsmTbQRYXc'
    client = Client(api_key, api_secret)
    
    bootstrap_servers = 'localhost:9092'
    topic = 'nguyentri'
    producer = Producer({'bootstrap.servers': bootstrap_servers})

    data = []
    while True:
        sub_data = []
        for pair in trading_pairs:
            pair_data = client.get_historical_klines(pair, Client.KLINE_INTERVAL_3MINUTE, "3 min ago UTC")
            pair_data[0].append(pair)
            sub_data.append(create_train_data(pair_data[0]))
  
        if len(data) == 10:
            data.pop(0)
            data.append(sub_data)
            send_data = json.dumps(data).encode('utf-8')
            # await send_data_to_kafka(producer, topic, send_data)
            print(send_data)
            await asyncio.sleep(5)
        else:
            data.append(sub_data)
            await asyncio.sleep(1)
        


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
