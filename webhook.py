import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiohttp import web
import logging

# Ətraf mühitdən API_TOKEN oxunur
API_TOKEN = os.getenv("API_TOKEN")

# Əgər token yoxdur, xətanı göstər
if not API_TOKEN:
    raise Exception("API_TOKEN environment variable is not set!")

print("API_TOKEN:", API_TOKEN)  # Debug məqsədli

# Bot və dispatcher yaradılır
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Start komandası üçün cavab
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 CaspianCoin Al", web_app=WebAppInfo(url="https://caspiancoin.gumroad.com/l/oxnhw"))]
    ])
    await message.answer(
        text="🌊 *CaspianCoin* — Xəzərdən ilhamlanan rəqəmsal valyuta\n\nAşağıdakı düyməyə kliklə!",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

# Webhook başladıqda
async def on_startup(app):
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook("https://caspiancoin-bot-4.onrender.com/")

# Webhook dayandıqda
async def on_shutdown(app):
    await bot.delete_webhook()

# Telegram webhook handler
async def handle(request):
    update = await request.json()
    print("Gələn mesaj:", update)
    telegram_update = types.Update(**update)
    await dp.process_update(telegram_update)
    return web.Response(text="OK")

# Aiohttp tətbiqi
app = web.Application()
app.router.add_post("/", handle)
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

# Proqramın başlanğıcı
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    web.run_app(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
