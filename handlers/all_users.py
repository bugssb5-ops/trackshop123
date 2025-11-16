from aiogram import types, Dispatcher, F
from aiogram.filters import Command
from bot_data import bot, db, shop_name, admin_chat, profile_photo_path, bot_username
from aiogram.enums import ParseMode
from markups import get_main_menu
import os


async def send_profile_with_photo(user_id, message=None):
    user_data = db.get_client_data(user_id)
    balance = user_data[1] if user_data else 0

    # Уникальная реферальная ссылка для каждого пользователя
    user_ref_link = f"https://t.me/{bot_username}?start=ref_{user_id}"

    profile_text = f"""🏆 **Профиль:**

Рейтинг магазина: ★ 4.3 (869 шт.)
Ваш рейтинг: ★ 5.00 (0 шт.)

📍 Ваша страна: Россия
📍 Ваш город: Великий Новгород
🛍 Заказов/покупок: 0
🎯 Скидка: 0 %

👥 Приглашено: 0
💰 Бонус: 0 USD

💰 Баланс: {balance} руб

🔗 Пригласи друга и получи бонус:
{user_ref_link}"""

    # Проверяем существует ли фото профиля
    if os.path.exists(profile_photo_path):
        await message.answer_photo(
            photo=types.FSInputFile(profile_photo_path),
            caption=profile_text,
            reply_markup=get_main_menu()
        )
    else:
        # Если фото нет, отправляем только текст
        await message.answer(profile_text, reply_markup=get_main_menu())


async def command_start(message: types.Message):
    if message.from_user.username is None:
        await message.answer(
            "У вас не установлен <b>username</b>\n\nУстановите его, потом введите /start",
            parse_mode=ParseMode.HTML
        )
        return

    if not db.client_exist(message.from_user.id):
        db.add_client(message.from_user.id)
        await send_profile_with_photo(message.from_user.id, message=message)

    elif db.get_client_data(message.from_user.id)[2] != "ban":
        await send_profile_with_photo(message.from_user.id, message=message)

    else:
        await message.answer(
            f"❌ Ваша учетная запись заблокирована.\n\n"
            f"Свяжитесь с админом: @{admin_chat}",
            parse_mode=ParseMode.HTML
        )


def register_handlers_verification(dp: Dispatcher):
    dp.message.register(command_start, Command("start"))
