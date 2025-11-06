from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandObject
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

BOT_TOKEN = "8300246817:AAEWYptTIHhhMjYjvzy9x6B3jzEMX6h5k2U"
WEBAPP_URL = "https://telegramchristmass.netlify.app/"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

ADMIN_ID = 731475622

@dp.message(Command("start"))
async def start_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(
                    text="🎄 Відкрити Christmas Mini-App",
                    web_app=types.WebAppInfo(url=WEBAPP_URL)
                )
            ],
            [types.KeyboardButton(text="ℹ️ Допомога")]
        ],
        resize_keyboard=True
    )

    caption = (
        "🎅 **Ласкаво просимо до Christmas Mini-App!**\n\n"
        "Збирай іграшки, прикрашай ялинку 🎄 та ділися святковим настроєм з друзями!\n\n"
        "Натисни кнопку нижче, щоб розпочати гру 👇"
    )

    photo = FSInputFile("assets/Intro.png")

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

@dp.message(Command("post"))
async def post_update(message: types.Message, command: CommandObject):
    # 🔐 Перевірка на власника
    if message.from_user.id != ADMIN_ID:
        await message.answer("🚫 У тебе немає прав на цю команду.")
        return

    text = command.args
    if not text:
        await message.answer("❗️Використання: `/post Текст повідомлення`", parse_mode="Markdown")
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎄 Відкрити Christmas Mini-App",
                    web_app=types.WebAppInfo(url=WEBAPP_URL)
                )
            ]
        ]
    )

    photo_path = "assets/Update.png"

    try:
        photo = FSInputFile(photo_path)
        await message.answer_photo(
            photo=photo,
            caption=text,
            parse_mode="Markdown",
            reply_markup=keyboard
        )
    except FileNotFoundError:
        await message.answer(text, parse_mode="Markdown", reply_markup=keyboard)



async def main():
    print("✅ Bot is running... (Press Ctrl+C to stop)")

    # 🔹 Очищаємо старі webhook-и перед polling
    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await dp.start_polling(bot, timeout=10)
    finally:
        await bot.session.close()  # 🔹 Гарантовано закриваємо сесію при виході


if __name__ == "__main__":
    asyncio.run(main())
