from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext
from bot_data import bot, db, shop_name, admin_chat, product_data, reviews_data, current_user_city, profile_photo_path, \
    admin_id, card_payment_message, bot_username
from markups import *
import asyncio
import os

router = Router()


# Главное меню с фото профиля
async def send_profile_with_photo(user_id, callback=None):
    user_data = db.get_client_data(user_id)
    balance = user_data[1] if user_data else 0

    # Уникальная реферальная ссылка для каждого пользователя
    user_ref_link = f"https://t.me/{bot_username}?start=ref_{user_id}"

    profile_text = f"""🏆 **Профиль:**

Рейтинг магазина: ★ 4.3 (865 шт.)
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
        if callback:
            await callback.message.answer_photo(
                photo=types.FSInputFile(profile_photo_path),
                caption=profile_text,
                reply_markup=get_main_menu()
            )
        else:
            # Для обработчика /start
            pass
    else:
        # Если фото нет, отправляем только текст
        if callback:
            await callback.message.answer(profile_text, reply_markup=get_main_menu())
        else:
            # Для обработчика /start
            pass


# Обработка главного меню
@router.callback_query(F.data == "back_main")
async def back_to_main_handler(callback: types.CallbackQuery):
    await callback.message.delete()
    await send_profile_with_photo(callback.from_user.id, callback=callback)


# Пополнение баланса из главного меню
@router.callback_query(F.data == "deposit")
async def deposit_main_handler(callback: types.CallbackQuery):
    user_balance = db.get_client_data(callback.from_user.id)[1]

    deposit_text = f"""💳 **Пополнение баланса**

💰 Ваш текущий баланс: {user_balance} руб

Выберите способ пополнения:"""

    await callback.message.answer(
        deposit_text,
        reply_markup=get_deposit_menu()
    )


# Назад к товарам
@router.callback_query(F.data == "back_products")
async def back_to_products_handler(callback: types.CallbackQuery):
    city_name = current_user_city.get(callback.from_user.id, "")
    if city_name:
        await callback.message.answer(
            f"🏙 Город: {city_name}\n\nВыберите товар:",
            reply_markup=get_products_menu("", callback.from_user.id)
        )
    else:
        await callback.message.answer(
            "📍 Выберите ваш город:",
            reply_markup=get_cities_menu()
        )


# Локации
@router.callback_query(F.data == "locations")
async def locations_handler(callback: types.CallbackQuery):
    await callback.message.answer(
        "📍 Выберите ваш город:",
        reply_markup=get_cities_menu()
    )


# Бонусы
@router.callback_query(F.data == "bonuses")
async def bonuses_handler(callback: types.CallbackQuery):
    # Уникальная реферальная ссылка для каждого пользователя
    user_ref_link = f"https://t.me/{bot_username}?start=ref_{callback.from_user.id}"

    bonuses_text = f"""🫂 Приглашай друзей и получай 10% с каждой их покупки. Чем больше друзей — тем больше твой доход! Просто делись ссылкой, и зарабатывай на их покупках.

🔗 Твоя реферальная ссылка:
{user_ref_link}"""

    await callback.message.answer(
        bonuses_text,
        reply_markup=get_bonuses_menu()
    )


# Работа
@router.callback_query(F.data == "work")
async def work_handler(callback: types.CallbackQuery):
    work_text = f"""💼 **Работа в {shop_name}**

Наш магазин ведет постоянный набор по всей РФ.

📋 Открыты вакансии:
• Кладмен (от 1100 руб/клад)
• Трафаретчик (от 150-300 руб/рисунок)
• Перевозчик (только с залогом)
• Склад (только с залогом)

🤝 Также приглашаем к сотрудничеству химиков и гроверов с качественным товаром.

📞 Для связи: @{admin_chat} с пометкой 'Работа'"""

    await callback.message.answer(
        work_text,
        reply_markup=get_work_menu()
    )


# Отзывы - показываем по одному
@router.callback_query(F.data == "reviews")
async def reviews_handler(callback: types.CallbackQuery):
    await show_reviews_page(callback, 0)


@router.callback_query(F.data.startswith("reviews_"))
async def reviews_pagination_handler(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[1])
    await show_reviews_page(callback, page)


async def show_reviews_page(callback: types.CallbackQuery, page: int):
    if page < 0:
        page = 0
    if page >= len(reviews_data):
        page = len(reviews_data) - 1

    review = reviews_data[page]

    # Для пустых отзывов (после 30-го) показываем другое сообщение
    if page >= 30:
        reviews_text = f"""⭐ **Отзывы о магазине**

📊 Всего отзывов: 865

🟡 ★★★★★

💬 Отзыв скрыт

👤 Пользователь

📄 {page + 1}/865"""
    else:
        reviews_text = f"""⭐ **Отзывы о магазине**

📊 Всего отзывов: 865

🟡 {review['rating']}

💬 {review['text']}

👤 Пользователь

