from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message
from functions import checker


class CounterMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if get_flag(data, "once"):
            if await checker(event.from_user.id):
                return await event.answer('Вы уже запустили бота!')
            else:
                return await handler(event, data)
        else:
            return await handler(event, data)
