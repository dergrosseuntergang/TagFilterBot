from typing import Any
from models import *
from aiogram import types
from aiogram.methods import ForwardMessage


async def putter(data: dict[str, Any]) -> None:
    check = await Users.filter(user=data['user_id']).first()
    if check is None:
        check = await Users.create(user=data['user_id'])

    user_id = check.id
    check = await Hashtags.filter(user=check.id, hashtag=data['hashtag']).first()
    if check is None:
        await Hashtags.create(hashtag=data['hashtag'], user_id=user_id)


async def sender(tags: list[str], post: types.Message, bot):
    user_list = set()
    for i in tags:
        users = await Users.filter(user_hashtags__hashtag=i).values_list('user', flat=True)
        user_list = set(users) | user_list

    for j in user_list:
        await ForwardMessage(chat_id=j, from_chat_id=post.chat.id, message_id=post.message_id).as_(bot=bot)
