import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from pathlib import Path

BOT_TOKEN = "8300246817:AAEWYptTIHhhMjYjvzy9x6B3jzEMX6h5k2U"
WEBAPP_URL = "https://telegramchristmass.netlify.app/"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(
                    text="🎄 Відкрити Christmas Mini-App",
                    web_app=types.WebAppInfo(url=WEBAPP_URL)
                )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )

    caption = (
        "🎅 **Ласкаво просимо до Christmas Mini-App!**\n\n"
        "Збирай іграшки, прикрашай ялинку 🎄 та ділися святковим настроєм з друзями!\n\n"
        "Натисни кнопку нижче, щоб розпочати гру 👇"
    )

    photo_path = Path("assets/Intro.png")

    with photo_path.open("rb") as photo:
        await message.answer_photo(
            photo=photo,
            caption=caption,
            parse_mode="Markdown",
            reply_markup=keyboard
        )

    @dp.message(lambda msg: msg.text == "ℹ️ Допомога")
    async def help_message(message: types.Message):
        await message.answer(
            "ℹ️ **Як грати:**\n\n"
            "1️⃣ Натисни '🎄 Відкрити Christmas Mini-App'.\n"
            "2️⃣ Грай прямо в Telegram — прикрась свою ялинку!\n"
            "3️⃣ Збирай іграшки, ділися результатом з друзями! 🎁",
            parse_mode="Markdown"
        )

async def main():
    print("✅ Bot is running... (Press Ctrl+C to stop)")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
