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


async def sender(tags: list[str], post: types.Message, bot) -> None:
    user_list = set()
    for i in tags:
        users = await Users.filter(user_hashtags__hashtag=i).values_list('user', flat=True)
        user_list = set(users) | user_list

    for j in user_list:
        await ForwardMessage(chat_id=j, from_chat_id=post.chat.id, message_id=post.message_id).as_(bot=bot)


async def deleter(data:  dict[str, Any]) -> None:
    if data['hashtag'] is None:
        object_to_delete = await Users.get_or_none(user=data['user_id'])
    else:
        object_to_delete = await Hashtags.filter(hashtag=data['hashtag'], user__user=data['user_id']).first()

    if object_to_delete:
        await object_to_delete.delete()
    else:
        print("Object not found")


async def checker(user: int):
    inserted = await Users.filter(user=user)
    return inserted is not None


def confirm_kb():
    kb = [
        [
            types.KeyboardButton(text="Да"),
            types.KeyboardButton(text="Отмена")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    return keyboard


def del_all_kb():
    buttons = [[types.InlineKeyboardButton(text="Удалить всё", callback_data="delete_all")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
