from dataclasses import dataclass
import os
from environs import Env


@dataclass
class TgBot:
    token: str            # Токен для доступа к телеграм-боту
    admin_ids: list[int]  # Список id администраторов бота


@dataclass
class DBConf:
    host: str            # хост для доступа к базе данных
    port: str            # порт для доступа к базе данных
    pg_user: str         # имя юзера базы данных
    pg_password: str     # пароль к базе данных
    DATABASE: str        # название базы данных


@dataclass
class Config:
    tg_bot: TgBot


@dataclass
class DataBaseConfig:
    db_conf: DBConf


# Создаем функцию, которая будет читать файл .env и возвращать
# экземпляр класса Config с заполненными полями token и admin_ids
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(
                    token=env('BOT_TOKEN'),
                    admin_ids=list(map(int, env.list('ADMIN_IDS')))))


def load_config_db(path: str | None = None) -> DataBaseConfig:
    env = Env()
    env.read_env(path)
    return DataBaseConfig(db_conf=DBConf(
                    host= env('ip'),
                    port= env('port'),
                    pg_user= env('pg_user'),
                    pg_password= env('pg_password'),
                    DATABASE= env('DATABASE')))


ip = os.getenv('ip')
pg_user = str(os.getenv('pg_user'))
pg_password = str(os.getenv('pg_password'))
DATABASE = str(os.getenv('DATABASE'))
port = str(os.getenv('port'))

POSTGRES_URI = f'postgresql://{pg_user}:{pg_password}@{ip}/{DATABASE}'
