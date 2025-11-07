from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandObject
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

BOT_TOKEN = "8300246817:AAEWYptTIHhhMjYjvzy9x6B3jzEMX6h5k2U"
WEBAPP_URL = "https://telegramchristmass.netlify.app/"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

ADMIN_ID = 731475622


# ✅ Головне меню
def get_main_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎄 Відкрити Christmas Mini-App",
                    web_app=types.WebAppInfo(url=WEBAPP_URL)
                )
            ],
            [
                InlineKeyboardButton(
                    text="ℹ️ Допомога",
                    callback_data="show_help"
                )
            ]
        ]
    )


# ✅ Кнопка гри для екрана допомоги
def get_game_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎄 Відкрити Christmas Mini-App",
                    web_app=types.WebAppInfo(url=WEBAPP_URL)
                )
            ]
        ]
    )


# ✅ Команда /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    caption = (
        "🎅 **Ласкаво просимо до Christmas Mini-App!**\n\n"
        "Прикрашай ялинку 🎄, збирай іграшки 🎁 і змагайся з друзями!\n\n"
        "Натисни кнопку нижче, щоб розпочати гру 👇"
    )

    try:
        photo = FSInputFile("assets/Intro.png")
        await message.answer_photo(
            photo=photo,
            caption=caption,
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
    except FileNotFoundError:
        await message.answer(
            caption,
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )


# ✅ Кнопка "ℹ️ Допомога"
@dp.callback_query(lambda c: c.data == "show_help")
async def show_help_callback(callback: types.CallbackQuery):
    await callback.message.answer(
        "ℹ️ **Як грати:**\n\n"
        "1️⃣ Кожного дня ви маєте змогу отримати гроші, натиснувши на коробку.\n"
        "2️⃣ Іграшки можна купувати в магазині!\n"
        "3️⃣ Натискай на іграшку — буде звук! 🎁\n"
        "4️⃣ Затисни палець на іграшці та переміщай її 🖐️\n\n"
        "Натисни кнопку нижче, щоб розпочати гру 👇",
        parse_mode="Markdown",
        reply_markup=get_game_button()
    )
    await callback.answer()  # закриває "Loading..." у Telegram


# ✅ /post — оновлення від адміністратора
@dp.message(Command("post"))
async def post_update(message: types.Message, command: CommandObject):
    if message.from_user.id != ADMIN_ID:
        await message.answer("🚫 У тебе немає прав на цю команду.")
        return

    text = command.args
    if not text:
        await message.answer("❗️Використання: `/post Текст повідомлення`", parse_mode="Markdown")
        return

    photo_path = "assets/Update.png"

    try:
        photo = FSInputFile(photo_path)
        await message.answer_photo(
            photo=photo,
            caption=text,
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
    except FileNotFoundError:
        await message.answer(
            text,
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )


# ✅ Запуск бота
async def main():
    print("✅ Bot is running... (Press Ctrl+C to stop)")
    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await dp.start_polling(bot, timeout=10)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
