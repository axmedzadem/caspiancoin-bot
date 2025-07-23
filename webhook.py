import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiohttp import web

print("API_TOKEN:", os.getenv("API_TOKEN"))  # Tokenin gəldiyini yoxlamaq üçün

API_TOKEN = os.getenv("API_TOKEN")
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
    try:
        update = await request.json()
        print("Gələn mesaj:", update)  # Konsola gələn mesajı yazdırırıq
        TelegramUpdate = types.Update(**update)
        await dp.process_update(TelegramUpdate)
    except Exception as e:
        print("Error in handle:", e)
        return web.Response(status=500, text="Internal Server Error")
    return web.Response(text="OK")

app = web.Application()
app.router.add_post("/", handle)
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == "__main__":
    import logging
    logging.basicCon
