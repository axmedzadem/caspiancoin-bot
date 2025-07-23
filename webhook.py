import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.executor import start_webhook

API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise RuntimeError("API_TOKEN environment variable is not set")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

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

WEBHOOK_PATH = "/webhook"
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")
if not RENDER_EXTERNAL_URL:
    raise RuntimeError("RENDER_EXTERNAL_URL environment variable is not set")

WEBHOOK_URL = RENDER_EXTERNAL_URL + WEBHOOK_PATH

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    print(f"Webhook set to {WEBHOOK_URL}")

async def on_shutdown(dp):
    await bot.delete_webhook()
    print("Webhook deleted")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host="0.0.0.0",
        port=port,
    )
