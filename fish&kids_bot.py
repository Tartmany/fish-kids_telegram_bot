import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from config_data.config import Config, load_config
from handlers import (other_handlers, user_handlers, admin_handlers,
                      FSM_handlers)
from keyboards.main_menu import set_main_menu
from middlewares.throttling import ThrottlingMiddlewareMessage
from middlewares.update_db import UpdateDBMiddlewareCB, UpdateDBMiddlewareMSG


# Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
    storage: MemoryStorage = MemoryStorage()

    # Инициализируем бот и диспетчер
    bot: Bot = Bot(token=config.tg_bot.token,
                   parse_mode='HTML')
    dp: Dispatcher = Dispatcher(storage=storage)

    # Настраиваем главное меню бота
    await bot.delete_my_commands()
    await set_main_menu(bot)

    # Регистриуем роутеры в диспетчере
    dp.include_router(admin_handlers.router)
    dp.include_router(FSM_handlers.router)
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # Регистрация мидлвари для троттлинга
    dp.callback_query.middleware(CallbackAnswerMiddleware())
    dp.callback_query.middleware(ThrottlingMiddlewareMessage())
    dp.message.middleware(ThrottlingMiddlewareMessage())
    dp.callback_query.middleware(UpdateDBMiddlewareCB())
    dp.message.middleware(UpdateDBMiddlewareMSG())

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        # Запускаем функцию main
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        # Выводим в консоль сообщение об ошибке,
        # если получены исключения KeyboardInterrupt или SystemExit
        logger.error('Bot stopped!')
