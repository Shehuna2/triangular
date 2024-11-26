from aiogram import Bot

async def send_telegram_message(token, chat_id, message):
    """Send Telegram message via bot."""
    bot = Bot(token=token)
    try:
        await bot.send_message(chat_id, message)
    finally:
        await bot.close()
