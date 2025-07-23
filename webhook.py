import os
from flask import Flask
from bot import dp  # Əgər bot.py faylında dp və bot varsa
from aiogram import Bot, Dispatcher
from aiogram.utils.executor import start_webhook

# Tokeni mühitdən (Render Environment Variable) alırıq
API_TOKEN = os.getenv("API_TOKEN")

# Flask server
app = Flask(__name__)

# Aiogram üçün bot və dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Webhook ayarları
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("RENDER_EXTERNAL_URL", "") + WEBHOOK_PATH

@app.route("/")
def home():
    return "Bot webhook server is running ✅"

# Bot işə başlayanda webhook-u təyin et
async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

# Server bağlananda webhook-u sil
async def on_shutdown(dp):
    await bot.delete_webhook()

# Flask server və webhooku başlat
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host="0.0.0.0",
        port=port,
    )
