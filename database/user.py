import config
import aiosqlite

async def create_user(user_id: int):
    async with aiosqlite.connect(config.database) as db:
        await db.execute("INSERT OR IGNORE INTO user (user_id, notification_at) VALUES (?, ?)", (user_id, config.default_notification_at))
        await db.commit()

async def set_notification_time(user_id: int, notification_at: int):
    async with aiosqlite.connect(config.database) as db:
        await db.execute("UPDATE user SET notification_at = ? WHERE user_id = ?", (notification_at, user_id))
        await db.commit()

async def get_notification_time(user_id: int):
    async with aiosqlite.connect(config.database) as db:
        cursor = await db.execute("SELECT notification_at FROM user WHERE user_id = ?", (user_id,))
        result = await cursor.fetchone()
        return result[0]