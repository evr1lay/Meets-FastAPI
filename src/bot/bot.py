from telebot import TeleBot
from dotenv import load_dotenv

import requests
import os

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if BOT_TOKEN is None:
    raise ValueError("BOT_TOKEN not found")

bot = TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['API', 'api'])
def api_status(message):
    req = requests.get("http://localhost:8000")
    api_enabled = req.json()["API_ENABLED"]
    if api_enabled is False:
        bot.reply_to(message, "API is terminated")
        raise
    
    bot.reply_to(message, "API is enabled")
    
if __name__ == "__main__":
    print("✨ Bot is running")
    bot.infinity_polling()
    print("🔒 Bot is terminated")