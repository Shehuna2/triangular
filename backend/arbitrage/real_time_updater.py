import asyncio
import logging
from binance import AsyncClient, BinanceSocketManager

# Configure logging
logging.basicConfig(level=logging.INFO)

class RealTimePriceUpdater:
    def __init__(self, pairs):
        self.pairs = pairs
        self.prices = {}  # Shared dictionary for prices
        self.client = None
        self.bsm = None

    async def start(self, api_key, api_secret):
        """Start WebSocket connections to update prices in real-time."""
        self.client = await AsyncClient.create(api_key, api_secret)
        self.bsm = BinanceSocketManager(self.client)
        
        streams = [self.bsm.trade_socket(pair) for pair in self.pairs]

        async def handle_stream(stream):
            async with stream as s:
                while True:
                    msg = await s.recv()
                    self._update_price(msg)

        tasks = [handle_stream(stream) for stream in streams]
        await asyncio.gather(*tasks)

    def _update_price(self, msg):
        """Update the prices dictionary with new data."""
        try:
            symbol = msg['s']
            price = float(msg['p'])
            self.prices[symbol] = price
            logging.info(f"Updated price: {symbol} = {price}")
        except KeyError as e:
            logging.error(f"Malformed message: {msg} - {e}")

    async def stop(self):
        """Stop the WebSocket and close the client."""
        await self.client.close_connection()
