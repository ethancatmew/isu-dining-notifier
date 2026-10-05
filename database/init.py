import aiosqlite
import config

async def init_db():
    async with aiosqlite.connect(config.database) as db:
        await db.execute("PRAGMA foreign_keys = ON")

        await db.executescript("""
            CREATE TABLE IF NOT EXISTS user (
                user_id INTEGER,
                notification_at INTEGER,
                
                PRIMARY KEY (user_id)
            );

            CREATE TABLE IF NOT EXISTS food (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS user_foods (
                user_id INTEGER,
                food_id INTEGER,

                PRIMARY KEY (user_id, food_id),
                FOREIGN KEY (user_id) REFERENCES user(user_id),
                FOREIGN KEY (food_id) REFERENCES food(id)
            );

            CREATE TABLE IF NOT EXISTS dining_hall (
                id INTEGER,
                name TEXT NOT NULL,

                PRIMARY KEY (id)
            );

            CREATE TABLE IF NOT EXISTS menu (
                dining_hall_id INTEGER,
                food_id INTEGER,
                menu_date TEXT,

                PRIMARY KEY (dining_hall_id, food_id, menu_date),
                FOREIGN KEY (dining_hall_id) REFERENCES dining_hall(id),
                FOREIGN KEY (food_id) REFERENCES food(id)
            );

            CREATE TABLE IF NOT EXISTS user_dining_halls (
                user_id INTEGER,
                dining_hall_id INTEGER,

                PRIMARY KEY (user_id, dining_hall_id),
                FOREIGN KEY (user_id) REFERENCES user(user_id),
                FOREIGN KEY (dining_hall_id) REFERENCES dining_hall(id)
            );
        """)

        await db.executemany("INSERT OR IGNORE INTO dining_hall (id, name) VALUES (?, ?)", [
            (1, "Conversations"),
            (11, "Memorial Union Food Court"),
            (23, "Seasons Marketplace"),
            (30, "Friley Windows"),
            (38, "Clyde's"),
            (39, "Union Drive Marketplace"),
        ])

        await db.commit()