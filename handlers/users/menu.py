from aiogram.dispatcher.storage import FSMContext
from states.state import Insert
from utils.db.db import DB
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, User
from keyboards.default import menu, status_menu, teacher_menu
from loader import dp
import string, random

db = DB()

def get_password(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@dp.message_handler(Command('menu'))
async def show_menu(message: Message):
    user = User.get_current()
    if (await db.check_teacher_by_id(user.id) != 0): current_menu = teacher_menu
    else: current_menu = menu
    
    await message.answer('Выберите действие в меню', reply_markup=current_menu)

@dp.message_handler(Text(equals='Указать статус'))
async def set_status(message: Message):
    user = User.get_current()
    if (await db.check_teacher_by_id(user.id) != 1):
        await message.answer('Выберите ваш статус', reply_markup=status_menu)

@dp.message_handler(Text(equals='Болен'))
async def set_status(message: Message):
    user = User.get_current()

    await db.update_is_sick(user.id, True)
    await message.answer('Ваш статус: Болен\nПреподаватель будет оповещён', reply_markup=menu)

@dp.message_handler(Text(equals='Здоров'))
async def set_status(message: Message):
    user = User.get_current()

    await db.update_is_sick(user.id, False)
    await message.answer('Ваш статус: Здоров', reply_markup=menu)

@dp.message_handler(Text(equals='Получить расписание'))
async def set_status(message: Message):
    user = User.get_current()
    if (await db.check_teacher_by_id(user.id) != 0): current_menu = teacher_menu
    else: current_menu = menu

    for row in await db.get_schedule(user.id):
        classroom = row[1].replace('-', '\\-').replace('(', '\\(').replace(')', '\\)')
        time = row[2].replace('.', ' ').replace(':', '\\:').replace('-', '\\-')
        subject = row[3].replace('(', '\\(').replace(')', '\\)')
        group_id = row[4]
        sicked = ''
        for student in await db.get_sicked(group_id):
            sicked += student[0]
        await message.answer(f'{time} {classroom} {subject}\nНе сможет присутствовать\: {sicked}')


# Для работы с БД
@dp.message_handler(Command('db'), state=None)
async def get_command(message: Message):
    await message.answer('Введите Фамилию Имя, Группу')
    await Insert.first()

@dp.message_handler(state=Insert.input)
async def get_data(message: Message, state: FSMContext):
    # Здесь работать с базой
    await state.finish()
