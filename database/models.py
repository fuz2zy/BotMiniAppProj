import aiosqlite
from core import admins, logger
from config import db_path


class Photos:
    def __init__(self, data):
        self.all = data
        self.last = data[-1][0] if data else None
        self.first = data[0][0] if data else None


async def load_admins():
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("SELECT * FROM admins")
        admins.clear()
        for admin_data in await cursor.fetchall():
            admins[admin_data[0]] = admin_data[1]


async def add_admin(user_id, user_role):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("INSERT OR IGNORE INTO admins VALUES (?, ?)", (user_id, user_role))
        await db.commit()
        await load_admins()


async def del_admin(user_id):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("DELETE FROM admins WHERE id = ?", (user_id,))
        await db.commit()
        await load_admins()


async def add_user(user_id: int, user_name: str):
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("INSERT OR IGNORE INTO users VALUES (?, ?, '')", (user_id, user_name))
        await db.commit()
        if cursor.rowcount > 0:
            logger.info(f"Пользователь {user_id} был добавлен в базу данных")


async def delete_user(user_id: int):
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("DELETE FROM users WHERE id = ?", (user_id,))
        await db.commit()
        if cursor.rowcount > 0:
            logger.info(f"Пользователь {user_id} был удален из базы данных")


async def get_user(user_id: int):
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return list(await cursor.fetchone())


async def get_users():
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("SELECT * FROM users")
        return list(await cursor.fetchall())


async def add_photo(file_id, tag):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("INSERT OR IGNORE INTO photos VALUES (?, ?)", (file_id, tag))
        await db.commit()


async def get_photos(tag) -> Photos:
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("SELECT * FROM photos WHERE tag = ?", (tag,))
        return Photos(list(await cursor.fetchall()))


async def get_dish(dish_id) -> list:
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("SELECT * FROM dishes WHERE dish_id = ?", (dish_id,))
        return list(await cursor.fetchone())


async def get_dishes(category, num=None) -> list:
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("SELECT * FROM dishes WHERE category = ?", (category,))
        if type(num) is int:
            return list(await cursor.fetchall())[num]
        else:
            return list(await cursor.fetchall())


async def add_dish(dish_name, dish_description, dish_photo, category, dish_prise, dish_time):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("INSERT OR IGNORE INTO dishes VALUES (NULL, ?, ?, ?, ?, ?, ?)", (dish_name, dish_description, dish_photo, category, dish_prise, dish_time))
        await db.commit()


async def get_user_cart(user_id) -> dict[int]:
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return decode_user_cart(str((await cursor.fetchone())[2]))


def encode_user_cart(cart: dict) -> str:
    result = ""
    for card_id in cart:
        result += str(card_id) + "_"
        result += str(cart[card_id]) + "_"
    return result


def decode_user_cart(cart: str) -> dict:
    result = {}
    card_id = ""
    card_ammount = ""
    flag_cart = True
    for char in cart:
        if char != "_":
            if flag_cart:
                card_id += char
            else:
                card_ammount += char
        else:
            if not flag_cart:
                result[int(card_id)] = int(card_ammount)
                card_id = ""
                card_ammount = ""

            flag_cart = not flag_cart

    return result


async def del_from_cart(user_id, card_id: int, ammount: int) -> int:
    user_cart = await get_user_cart(user_id)
    user_cart[card_id] = max(user_cart.get(card_id, 0) - ammount, 0)
    res = user_cart[card_id]
    user_cart = encode_user_cart(user_cart)
    async with aiosqlite.connect(db_path) as db:
        await db.execute("UPDATE users SET cart = ? WHERE id = ?", (user_cart, user_id))
        await db.commit()
    return res


async def add_to_cart(user_id, card_id: int, ammount: int) -> int:
    user_cart = await get_user_cart(user_id)
    user_cart[card_id] = user_cart.get(card_id, 0) + ammount
    res = user_cart[card_id]
    user_cart = encode_user_cart(user_cart)
    async with aiosqlite.connect(db_path) as db:
        await db.execute("UPDATE users SET cart = ? WHERE id = ?", (user_cart, user_id))
        await db.commit()
    return res

