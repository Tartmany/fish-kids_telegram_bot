# Модуль с запросами к базе данных, которые используются в хэндлерах
from database.database_class import DataBaseClass


DataBase = DataBaseClass()


async def insert_update(update: tuple) -> int:
    return await DataBase.execute(f'''INSERT INTO updates(user_id, date, message) \
    VALUES ($1, $2, $3)''', *update, execute=True)


async def load_updates() -> list:
    result = await DataBase.execute('''SELECT * FROM updates''', fetch=True)
    updates = []
    for i in result:
        update = [i[0], i[1], i[2], i[3]]
        updates.append(update)
    return updates


async def delete_updates() -> list:
    return await DataBase.execute('''DELETE FROM updates''', execute=True)
