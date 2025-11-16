from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot_data import any_data, admin_chat


# Главное меню с кнопкой Оператор и Пополнить баланс
def get_main_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="📍 ЛОКАЦИИ", callback_data="locations"))
    keyboard.add(InlineKeyboardButton(text="💰 ПОПОЛНИТЬ БАЛАНС", callback_data="deposit"))
    keyboard.add(InlineKeyboardButton(text="🎁 БОНУСЫ", callback_data="bonuses"))
    keyboard.add(InlineKeyboardButton(text="💼 РАБОТА", callback_data="work"))
    keyboard.add(InlineKeyboardButton(text="⭐ ОТЗЫВЫ", callback_data="reviews"))
    keyboard.add(InlineKeyboardButton(text="👨‍💼 ОПЕРАТОР", url=f"https://t.me/{icelab_manager1}"))
    keyboard.adjust(2)
    return keyboard.as_markup()


# Админ меню
def get_admin_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="📊 Подсчет мамонтов", callback_data="admin_count"))
    keyboard.add(InlineKeyboardButton(text="📢 Рассылка", callback_data="admin_mailing"))
    keyboard.add(InlineKeyboardButton(text="🔨 Бан пользователя", callback_data="admin_ban"))
    keyboard.add(InlineKeyboardButton(text="🔓 Разбан пользователя", callback_data="admin_unban"))
    keyboard.adjust(2)
    return keyboard.as_markup()


# Способы оплаты
def get_deposit_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="💳 Банк. Картой", callback_data="deposit_card"))
    keyboard.add(InlineKeyboardButton(text="₿ Bitcoin", callback_data="deposit_bitcoin"))
    keyboard.add(InlineKeyboardButton(text="💎 USDT", callback_data="deposit_usdt"))
    keyboard.add(InlineKeyboardButton(text="🔙 Назад", callback_data="back_main"))
    keyboard.adjust(1)
    return keyboard.as_markup()


# Подтверждение оплаты
def get_check_deposit():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="✅ Оплатил", callback_data="paid"))
    keyboard.add(InlineKeyboardButton(text="❌ Отменить", callback_data="cancel"))
    keyboard.adjust(1)
    return keyboard.as_markup()


# Города
def get_cities_menu():
    keyboard = InlineKeyboardBuilder()
    for city in any_data["city"]:
        keyboard.add(InlineKeyboardButton(text=city, callback_data=f"city_{city}"))
    keyboard.add(InlineKeyboardButton(text="🔙 Назад", callback_data="back_main"))
    keyboard.adjust(1)
    return keyboard.as_markup()


# Районы
def get_zones_menu(city_name, user_id):
    from bot_data import current_user_city

    zones = any_data["city_zone"].get(city_name, ["Центр", "Север", "Юг", "Восток", "Запад"])

    keyboard = InlineKeyboardBuilder()
    for zone in zones:
        keyboard.add(InlineKeyboardButton(text=zone, callback_data=f"zone_{zone}"))
    keyboard.add(InlineKeyboardButton(text="🔙 Назад", callback_data="locations"))
    keyboard.adjust(2)
    return keyboard.as_markup()


# Товары
def get_products_menu(zone_name, user_id):
    from bot_data import current_user_city
    city_name = current_user_city.get(user_id, "")

    keyboard = InlineKeyboardBuilder()

    if city_name == "Великий Новгород":
        products = [
            "Амфетамин", "A-PVP кристалы", "Мефедрон кристалы VHQ",
            "Метадон", "Гашиш Ice-o-Lator", "Шишки Gorilla Glue",
            "Экстази"
        ]
    else:
        products = [
            "Кокаин VHQ Apple", "Альфа-PVP кристаллы", "Мефедрон кристаллы",
            "Мефедрон мука", "МДМА", "Марки LSD 250мкг",
            "Гашиш Ice-o-Lator Liverpool", "Шишки Banana Punch",
            "Шишки Gorilla Scittles"
        ]

    for product in products:
        keyboard.add(InlineKeyboardButton(text=product, callback_data=f"product_{product}"))
    keyboard.add(InlineKeyboardButton(text="🔙 Назад", callback_data=f"city_{city_name}"))
    keyboard.adjust(2)
    return keyboard.as_markup()


# Цены/фасовки
def get_prices_menu(product_name):
    prices = any_data["product_price"].get(product_name, [])

    keyboard = InlineKeyboardBuilder()
    for price in prices:
        keyboard.add(InlineKeyboardButton(text=price, callback_data=f"price_{price}"))
    keyboard.add(InlineKeyboardButton(text="🔙 Назад к товарам", callback_data="back_products"))
    keyboard.adjust(1)
    return keyboard.as_markup()


# Рейтинг и отзывы с кнопкой "Оставить отзыв"
def get_reviews_menu(page=0, total_pages=865):
    keyboard = InlineKeyboardBuilder()

    if page > 0:
        keyboard.add(InlineKeyboardButton(text="⬅️ Предыдущий", callback_data=f"reviews_{page - 1}"))

    if page < total_pages - 1:
        keyboard.add(InlineKeyboardButton(text="Следующий ➡️", callback_data=f"reviews_{page + 1}"))

    keyboard.add(InlineKeyboardButton(text="✍️ Оставить отзыв", url=f"https://t.me/{admin_chat}"))
    keyboard.add(InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_main"))
    keyboard.adjust(2)
    return keyboard.as_markup()


# Бонусы меню
def get_bonuses_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_main"))
    return keyboard.as_markup()


# Работа меню
def get_work_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_main"))
    return keyboard.as_markup()


# Назад в главное меню
def get_back_to_main():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_main"))
    return keyboard.as_markup()
