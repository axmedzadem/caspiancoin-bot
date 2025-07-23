import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

API_TOKEN = os.getenv("API_TOKEN")
WEBHOOK_PATH = "/"
WEBHOOK_HOST = os.getenv("RENDER_EXTERNAL_URL", "https://caspiancoin-bot-4.onrender.com")
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("🌊 CaspianCoin — Xəzər dənizindən ilhamlanan, yerli və dayanıqlı rəqəmsal valyuta.")

async def on_startup(app: web.Application):
    await bot.set_webhook(WEBHOOK_URL)
    print("✅ Webhook quruldu:", WEBHOOK_URL)

async def on_shutdown(app: web.Application):
    await bot.delete_webhook()
    await bot.session.close()

app = web.Application()
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
setup_application(app, dp, bot=bot)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
