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
    await message.answer(
        f"Привет, {message.from_user.full_name}\! Данный чат\-бот позволяет получать расписание занятий и фиксировать отсутствующих студентов\.")
    await message.answer(f"Вы студент или преподаватель?", reply_markup=role_menu)

    await Auth.first()


@dp.message_handler(state=Auth.role)
async def get_role(message: Message, state: FSMContext):
    role = message.text

    await state.update_data(role=role)
    await message.answer('Введите вашу почту, зарегистрированную в базе\. Вам будет выслан код для авторизации\.',
                         reply_markup=ReplyKeyboardRemove())

    await Auth.next()


@dp.message_handler(state=Auth.email)
async def get_email(message: Message, state: FSMContext):
    email = message.text
    await state.update_data(email=email)

    data = await state.get_data()

    if await db.check_student(email) != 0 and data.get('role') == 'Студент':
        password = await db.get_student_password(email)

        sender = SendMail(email)
        await sender.sendmail(password)

        await message.answer('Введите код, пришедший вам на почту \(не забудте про папку Спам\)')
        await Auth.next()
    elif await db.check_teacher(email) != 0 and data.get('role') == 'Преподаватель':
        password = await db.get_teacher_password(email)

        sender = SendMail(email)
        await sender.sendmail(password)

        await message.answer('Введите код, пришедший вам на почту \(не забудте про папку Спам\)')
        await Auth.next()
    else:
        await message.answer('Данные некорректны, повторите попытку')


@dp.message_handler(state=Auth.password)
async def get_password(message: Message, state: FSMContext):
    user = User.get_current()
    password = message.text

    data = await state.get_data()
    email = data.get("email")

    if await db.check_password_s(email) == password:
        await db.update_student_id(user.id, email)

        await message.answer('Вы авторизованны\!', reply_markup=menu)
        await state.finish()
    elif await db.check_password_t(email) == password:
        await db.update_schedule_id(user.id, await db.get_teacher_id_by_email(email))
        await db.update_teacher_id(user.id, email)

        await message.answer('Вы авторизованны\!', reply_markup=teacher_menu)
        await state.finish()
    else:
        await message.answer(
            'Код не подошёл, проверьте правильность введённых данных\nЛибо обратитесь к админу @yendefr')


@dp.message_handler(state="*", content_types=ContentType.ANY)
async def incorrect_message(message: Message):
    await message.answer('Данные некорректны, повторите попытку')
