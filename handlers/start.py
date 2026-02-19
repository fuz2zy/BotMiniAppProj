from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.inline import start_keyboard
from database.models import get_photos

start_router = Router()


@start_router.message(Command("start"))
async def start_handler(message: Message):

    await message.answer_photo((await get_photos("start_photo")).last, caption=f"""
<i>Привет, <b>{message.from_user.first_name}!</b></i> ☺

<i>Рады видеть тебя в нашем кафе <b>DEJAVU</b>, <b>свежие блюда, быстра доставка, дружелюбное обслуживание <u>ждут тебя</u>!</b></i> 🔥

<i>Для начала предлгаю ознакомиться с нашим меню.</i> 🍽️""", parse_mode="html", reply_markup=start_keyboard)

