import os
import json
import asyncio
from pathlib import Path
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandObject
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from google.cloud import firestore

# =============================
# 🔑 Налаштування
# =============================

BOT_TOKEN = "8300246817:AAEWYptTIHhhMjYjvzy9x6B3jzEMX6h5k2U"
WEBAPP_URL = "https://telegramchristmass.netlify.app/"
SUGGEST_URL = "https://docs.google.com/forms/d/e/1FAIpQLSf0hhijdz8upqx0umgQ6kNZp5UjpAdjn3n8cedKWKvGKbjlrQ/viewform?usp=sharing&ouid=101691539867638061155"  # 👈 заміни на своє посилання
ADMIN_ID = 731475622  # 👈 твій Telegram ID


# =============================
# 🧩 Ініціалізація Firestore
# =============================

def init_firestore():
    """Автоматичне підключення до Firestore з ENV або локального файлу."""
    creds_json = os.getenv("FIREBASE_KEY")

    if creds_json:
        try:
            creds = json.loads(creds_json)
            print("✅ Firestore підключено через змінну середовища.")
            return firestore.Client.from_service_account_info(creds)
        except Exception as e:
            print(f"⚠️ Помилка при зчитуванні FIREBASE_KEY: {e}")

    local_key_path = Path("assets/firebase-key.json")
    if local_key_path.exists():
        try:
            print("✅ Firestore підключено через локальний файл firebase-key.json.")
            return firestore.Client.from_service_account_json(str(local_key_path))
        except Exception as e:
            print(f"❌ Не вдалося підключитись через локальний файл: {e}")
            raise
    else:
        raise FileNotFoundError("❌ Не знайдено FIREBASE_KEY або firebase-key.json")


db = init_firestore()


# =============================
# 🤖 Ініціалізація бота
# =============================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# =============================
# 🎛️ Глобальні кнопки
# =============================

def get_global_buttons():
    """Універсальні inline-кнопки для всіх повідомлень."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎄 Відкрити Christmas Mini-App",
                    web_app=types.WebAppInfo(url=WEBAPP_URL)
                )
            ],
            [
                InlineKeyboardButton(text="🎁 Запропонувати нову іграшку", url=SUGGEST_URL),
                InlineKeyboardButton(text="ℹ️ Допомога", callback_data="show_help")
            ]
        ]
    )


# =============================
# 🧑‍🎄 Команда /start
# =============================

@dp.message(Command("start"))
async def start_command(message: types.Message):
    user_id = str(message.from_user.id)
    username = message.from_user.username or "Unknown"

    # ✅ Запис користувача у Firestore
    user_ref = db.collection("users").document(user_id)
    user_ref.set({
        "userId": int(user_id),
        "userName": username,
    }, merge=True)

    caption = (
        "🎅 **Ласкаво просимо до Christmas Mini-App!**\n\n"
        "Прикрашай ялинку 🎄, збирай іграшки 🎁 та ділися святковим настроєм!\n\n"
        "Натисни кнопку нижче, щоб розпочати гру 👇"
    )

    try:
        photo = FSInputFile("assets/Intro.png")
        await message.answer_photo(
            photo=photo,
            caption=caption,
            parse_mode="Markdown",
            reply_markup=get_global_buttons()
        )
    except FileNotFoundError:
        await message.answer(
            caption,
            parse_mode="Markdown",
            reply_markup=get_global_buttons()
        )


# =============================
# ℹ️ Допомога (callback)
# =============================

@dp.callback_query(lambda c: c.data == "show_help")
async def show_help_callback(callback: types.CallbackQuery):
    await callback.message.answer(
        "ℹ️ **Як грати у Christmas Mini-App:**\n\n"
        "1️⃣ Натисни '🎄 Відкрити Christmas Mini-App'.\n"
        "2️⃣ Заробляй монети 🎁.\n"
        "3️⃣ Купуй нові іграшки 🛍️.\n"
        "4️⃣ Натискай на іграшку — вона видає звук 🔊.\n"
        "5️⃣ Перетягуй іграшки на ялинку 🖐️.\n\n"
        "🎄 Веселих свят!",
        parse_mode="Markdown",
        reply_markup=get_global_buttons()
    )
    await callback.answer()


# =============================
# 📣 /post — розсилка всім користувачам
# =============================

@dp.message(Command("post"))
async def post_update(message: types.Message, command: CommandObject):
    if message.from_user.id != ADMIN_ID:
        await message.answer("🚫 У тебе немає прав на цю команду.")
        return

    text = command.args or "🎉 Нове оновлення у Christmas Mini-App!"
    photo_path = "assets/Update.png"

    users_ref = db.collection("users").stream()
    user_ids = [int(u.id) for u in users_ref]

    await message.answer(f"📨 Надсилаю оновлення {len(user_ids)} користувачам...")

    sent = 0
    for user_id in user_ids:
        try:
            if Path(photo_path).exists():
                photo = FSInputFile(photo_path)
                await bot.send_photo(
                    chat_id=user_id,
                    photo=photo,
                    caption=text,
                    parse_mode="Markdown",
                    reply_markup=get_global_buttons()
                )
            else:
                await bot.send_message(
                    chat_id=user_id,
                    text=text,
                    parse_mode="Markdown",
                    reply_markup=get_global_buttons()
                )
            sent += 1
            await asyncio.sleep(0.05)  # трохи паузи, щоб уникнути flood
        except Exception as e:
            print(f"❌ Не вдалося надіслати користувачу {user_id}: {e}")

    await message.answer(f"✅ Успішно відправлено {sent}/{len(user_ids)} користувачам.")


# =============================
# 🧩 Будь-яке інше повідомлення
# =============================

@dp.message()
async def fallback_message(message: types.Message):
    await message.answer("🎄 Обери дію нижче:", reply_markup=get_global_buttons())


# =============================
# 🚀 Запуск
# =============================

async def main():
    print("✅ Bot is running... (Press Ctrl+C to stop)")
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot, timeout=10)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
