import os
print("API_TOKEN:", os.getenv("API_TOKEN"))

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiohttp import web

API_TOKEN = os.getenv("API_TOKEN")  # Tokeni environment variable-dan oxuyuruq

if not API_TOKEN:
    raise Exception("API_TOKEN environment variable is not set!")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

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

async def on_startup(app):
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook("https://caspiancoin-bot-4.onrender.com/")

async def on_shutdown(app):
    await bot.delete_webhook()

async def handle(request):
    update = await request.json()
    TelegramUpdate = types.Update(**update)
    await dp.process_update(TelegramUpdate)
    return web.Response(text="OK")

app = web.Application()
app.router.add_post("/", handle)
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    web.run_app(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
