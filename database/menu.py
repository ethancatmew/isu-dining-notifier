import config
import aiosqlite

async def add_menu_items(items):
    async with aiosqlite.connect(config.database) as db:
        await db.executemany("INSERT OR IGNORE INTO menu (dining_hall_id, food_name, menu_date) VALUES (?, ?, ?)", items)
        await db.commit()

async def clear_menu(menu_date: str):
    async with aiosqlite.connect(config.database) as db:
        await db.execute("DELETE FROM menu WHERE menu_date = ?", (menu_date,))
        await db.commit()

async def get_favorites_for_date(user_id: int, menu_date: str):
    async with aiosqlite.connect(config.database) as db:
        cursor = await db.execute("""
            SELECT food.name, dining_hall.id, dining_hall.name FROM menu
            JOIN food ON food.name = menu.food_name
            JOIN user_foods ON user_foods.food_name = menu.food_name
            JOIN user_dining_halls ON user_dining_halls.dining_hall_id = menu.dining_hall_id
            JOIN dining_hall ON dining_hall.id = menu.dining_hall_id
            WHERE user_foods.user_id = ?
            AND user_dining_halls.user_id = ?
            AND menu.menu_date = ?
            ORDER BY dining_hall.name, food.name
        """, (user_id, user_id, menu_date))
        return await cursor.fetchall()