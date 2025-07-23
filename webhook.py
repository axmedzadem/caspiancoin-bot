import os
from flask import Flask
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.executor import start_webhook

# Mühit dəyişənindən tokeni al
API_TOKEN = os.getenv("API_TOKEN")

# Bot və Dispatcher qur
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Flask tətbiqi qur
app = Flask(__name__)

# Ana səhifə
@app.route("/")
def home():
    return "Bot webhook server is running ✅"

# Start komandası
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(
                text="💰 CaspianCoin Al",
                web_app=types.WebAppInfo(url="https://caspiancoin.gumroad.com/l/oxnhw")
            )
        ]
    ])
    await message.answer(
        "🌊 *CaspianCoin* — Xəzərdən ilhamlanan rəqəmsal valyuta\n\nAşağıdakı düyməyə kliklə!",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

# Webhook ünvanı
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("RENDER_EXTERNAL_URL", "") + WEBHOOK_PATH

# Bot işə düşəndə webhook təyin et
async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

# Bot bağlananda webhook sil
async def on_shutdown(dp):
    await bot.delete_webhook()

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
