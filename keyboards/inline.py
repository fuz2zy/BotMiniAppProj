from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.models import get_dishes


start_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Меню 🍽", callback_data="menu")],
        [InlineKeyboardButton(text="Корзина 🛒", callback_data="my_cart")],
        [InlineKeyboardButton(text="Помощь ❔", callback_data="help")]])

menu_button_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню 🍽", callback_data="menu")]])


def cart_keyboard():
    pass


webapp_keyboard = ReplyKeyboardMarkup(keyboard=[[
    KeyboardButton(text="Открыть меню", web_app=WebAppInfo(url="https://tg-mini-app-proj.vercel.app"))
]], resize_keyboard=True)


def dish_card_keyboard(category, num_in_category, cur_cart_ammount=0):
    dishes = get_dishes(category)
    dish_id = dishes[num_in_category][0]

    if not cur_cart_ammount:
        curt_button_row = [InlineKeyboardButton(text="Добавить в коорзину 🛒", callback_data=f"add_to_cart_{dish_id}_1_{category}_{num_in_category}")]
    else:
        curt_button_row = [
            InlineKeyboardButton(text=f"-", callback_data=f"del_to_cart_{dish_id}_1_{category}_{num_in_category}"),
            InlineKeyboardButton(text=f"🛒 {cur_cart_ammount}", callback_data=f"my_cart"),
            InlineKeyboardButton(text=f"+", callback_data=f"add_to_cart_{dish_id}_1_{category}_{num_in_category}")]

    return InlineKeyboardMarkup(inline_keyboard=[
        curt_button_row,
        [InlineKeyboardButton(text="« Назад", callback_data=f"back_card_{category}_{num_in_category - 1}_{len(dishes) - 1}"),
         InlineKeyboardButton(text=f"☰{num_in_category + 1}/{len(dishes)}", callback_data=f"show_all_in_category_{category}_{num_in_category}"),
         InlineKeyboardButton(text="Вперед »", callback_data=f"next_card_{category}_{num_in_category + 1}_{len(dishes) - 1}")
         ]
    ])


def all_cards_in_category_keyboard(category, curent_num):
    dishes = get_dishes(category)
    builder = InlineKeyboardBuilder()
    dish_num = 0
    for dish in dishes:
        dish_header = f"🍽 {dish[1]} {dish[5]} р"
        if dish_num == curent_num:
            dish_header = f"👉🍽 {dish[1]} {dish[5]} р"
        builder.button(text=dish_header, callback_data=f"show_card_of_category_{dish[4]}_{dish_num}")
        dish_num += 1
    builder.adjust(1)
    return builder.as_markup()
