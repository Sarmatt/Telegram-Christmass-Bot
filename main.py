import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

BOT_TOKEN = "8300246817:AAEWYptTIHhhMjYjvzy9x6B3jzEMX6h5k2U"
WEBAPP_URL = "https://telegramchristmass.netlify.app/"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_command(message: types.Message):
    # ✅ Правильний спосіб створення клавіатури у v3
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(
                text="🎄 Відкрити Christmas Mini-App",
                web_app=types.WebAppInfo(url=WEBAPP_URL)
            )]
        ]
    )

    await message.answer(
        "Вітаю у 🎅 Christmas Mini-App!\nНатисни кнопку нижче, щоб запустити гру:",
        reply_markup=keyboard
    )

async def main():
    print("✅ Bot is running... (Press Ctrl+C to stop)")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
