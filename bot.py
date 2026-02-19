from database.db import init_db
from middlewares.reg_middleware import RegisterMiddleware
from middlewares.antispam_middleware import AntispamMiddleware
from database.models import add_admin, load_admins, add_dish, add_photo, add_user, add_to_cart, get_user_cart
from core import dp, bot, message_cooldown, callback_cooldown
from handlers.start import start_router
from handlers.menu import menu_router
import asyncio


async def main():
    await init_db()
    await add_admin(7716932686, "admin")
    await add_user(7716932686, "fuzzy")
    await add_dish("Салат «Оливье»", """
Изысканный салат с богатой историей, названный в честь французского шеф-повара Люсьена Оливье. Идеально сбалансированный ансамбль из отборных продуктов: нежнейшее филе птицы, рассыпчатый картофель, перепелиные яйца и хрустящие корнишоны. Легкая заправка на основе майонеза и дижонской горчицы придает блюду благородную пикантность и неповторимый сливочный вкус
""", "AgACAgIAAxkBAAIBhWmV6MQXuPKjEO2lWx2EtQaAXUN6AAJ4GWsbkjyxSJAAAZYnl_S4RwEAAwIAA3kAAzoE", "Салаты", 30, 30)

    await add_dish("Салат «ливье»", """
Изысканный салат с богатой историей, названный в честь французского шеф-повара Люсьена Оливье. Идеально сбалансированный ансамбль из отборных продуктов: нежнейшее филе птицы, рассыпчатый картофель, перепелиные яйца и хрустящие корнишоны. Легкая заправка на основе майонеза и дижонской горчицы придает блюду благородную пикантность и неповторимый сливочный вкус
        """, "AgACAgIAAxkBAAIBhWmV6MQXuPKjEO2lWx2EtQaAXUN6AAJ4GWsbkjyxSJAAAZYnl_S4RwEAAwIAA3kAAzoE", "Салаты", 20, 30)

    await add_photo("AgACAgIAAxkBAAIBPGmVmfcOXSMlBUzxDCCcG6jq09lfAAKzFWsbvROwSD62Z1CvmJntAQADAgADeQADOgQ", "start_photo")
    await load_admins()

    dp.message.middleware(RegisterMiddleware())
    dp.message.middleware(AntispamMiddleware(message_cooldown, False))

    dp.callback_query.middleware(RegisterMiddleware())
    dp.callback_query.middleware(AntispamMiddleware(callback_cooldown, True))
    
    dp.include_router(start_router)
    dp.include_router(menu_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
