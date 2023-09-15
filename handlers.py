from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from functions import putter, sender
from models import *
from config import CHANNEL_NAME
from filters import ChatNameFilter

router = Router()
cp_router = Router()


@cp_router.channel_post(ChatNameFilter(CHANNEL_NAME))
async def channel_post_handler(channel_post: types.Message, bot) -> None:
    tags = [x.extract_from(channel_post.text) for x in channel_post.entities if x.type == 'hashtag']
    if tags is None:
        return
    await sender(tags, channel_post, bot)


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Tags.user_id)
    await state.update_data(user_id=message.chat.id)
    await state.set_state(Tags.hashtag)
    await message.answer(
        "Добавь хэштеги, которые хочешь отслеживать",
        reply_markup=ReplyKeyboardRemove())


@router.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Tags.hashtag, F.text.regexp(r'#\w+'))
async def process_tag(message: Message, state: FSMContext) -> None:
    await state.update_data(hashtag=message.text)
    await message.answer(
        "Thanks!",
        reply_markup=ReplyKeyboardRemove())
    data = await state.get_data()
    await putter(data)
    await state.clear()


@router.message(Tags.hashtag)
async def process_fail(message: Message) -> None:
    await message.answer("Incorrect tag. Please, try again")


@router.message(F.text)
async def echo_handler(message: types.Message) -> None:
    """
    Переписать
    """
    try:
        await message.answer(message.text)
    except TypeError:
        await message.answer("Nice try!")