📄 {page + 1}/865"""

    await callback.message.answer(
        reviews_text,
        reply_markup=get_reviews_menu(page, 865)
    )


# Обработка выбора города
@router.callback_query(F.data.startswith("city_"))
async def city_callback_handler(callback: types.CallbackQuery):
    city_name = callback.data.split("_")[1]
    current_user_city[callback.from_user.id] = city_name
    await callback.message.answer(
        f"🏙 Выбран город: {city_name}\n\nВыберите район:",
        reply_markup=get_zones_menu(city_name, callback.from_user.id)
    )


# Обработка выбора района
@router.callback_query(F.data.startswith("zone_"))
async def zone_callback_handler(callback: types.CallbackQuery):
    zone_name = callback.data.split("_")[1]
    city_name = current_user_city.get(callback.from_user.id, "выбранном городе")
    await callback.message.answer(
        f"📍 Выбран район: {zone_name}\n🏙 Город: {city_name}\n\nВыберите товар:",
        reply_markup=get_products_menu(zone_name, callback.from_user.id)
    )


# Обработка выбора товара
@router.callback_query(F.data.startswith("product_"))
async def product_callback_handler(callback: types.CallbackQuery):
    product_name = callback.data.split("_")[1]
    product_info = product_data.get(product_name, {})

    # Получаем текущий город пользователя
    city_name = current_user_city.get(callback.from_user.id, "выбранном городе")

    text = f"🛒 {product_name}\n\n{product_info.get('description', 'Описание товара')}\n\n📍 В наличии в {city_name}\n\nВыберите фасовку:"

    # Пытаемся отправить фото с компьютера
    photo_file = product_info.get("photo")
    if photo_file and os.path.exists(photo_file):
        try:
            await callback.message.answer_photo(
                photo=types.FSInputFile(photo_file),
                caption=text,
                reply_markup=get_prices_menu(product_name)
            )
            return
        except Exception as e:
            print(f"Ошибка загрузки фото {photo_file}: {e}")

    # Если фото нет или ошибка - отправляем только текст
    await callback.message.answer(
        text,
        reply_markup=get_prices_menu(product_name)
    )


# Обработка выбора цены
@router.callback_query(F.data.startswith("price_"))
async def price_callback_handler(callback: types.CallbackQuery):
    price_text = callback.data.split("_")[1]

    # Извлекаем цену из текста (например: "0.5г (4200 руб)" -> 4200)
    try:
        price_value = int(price_text.split("(")[1].split(" руб")[0])
    except:
        price_value = 0

    user_balance = db.get_client_data(callback.from_user.id)[1]

    if price_value <= user_balance:
        await callback.message.answer(
            f"✅ Товар успешно приобретен!\n\n{price_text}\n\nСредства списаны с вашего баланса.",
            reply_markup=get_back_to_main()
        )
    else:
        await callback.message.answer(
            f"❌ Недостаточно средств!\n\nДля покупки {price_text} необходимо пополнить счет.\n\nБаланс: {user_balance} руб",
            reply_markup=get_deposit_menu()
        )


# Пополнение баланса
@router.callback_query(F.data.startswith("deposit_"))
async def deposit_callback_handler(callback: types.CallbackQuery):
    method = callback.data.split("_")[1]

    if method == "card":
        await callback.message.answer(
            card_payment_message,
            reply_markup=get_back_to_main()
        )
    elif method in ["bitcoin", "usdt"]:
        msg = await callback.message.answer(
            "⏳ Подбираем актуальный адрес кошелька...",
            reply_markup=None
        )

        await asyncio.sleep(1.5)

        if method == "bitcoin":
            address = "bc1q7ygl7d2lp2yzsylwgjrshd2eap45a6lzvpkfaa"
            text = f"""₿ Оплата Bitcoin

Адрес для пополнения:
`{address}`

После оплаты нажмите кнопку "✅ Оплатил"

С уважением, команда icelab 🧊"""
        else:
            address = "UQAG2zu2uhQ6vhZNOWMfMG2o1HhiA31PLnLJnfB09FEfrIYV"
            text = f"""💎 Оплата USDT

Адрес для пополнения:
`{address}`

⚠️ ВАЖНО: USDT переводятся СТРОГО в сети TON (The Open Network)

После оплаты нажмите кнопку "✅ Оплатил"

С уважением, команда icelab 🧊"""

        await msg.edit_text(text, reply_markup=get_check_deposit())


# Подтверждение оплаты
@router.callback_query(F.data == "paid")
async def paid_handler(callback: types.CallbackQuery):
    await callback.message.answer(
        "✅ Ваша оплата принята в обработку. Ожидайте зачисления средств на баланс в течение 15-30 минут.",
        reply_markup=get_back_to_main()
    )


# Отмена
@router.callback_query(F.data == "cancel")
async def cancel_handler(callback: types.CallbackQuery):
    await callback.message.delete()
    await send_profile_with_photo(callback.from_user.id, callback=callback)


# Админ панель
@router.message(F.text == "/admin")
async def admin_handler(message: types.Message):
    if message.from_user.id in admin_id:
        await message.answer("👨‍💼 Админ панель", reply_markup=get_admin_menu())
    else:
        await message.answer("❌ Доступ запрещен")


# Админ команды
@router.callback_query(F.data == "admin_count")
async def admin_count_handler(callback: types.CallbackQuery):
    if callback.from_user.id in admin_id:
        users_count = len(db.get_all_client())
        await callback.message.answer(
            f"📊 В системе {users_count} пользователей",
            reply_markup=get_admin_menu()
        )


def register_handlers_client(dp):
    dp.include_router(router)