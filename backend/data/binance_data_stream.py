import asyncio
import logging
from binance import AsyncClient, BinanceSocketManager

# Configure logging
logging.basicConfig(level=logging.INFO)

# API Credentials
BINANCE_API_KEY = "fZjkR4L7d0oCa4FE87soSqvYNcyrutlmjtIVVhXfwVnRbEuCx7qrtYkI5zWF3Qfc"
BINANCE_API_SECRET = 'S8UJohKiOkVHgH59Bcsa8KP3URLPPNzyOewiFYF4pXX8OKaDhVG6Ewejtbiw4A2v'
TELEGRAM_BOT_TOKEN = '7574272150:AAEx0Vv8fog11nOheF8LIqqQVw0kLDaZMBE'
CHAT_ID = "7843740783"  # Replace with your actual chat ID

async def fetch_trade_data(pair):
    """Fetch real-time trade data for a trading pair."""
    client = await AsyncClient.create(BINANCE_API_KEY, BINANCE_API_SECRET)
    bsm = BinanceSocketManager(client)
    stream = bsm.trade_socket(pair)

    async with stream as trade_stream:
        while True:
            try:
                msg = await trade_stream.recv()
                logging.info(f"Trade Update for {pair}: {msg}")
            except Exception as e:
                logging.error(f"WebSocket error: {e}")

    await client.close_connection()

if __name__ == "__main__":
    # Replace 'BTCUSDT' with any pair you want to track
    asyncio.run(fetch_trade_data('TONUSDT'))
