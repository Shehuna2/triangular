import logging
from aiogram import Bot

# Configure logger
logger = logging.getLogger(__name__)

class TelegramAlerts:
    def __init__(self, bot_token, chat_id):
        """Initialize the Telegram bot with the given token and chat ID."""
        self.bot = Bot(token=bot_token)
        self.chat_id = chat_id

    async def send_alert(self, message):
        """Send a message to the Telegram chat."""
        try:
            await self.bot.send_message(self.chat_id, message)
        except Exception as e:
            logger.error(f"Error sending Telegram alert: {e}")
            return False
        return True

    def format_arbitrage_message(self, path, profit):
        """Format the message for arbitrage opportunities."""
        return (
            f"💡 **Arbitrage Opportunity Detected!**\n"
            f"Path: {path}\n"
            f"Profit: {profit:.2f}%\n\n"
            f"📖 **Execution Guide**:\n"
            f"1. Trade **{path[0]}**: Buy {path[0][:-4]} with USDT.\n"
            f"2. Trade **{path[1]}**: Convert {path[0][:-4]} to {path[1][:-3]}.\n"
            f"3. Trade **{path[2]}**: Convert {path[1][:-3]} back to USDT.\n\n"
            f"⚠️ **Note**: Verify market prices and fees before executing trades."
        )
