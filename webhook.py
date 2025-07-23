import asyncio
from flask import Flask, request, Response
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
import logging

API_TOKEN = "BOT_TOKENUNU_BURA_YAZ"

app = Flask(__name__)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(types.filters.Command(commands=["start"]))
async def cmd_start(message: types.Message):
    await message.answer(
        "🌊 *CaspianCoin* — Xəzərdən ilhamlanan rəqəmsal valyuta\n\n"
        "Aşağıdakı düyməyə kliklə!",
        parse_mode="Markdown"
    )

@app.route("/", methods=["GET"])
def root():
    return "✅ Bot webhook server is running"

@app.route("/webhook", methods=["POST"])
def webhook_handler():
    update = Update.model_validate(request.json)
    asyncio.create_task(dp.feed_update(bot, update))
    return Response(status=200)

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
    loop.run_until_complete(bot.delete_webhook())
    # Burada webhook set etmək lazım olsa, onu özün API-dən ya manual etməlisən
    loop.run_until_complete(serve(app, config))
