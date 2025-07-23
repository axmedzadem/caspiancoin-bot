import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

API_TOKEN = os.getenv("API_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("RENDER_EXTERNAL_URL", "") + WEBHOOK_PATH

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message(Command("start"))
async def start_handler(message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💰 CaspianCoin Al", web_app=WebAppInfo(url="https://caspiancoin.gumroad.com/l/oxnhw"))
        ]
    ])
    await message.answer(
        "🌊 *CaspianCoin* — Xəzərdən ilhamlanan rəqəmsal valyuta\n\nAşağıdakı düyməyə kliklə!",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

async def on_startup():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(WEBHOOK_URL)
    print(f"Webhook set to {WEBHOOK_URL}")

async def on_shutdown():
    await bot.delete_webhook()
    print("Webhook deleted")

async def main():
    await on_startup()

    app = web.Application()
    app.add_routes([web.post(WEBHOOK_PATH, dp.webhook_handler)])

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.getenv("PORT", 8000)))
    await site.start()

    print(f"Server started at {WEBHOOK_URL}")

    try:
        while True:
            await asyncio.sleep(3600)
    except KeyboardInterrupt:
        await on_shutdown()

if __name__ == "__main__":
    asyncio.run(main())
