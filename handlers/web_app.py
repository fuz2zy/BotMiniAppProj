from aiogram import Router, types, F
import json

web_app_router = Router()


@web_app_router.message(F.web_app_data)
async def on_web_app(message: types.Message):
    data = json.loads(message.web_app_data.data)
    print(data)
    await message.answer(f"Заказ принят {data}")
