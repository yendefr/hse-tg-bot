from aiogram.types import Message, ContentTypes, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text, state
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default import menu, role_menu
from handlers.users.menu import *
from states.state import Auth

from loader import dp


@dp.message_handler(CommandStart(), state=None)
async def req_role(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}! Данный чат-бот позволяет получать расписание занятий и фиксировать отсутствующих студентов.")
    await message.answer(f"Вы студент или преподаватель?", reply_markup=role_menu)

    await Auth.first()

@dp.message_handler(Command('info'))
async def get_info(message: Message, state: FSMContext):
    data = await state.get_data()
    role = data.get('role')
    name = data.get('name')
    email = data.get('email')


@dp.message_handler(state=Auth.role)
async def get_role(message: Message, state: FSMContext):
    role = message.text
    await state.update_data(role=role)
    await message.answer('Введите ваши Фамилию и Имя', reply_markup=ReplyKeyboardRemove())

    await Auth.next()

@dp.message_handler(state=Auth.name)
async def get_name(message: Message, state: FSMContext):
    data = await state.get_data()
    role = data.get("role")
    name = message.text
    await state.update_data(name=name)
    
    if (role == 'Студент' and name == 'Иван Иванов'):
        await message.answer('Введите вашу почту, вам будет выслан код для авторизации')
        await Auth.next()
    else:
        await message.answer('Данные не корректны, повторите попытку')

@dp.message_handler(state=Auth.email)
async def get_email(message: Message, state: FSMContext):
    email = message.text
    await state.update_data(email=email)
    await message.answer('Введите код, пришедший вам на почту (не забудте про папку Спам)')
    
    await Auth.next()

@dp.message_handler(state=Auth.password)
async def get_password(message: Message, state: FSMContext):
    password = message.text
    if (password == 'pass'):
        await message.answer('Вы авторизованны!', reply_markup=menu)
        await state.finish()
    else:
        await message.answer('Код не подошёл, проверьте правильность введённых данных\nЛибо обратитесь к админу @yendefr')

@dp.message_handler(state="*", content_types=ContentTypes.ANY)
async def incorrect_message(message: Message):
    await message.answer('Данные некорректны, повторите попытку')