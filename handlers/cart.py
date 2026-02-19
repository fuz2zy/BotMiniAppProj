from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from keyboards.inline import menu_button_keyboard
from database.models import get_user_cart

cart_router = Router()


@cart_router.message(Command("my_cart"))
async def on_command_my_cart(message: Message):
    user_id = message.from_user.id
    user_cart = await get_user_cart(user_id)
    if user_cart == {}:
        await message.answer("<blockquote>Ваша корзина еще  пуста, для начала выберете товары в  меню 🍽</blockquote>", reply_markup=menu_button_keyboard, parse_mode="html")
        return

