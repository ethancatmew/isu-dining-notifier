import config
import aiosqlite

async def add_food(name: str):
    async with aiosqlite.connect(config.database) as db:
        await db.execute("INSERT OR IGNORE INTO food (name) VALUES (?)", (name,))
        await db.commit()

async def add_foods(foods: list[str]):
    async with aiosqlite.connect(config.database) as db:
        await db.executemany(
            "INSERT OR IGNORE INTO food (name) VALUES (?)",
            [(food,) for food in foods]
        )
        await db.commit()

async def remove_food(name: str):
    async with aiosqlite.connect(config.database) as db:
        await db.execute("DELETE FROM food WHERE name = ?", (name,))
        await db.commit()

async def add_favorite(user_id: int, name: str):
    async with aiosqlite.connect(config.database) as db:
        await db.execute("INSERT OR IGNORE INTO user_foods (user_id, food_name) VALUES (?, ?)", (user_id, name))
        await db.commit()

async def remove_favorite(user_id: int, name: str):
    async with aiosqlite.connect(config.database) as db:
        await db.execute("DELETE FROM user_foods WHERE user_id = ? AND food_name = ?", (user_id, name))
        await db.commit()

async def get_favorites(user_id: int):
    async with aiosqlite.connect(config.database) as db:
        cursor = await db.execute("""
            SELECT food.name FROM user_foods
            JOIN food ON food.name = user_foods.food_name WHERE user_foods.user_id = ?
            ORDER BY food.name
        """, (user_id,))
        return await cursor.fetchall()

async def search_foods(query: str):
    async with aiosqlite.connect(config.database) as db:
        cursor = await db.execute("""
            SELECT name FROM food WHERE name LIKE ?
            ORDER BY name
            LIMIT 25
        """, (f"{query}%",))
        return await cursor.fetchall()