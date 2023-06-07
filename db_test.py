from typing import Union
import time
import asyncio
import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from config_data.config import DataBaseConfig, load_config_db


class DataBaseClass:
    async def execute(self, command: str, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False):
        config: DataBaseConfig = load_config_db()
        connection = await asyncpg.connect(host=config.db_conf.host, port=config.db_conf.port,
                                           user=config.db_conf.pg_user, database=config.db_conf.DATABASE,
                                           password=config.db_conf.pg_password)
        async with connection.transaction():
            if fetch:
                result = await connection.fetch(command, *args)
            elif fetchval:
                result = await connection.fetchval(command, *args)
            elif fetchrow:
                result = await connection.fetchrow(command, *args)
            elif execute:
                result = await connection.execute(command, *args)

        return result


DataBase = DataBaseClass()


# Эта функция отправляет запрос в базу данных и формирует
# список номеров всех аквариумов в базе
async def all_aquarium_numbers() -> list:
    result = await DataBase.execute('''SELECT aq_number FROM aquariums''', fetch=True)
    aquariums = []
    for i in result:
        aquariums.append(i[0])
    print(aquariums)
    return aquariums


asyncio.run(all_aquarium_numbers())
