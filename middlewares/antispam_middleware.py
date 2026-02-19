from core import user_last_action
from time import time
from aiogram import BaseMiddleware
from aiogram.types import Message


class AntispamMiddleware(BaseMiddleware):

    def __init__(self, cooldown, need_answ):
        self.cooldown = cooldown
        self.need_answ = need_answ

    async def __call__(self, handler, event: Message, data: dict):
        user_id = event.from_user.id
        now = time()
        last = user_last_action.get(user_id, 0)
        if now - last < self.cooldown:
            if self.need_answ:
                await event.answer("⌛ не так быстро!")
            return
        user_last_action[user_id] = now
        return await handler(event, data)
