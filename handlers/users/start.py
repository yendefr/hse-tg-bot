from aiogram.types import Message, ReplyKeyboardRemove, User
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types.message import ContentType
from keyboards.default import menu, role_menu, teacher_menu
from handlers.users.menu import *
from states.state import Auth
from utils.db.db import DB
from utils.mail.sendmail import SendMail

from loader import dp

db = DB()

@dp.message_handler(CommandStart(), state=None)
async def req_role(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}\! Данный чат\-бот позволяет получать расписание занятий и фиксировать отсутствующих студентов\.")
    await message.answer(f"Вы студент или преподаватель?", reply_markup=role_menu)

    await Auth.first()

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

    if (await db.check_student(name) != 0 or await db.check_teacher(name) != 0):
        await message.answer('Введите вашу почту, вам будет выслан код для авторизации')
        await Auth.next()
    else: 
        await message.answer('Данные некорректны, повторите попытку')

@dp.message_handler(state=Auth.email)
async def get_email(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data.get("name")
    email = message.text
    await state.update_data(email=email)
    if (await db.check_student(name) != 0): 
        await db.update_student_email(email, name)
        password = await db.get_student_password(name)
    if (await db.check_teacher(name) != 0):
        await db.update_teacher_email(email, name)
        password = await db.get_teacher_password(name)
    
    print('!!!', password, '!!!')

    sender = SendMail(email)
    await sender.sendmail(password)

    await message.answer('Введите код, пришедший вам на почту \(не забудте про папку Спам\)')
    
    await Auth.next()

@dp.message_handler(state=Auth.password)
async def get_password(message: Message, state: FSMContext):
    user = User.get_current()
    data = await state.get_data()
    name = data.get("name")
    password = message.text
    if (await db.check_password_s(name) == password):
        await db.update_student_id(user.id, name)
        await message.answer('Вы авторизованны\!', reply_markup=menu)
        await state.finish()
    elif (await db.check_password_t(name) == password):
        await db.update_schedule_id(user.id, await db.get_teacher_id_by_name(name))
        await db.update_teacher_id(user.id, name)
        await message.answer('Вы авторизованны\!', reply_markup=teacher_menu)
        await state.finish()
    else:
        await message.answer('Код не подошёл, проверьте правильность введённых данных\nЛибо обратитесь к админу @yendefr')

@dp.message_handler(state="*", content_types=ContentType.ANY)
async def incorrect_message(message: Message):
    await message.answer('Данные некорректны, повторите попытку')