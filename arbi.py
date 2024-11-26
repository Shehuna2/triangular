from binance import AsyncClient, BinanceSocketManager

class BinanceDataStream:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.client = None
        self.bsm = None

    async def connect(self):
        self.client = await AsyncClient.create(self.api_key, self.api_secret)
        self.bsm = BinanceSocketManager(self.client)

    async def stream_ticker(self, symbol):
        stream = self.bsm.trade_socket(symbol)
        async with stream as t_stream:
            while True:
                msg = await t_stream.recv()
                yield msg  # Real-time price data

    async def close(self):
        await self.client.close_connection()
