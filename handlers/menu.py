from aiogram.filters.callback_data import CallbackData
from keyboards.inline import dish_card_keyboard, all_cards_in_category_keyboard
from aiogram import Router, F, types
from aiogram.types import InputMediaPhoto
from database.models import get_dishes, add_to_cart, get_user_cart, del_from_cart

menu_router = Router()


@menu_router.callback_query(F.data == "menu")
async def on_btn_menu(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    user_id = callback.from_user.id
    await send_card_of_category(callback.message, "Салаты", 0, user_id)


@menu_router.callback_query(F.data[:9] == "back_card")
async def on_btn_back_card(callback: types.CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    category = callback.data.split("_")[2]
    dish_num = int(callback.data.split("_")[3])
    max_dish_num = int(callback.data.split("_")[4])
    dish_num = dish_num if dish_num >= 0 else max_dish_num
    await edit_card_of_category(callback.message, category, dish_num, user_id)


@menu_router.callback_query(F.data[:9] == "next_card")
async def on_btn_next_card(callback: types.CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    category = callback.data.split("_")[2]
    dish_num = int(callback.data.split("_")[3])
    max_dish_num = int(callback.data.split("_")[4])
    dish_num = dish_num if dish_num <= max_dish_num else 0
    await edit_card_of_category(callback.message, category, dish_num, user_id)


@menu_router.callback_query(F.data[:20] == "show_all_in_category")
async def on_btn_show_all_in_caterory(callback: types.CallbackQuery):
    category = callback.data.split("_")[4]
    curent_num = int(callback.data.split("_")[5])
    await callback.message.delete()
    await callback.message.answer(text=f"📁 Выберете блюдо из категории {category}", reply_markup=(all_cards_in_category_keyboard(category, curent_num)))


@menu_router.callback_query(F.data[:21] == "show_card_of_category")
async def on_show_card(callback: types.CallbackQuery):
    category = callback.data.split("_")[4]
    dish_num = int(callback.data.split("_")[5])
    user_id = callback.from_user.id
    await callback.message.delete()
    await send_card_of_category(callback.message, category, dish_num, user_id)


@menu_router.callback_query(F.data[:11] == "add_to_cart")
async def on_add_to_cart(callback: types.CallbackQuery):
    card_id = int(callback.data.split("_")[3])
    card_ammount = int(callback.data.split("_")[4])
    category = callback.data.split("_")[5]
    num_in_category = int(callback.data.split("_")[6])
    cur_card_ammount = await add_to_cart(callback.from_user.id, card_id, card_ammount)
    await callback.message.edit_reply_markup(reply_markup=(dish_card_keyboard(category, num_in_category, cur_card_ammount)))


@menu_router.callback_query(F.data[:11] == "del_to_cart")
async def on_add_to_cart(callback: types.CallbackQuery):
    card_id = int(callback.data.split("_")[3])
    card_ammount = int(callback.data.split("_")[4])
    category = callback.data.split("_")[5]
    num_in_category = int(callback.data.split("_")[6])
    cur_card_ammount = await del_from_cart(callback.from_user.id, card_id, card_ammount)
    await callback.message.edit_reply_markup(reply_markup=(dish_card_keyboard(category, num_in_category, cur_card_ammount)))


async def send_card_of_category(message: types.Message, category, num_in_category, user_id: int):
    dish_info = get_dishes(category, num_in_category)
    dish_id = int(dish_info[0])
    dish_name = dish_info[1]
    dish_description = dish_info[2]
    dish_photo = dish_info[3]
    category = dish_info[4]
    dish_price = dish_info[5]
    dish_time = dish_info[6]
    cur_card_ammount_in_cart = (await get_user_cart(user_id)).get(dish_id, 0)
    await message.answer_photo(photo=dish_photo, caption=f"""
<blockquote expandable>🍽 {dish_name}
💵 Стоимость: {dish_price} р
⌛ Время приготовления {dish_time} мин

️️️📝 Описание:️📝 {dish_description}

</blockquote>
""", parse_mode="html", reply_markup=(dish_card_keyboard(category, num_in_category, cur_card_ammount_in_cart)))


async def edit_card_of_category(message: types.Message, category, num_in_category, user_id):
    dish_info = get_dishes(category, num_in_category)
    dish_id = int(dish_info[0])
    dish_name = dish_info[1]
    dish_description = dish_info[2]
    dish_photo = dish_info[3]
    category = dish_info[4]
    dish_price = dish_info[5]
    dish_time = dish_info[6]
    cur_card_ammount_in_cart = (await get_user_cart(user_id)).get(dish_id, 0)
    await message.edit_media(InputMediaPhoto(media=dish_photo, caption=f"""
<blockquote expandable>🍽 {dish_name}
💵 Стоимость: {dish_price} р
⌛ Время приготовления {dish_time} мин

️️️📝 Описание:️📝 {dish_description}

</blockquote>
""", parse_mode="html"), reply_markup=(dish_card_keyboard(category, num_in_category, cur_card_ammount_in_cart)))


# @menu_router.message(F.text)
# async def photo_handler(message):
#     print(message.text)
#
#
# @menu_router.message(F.photo)
# async def photo_handler(message):
#     print(message.photo[-1])
