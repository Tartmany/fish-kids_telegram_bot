from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message
from cachetools import TTLCache


class ThrottlingMiddlewareMessage(BaseMiddleware):

    caches = {
        "lastmsg": TTLCache(maxsize=10_000, ttl=3),
        "lastcb": TTLCache(maxsize=10_000, ttl=2)
            }

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        throttling_key = get_flag(data, "throttling_key")
        if throttling_key is not None and throttling_key in self.caches:
            if event.from_user.id in self.caches[throttling_key]:
                return
            else:
                self.caches[throttling_key][event.from_user.id] = None
        return await handler(event, data)
