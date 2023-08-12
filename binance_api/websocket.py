import asyncio
import websockets

async def listen():
    """
        read about binance websocket: https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md
    """
    url = "wss://stream.binance.com:9443/ws/bnbusdt@kline_3m"
    
    async with websockets.connect(url) as ws:
        while True:
            msg = await ws.recv()
            print("=============")
            print(msg)
            # await asyncio.sleep(1)
        
asyncio.get_event_loop().run_until_complete(listen())


