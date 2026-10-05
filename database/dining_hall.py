import config
import aiosqlite

async def add_favorite(user_id: int, dining_hall_id: int):
    async with aiosqlite.connect(config.database) as db:
        await db.execute("INSERT OR IGNORE INTO user_dining_halls (user_id, dining_hall_id) VALUES (?, ?)", (user_id, dining_hall_id))
        await db.commit()

async def remove_favorite(user_id: int, dining_hall_id: int):
    async with aiosqlite.connect(config.database) as db:
        await db.execute("DELETE FROM user_dining_halls WHERE user_id = ? AND dining_hall_id = ?", (user_id, dining_hall_id))
        await db.commit()

async def get_favorites(user_id: int):
    async with aiosqlite.connect(config.database) as db:
        cursor = await db.execute("""
            SELECT dining_hall.id, dining_hall.name FROM user_dining_halls
            JOIN dining_hall ON dining_hall.id = user_dining_halls.dining_hall_id WHERE user_dining_halls.user_id = ?
            ORDER BY dining_hall.name
        """, (user_id,))
        return await cursor.fetchall()

async def get_all():
    async with aiosqlite.connect(config.database) as db:
        cursor = await db.execute("""
            SELECT id, name FROM dining_hall
            ORDER BY name
        """)
        return await cursor.fetchall()