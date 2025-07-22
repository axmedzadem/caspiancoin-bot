import asyncio
import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

API_TOKEN = "8106051015:AAG0rPQmyWAhBEIOi_kqZjMGyls0nuZOWso"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def get_balance(user_id):
    try:
        with open("balance.json", "r") as f:
            balances = json.load(f)
        return balances.get(str(user_id), 0)
    except:
        return 0

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer("🌊 Xoş gəldin! CaspianCoin botuna xoş gəlmisən.\nKomandalar:\n/balance – balansını yoxla")

@dp.message(Command("balance"))
async def check_balance(message: types.Message):
    user_id = message.from_user.id
    balance = get_balance(user_id)
    await message.answer(f"💰 Sənin CaspianCoin balansın: {balance} $CSP")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
