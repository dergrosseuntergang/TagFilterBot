from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from functions import putter, sender, deleter, confirm_kb, del_all_kb, checker
from models import *
from config import CHANNEL_NAME
from filters import ChatNameFilter
from middlewares import CounterMiddleware
router = Router()
cp_router = Router()
router.message.middleware(CounterMiddleware())


@cp_router.channel_post(ChatNameFilter(CHANNEL_NAME))
async def channel_post_handler(channel_post: types.Message, bot) -> None:
    tags = [x.extract_from(channel_post.text) for x in channel_post.entities if x.type == 'hashtag']
    if tags is None:
        return
    await sender(tags, channel_post, bot)


@router.message(CommandStart(), flags={"once": True})
@router.message(Command('add'))
async def command_start_handler(message: Message, state: FSMContext) -> None:

    await state.set_state(Tags.user_id)
    await state.update_data(user_id=message.chat.id)
    await state.set_state(Tags.hashtag)
    await message.answer(
        "Добавь хэштеги, которые хочешь отслеживать",
        reply_markup=ReplyKeyboardRemove())


@router.message(Command('delete'))
async def delete_single_tag(message: Message, state: FSMContext) -> None:
    await state.set_state(TagToDelete.user_id)
    await state.update_data(user_id=message.chat.id)
    await state.set_state(TagToDelete.hashtag)
    await message.answer(
        "Укажи хэштег, который хочешь перестать отслеживать",
        reply_markup=del_all_kb())


@router.message(F.text == 'Отмена', TagToDelete.confirm)
@router.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return await message.answer('Сейчас нет действий для отмены')
    await state.clear()
    await message.answer(
        "Отменено",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Tags.hashtag, F.text.regexp(r'#\w+'))
async def process_tag(message: Message, state: FSMContext) -> None:
    await state.update_data(hashtag=message.text)
    await message.answer(
        "Готово!",
        reply_markup=ReplyKeyboardRemove())
    data = await state.get_data()
    await putter(data)
    await state.clear()


@router.message(TagToDelete.hashtag, F.text.regexp(r'#\w+'))
async def confirmation(message: Message, state: FSMContext) -> None:
    await state.update_data(hashtag=message.text)
    await state.set_state(TagToDelete.confirm)
    await message.answer(
        "Вы уверены, что хотите прекратить отслеживать этот тэг?",
        reply_markup=confirm_kb())


@router.callback_query(TagToDelete.hashtag, F.data == "delete_all")
async def full_delete_confirm(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(hashtag=None)
    await state.set_state(TagToDelete.confirm)
    await callback.message.answer(
        "Вы уверены, что хотите удалить все данные?\nЭто необратимое действие.",
        reply_markup=confirm_kb())
    await callback.answer()


@router.message(TagToDelete.confirm, F.text == "Да")
async def delete_tag(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await deleter(data)
    await state.clear()
    await message.reply("Готово!", reply_markup=ReplyKeyboardRemove())


@router.message(Tags.hashtag or TagToDelete.hashtag)
async def process_fail(message: Message) -> None:
    await message.answer("Incorrect tag. Please, try again")


@router.message(Command('help'))
async def help_handler(message: types.Message) -> None:
    x = await checker(message.from_user.id)
    print(x)
    text = open('commands.txt', 'r').read()
    await message.answer(text=text)


@router.message(F.text)
async def echo_handler(message: types.Message) -> None:
    try:
        await message.answer("Пожалуйста, воспользуйтесь доступными командами")
    except TypeError:
        await message.answer("Nice try!")
