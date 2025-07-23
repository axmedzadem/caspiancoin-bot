from flask import Flask, request, Response
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
import asyncio
import logging
from aiogram.utils.webhook import start_webhook

API_TOKEN = "BOT_TOKENUNU_BURA_YAZ"

WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://caspiancoin-bot-4.onrender.com{WEBHOOK_PATH}"

app = Flask(__name__)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(types.filters.Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Salam! Bot webhook serveri işləyir.")

@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook_handler():
    update = Update.model_validate(request.json)
    asyncio.create_task(dp.feed_update(bot, update))
    return Response(status=200)

@app.route("/", methods=["GET"])
def index():
    return "✅ Bot Webhook Server is Running"

async def on_startup():
    await bot.delete_webhook()
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown():
    await bot.delete_webhook()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    config = Config()
    config.bind = ["0.0.0.0:8000"]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(on_startup())
    loop.run_until_complete(serve(app, config))
