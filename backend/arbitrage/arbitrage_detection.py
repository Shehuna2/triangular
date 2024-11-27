import time
import asyncio

from binance import AsyncClient

from real_time_updater import RealTimePriceUpdater



# API keys (store securely)
BINANCE_API_KEY = "fZjkR4L7d0oCa4FE87soSqvYNcyrutlmjtIVVhXfwVnRbEuCx7qrtYkI5zWF3Qfc"
BINANCE_API_SECRET = 'S8UJohKiOkVHgH59Bcsa8KP3URLPPNzyOewiFYF4pXX8OKaDhVG6Ewejtbiw4A2v'


async def fetch_all_pairs(client):
    """Fetch all trading pairs from Binance."""
    exchange_info = await client.get_exchange_info()
    symbols = exchange_info['symbols']
    return [symbol['symbol'] for symbol in symbols if symbol['status'] == 'TRADING']

async def fetch_prices(client, pairs):
    """Fetch the latest prices for all pairs."""
    # Batch-fetch all prices
    tickers = await client.get_all_tickers()
    prices = {ticker['symbol']: float(ticker['price']) for ticker in tickers if ticker['symbol'] in pairs}
    return prices

async def filter_pairs(client, pairs, min_volume=1000):
    """Filter pairs based on 24-hour trading volume."""
    filtered_pairs = []
    for pair in pairs:
        try:
            stats = await client.get_ticker(symbol=pair)
            volume = float(stats['quoteVolume'])
            if volume >= min_volume:
                filtered_pairs.append(pair)
        except Exception as e:
            print(f"Error fetching stats for {pair}: {e}")
    return filtered_pairs


def find_arbitrage_paths(prices):
    """Detect triangular arbitrage opportunities."""
    opportunities = []
    currencies = set(
        [pair[:3] for pair in prices.keys()] +
        [pair[3:] for pair in prices.keys()]
    )
    for base in currencies:
        for intermediate in currencies:
            if base == intermediate:
                continue
            for quote in currencies:
                if base == quote or intermediate == quote:
                    continue
                try:
                    rate1 = prices[f"{base}{intermediate}"]
                    rate2 = prices[f"{intermediate}{quote}"]
                    rate3 = prices[f"{quote}{base}"]

                    arbitrage = (1 / rate1) * rate2 * rate3
                    profit_percent = (arbitrage - 1) * 100
                    if profit_percent > 0:
                        opportunities.append((base, intermediate, quote, profit_percent))
                except KeyError:
                    continue
    return opportunities

async def main():
    # Define trading pairs
    pairs = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]  # Add your pairs here

    # Initialize real-time updater
    price_updater = RealTimePriceUpdater(pairs)

    try:
        # Start real-time price updates
        await price_updater.start(BINANCE_API_KEY, BINANCE_API_SECRET)

        # Run arbitrage detection in real time
        print("Starting arbitrage detection...")
        while True:
            opportunities = find_arbitrage_paths(price_updater.prices)
            if opportunities:
                for opportunity in opportunities:
                    base, intermediate, quote, profit = opportunity
                    print(f"Arbitrage Opportunity: {base} → {intermediate} → {quote} → {base} | Profit: {profit:.2f}%")
            await asyncio.sleep(1)  # Run detection every second
    finally:
        # Stop WebSocket and clean up
        await price_updater.stop()

if __name__ == "__main__":
    asyncio.run(main())
