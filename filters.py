from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message


class ChatNameFilter(BaseFilter):
    def __init__(self, chanel_name: Union[str, list]):
        self.chanel_name = chanel_name

    async def __call__(self, message: Message) -> bool:
        return message.chat.type == 'channel' and message.chat.title == self.chanel_name


class StartOrAdd(BaseFilter):

    async def __call__(self, message: Message) -> bool:
        return message.text == '/add' or message.text == '/start'
