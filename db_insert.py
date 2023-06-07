import asyncio
import asyncpg

from config_data.config import DataBaseConfig, load_config_db
from db_work import aquariums, animals, aq_an, aq_an_2, aq_an_3


async def insert_aquariums(aqua, connection) -> int:
    ins_aquariums = "INSERT INTO aquariums VALUES($1, $2, DEFAULT)"
    return await connection.executemany(ins_aquariums, aqua)


async def insert_animals(animal, connection) -> int:
    ins_animals = "INSERT INTO animals (name, description, callback) VALUES($1, $2, $3)"
    return await connection.executemany(ins_animals, animal)


async def insert_aq_an(animal, connection) -> int:
    ins_aq_an = "INSERT INTO aquarium_animals(aq_number, animal_id) VALUES($1, $2)"
    return await connection.executemany(ins_aq_an, animal)


async def main():
    config: DataBaseConfig = load_config_db()
    connection = await asyncpg.connect(host=config.db_conf.host, port=config.db_conf.port,
                                       user=config.db_conf.pg_user, database=config.db_conf.DATABASE,
                                       password=config.db_conf.pg_password)
    await insert_aq_an(aq_an_3, connection)

asyncio.run(main())
