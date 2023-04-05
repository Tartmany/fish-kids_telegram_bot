import asyncpg


from config_data.config import DataBaseConfig, load_config_db


class DataBaseClass:
    async def execute(self, command: str, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False,
                      executemany: bool = False):
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
            elif executemany:
                result = await connection.executemany(command, *args)

        return result
