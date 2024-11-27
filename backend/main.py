import asyncio
import logging
from backend.data.binance_data_stream import BinanceDataStream
from backend.arbitrage.arbitrage_detection import ArbitrageDetector
from backend.notifications.telegram_alerts import TelegramAlerts

# Configure logging
logging.basicConfig(level=logging.INFO)

# API Credentials
BINANCE_API_KEY = "fZjkR4L7d0oCa4FE87soSqvYNcyrutlmjtIVVhXfwVnRbEuCx7qrtYkI5zWF3Qfc"
BINANCE_API_SECRET = 'S8UJohKiOkVHgH59Bcsa8KP3URLPPNzyOewiFYF4pXX8OKaDhVG6Ewejtbiw4A2v'
TELEGRAM_BOT_TOKEN = '7574272150:AAEx0Vv8fog11nOheF8LIqqQVw0kLDaZMBE'
CHAT_ID = "7843740783" 


# Liquidity threshold
LIQUIDITY_THRESHOLD = 10000

async def main():
    """Main function to run the arbitrage detection system."""
    # Initialize services
    data_stream = BinanceDataStream(api_key=BINANCE_API_KEY, api_secret=BINANCE_API_SECRET)
    telegram_alerts = TelegramAlerts(bot_token=TELEGRAM_BOT_TOKEN, chat_id=CHAT_ID)
    detector = ArbitrageDetector(data_stream, liquidity_threshold=LIQUIDITY_THRESHOLD, telegram_alerts=telegram_alerts)

    # Fetch trading pairs and prices
    all_pairs = data_stream.get_all_pairs()
    prices = data_stream.get_prices()

    # Filter pairs based on liquidity
    filtered_pairs = detector.filter_pairs_by_liquidity(all_pairs)
    logging.info(f"Filtered pairs: {filtered_pairs}")

    # Detect arbitrage opportunities
    opportunities = detector.detect_arbitrage(filtered_pairs, prices)

    # Send alerts for each opportunity
    await detector.send_arbitrage_alerts(opportunities)

if __name__ == "__main__":
    asyncio.run(main())


