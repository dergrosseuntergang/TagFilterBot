from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message


class ChatNameFilter(BaseFilter):  # [1]
    def __init__(self, chanel_name: Union[str, list]): # [2]
        self.chanel_name = chanel_name

    async def __call__(self, message: Message) -> bool:  # [3]
        return message.chat.type == 'channel' and message.chat.title == self.chanel_name
