from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router, types, html, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


#код на случай, если нужно отслеживать несколько каналов


router = Router()


class Form(StatesGroup):
    groups = State()
    tag = State()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.groups)
    await message.answer(
        "Добавь группы, которые хочешь отслеживать",
        reply_markup=ReplyKeyboardRemove())


@router.message(Form.groups, F.text.regexp(r'@\w+'))
async def process_groups(message: Message, state: FSMContext) -> None:
    await state.update_data(groups=message.text)
    await state.set_state(Form.tag)
    await message.answer(
        "Well done! Now, add your tags",
        reply_markup=ReplyKeyboardRemove())


@router.message(Form.tag, F.text.regexp(r'#\w+'))
async def process_tag(message: Message, state: FSMContext) -> None:
    await state.update_data(tag=message.text)

    await message.answer(
        "Thank's!",
        reply_markup=ReplyKeyboardRemove())
    await state.set_state(state=None)


@router.message(Form.groups)
async def process_fail(message: Message) -> None:
    await message.answer("Incorrect group. Please, try again")


@router.message(Form.tag)
async def process_fail(message: Message) -> None:
    await message.answer("Incorrect tag. Please, try again")


@router.message(Command("show"))
async def show_summary(message: Message, state: FSMContext, positive: bool = True) -> None:
    data = await state.get_data()
    id = data["groups"]
    tag = data["tag"]
    text = f'{id}, {tag}'
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())