from aiogram import BaseMiddleware
from aiogram.types import Message
from database.models import add_user


class RegisterMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        user = event.from_user
        await add_user(user.id, user.username)
        return await handler(event, data)
