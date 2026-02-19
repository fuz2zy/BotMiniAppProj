from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from keyboards.inline import menu_button_keyboard, cart_keyboard
from database.models import get_user_cart, get_dish

cart_router = Router()


@cart_router.callback_query(F.data == "my_cart")
async def on_call_my_cart(callback: CallbackQuery):
    await callback.message.delete()
    await send_my_cart(callback.message, callback.from_user.id)


@cart_router.message(Command("my_cart"))
async def on_command_my_cart(message: Message):
    await send_my_cart(message, message.from_user.id)


async def send_my_cart(message: Message, user_id):
    user_cart = await get_user_cart(user_id)
    if user_cart == {}:
        await message.answer("<blockquote>Ваша корзина еще  пуста, для начала выберете товары в  меню 🍽</blockquote>", reply_markup=menu_button_keyboard, parse_mode="html")
        return

    cntr = 0
    tot_price = 0
    answ = "🛒 Ваша корзина:"
    for dish_id in user_cart:
        cntr += 1
        dish = get_dish(dish_id)
        tot_price += user_cart[dish_id] * dish[5]
        answ += f"""
<blockquote>{cntr}. {dish[1]}
- {user_cart[dish_id]} шт. * {dish[5]}руб. = {user_cart[dish_id] * dish[5]} руб. </blockquote>
"""
    answ += f"\n 💵 Общая стоимость: {tot_price} руб."
    await message.answer(answ, parse_mode="html")
