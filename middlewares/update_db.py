from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.flags import get_flag

from database.update_db_queries import insert_update


class UpdateDBMiddlewareCB(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        callback_updates = get_flag(data, "save_update")

        # Если такого флага на хэндлере нет
        if not callback_updates:
            return await handler(event, data)

        update = (event.from_user.id, event.message.date,
                  event.data)
        await insert_update(update)
        return await handler(event, data)


class UpdateDBMiddlewareMSG(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        message_updates = get_flag(data, "save_update")

        # Если такого флага на хэндлере нет
        if not message_updates:
            return await handler(event, data)

        update = (event.from_user.id, event.date,
                  event.text)
        await insert_update(update)
        return await handler(event, data)
