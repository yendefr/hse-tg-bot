from datetime import datetime, timedelta
import random
import string
import typing

from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message, User, CallbackQuery
from aiogram import types
from aiogram.types.message import ContentType

from keyboards.default import menu, status_menu, teacher_menu
from keyboards.inline import get_inline_buttons, data
from states.state import ChangeStatus, ApproveStatus
from loader import bot, dp
from utils.db.db import DB
from data.config import ADMINS

db = DB()


def get_password(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@dp.message_handler(Command('menu'))
async def show_menu(message: Message):
    user = User.get_current()

    if await db.check_teacher_by_id(user.id) != 0:
        current_menu = teacher_menu
    else:
        current_menu = menu

    await message.answer('Выберите действие в меню', reply_markup=current_menu)


# FIX: После проверки админом перестает работать
@dp.message_handler(Text(equals='Указать статус'))
async def set_status(message: Message):
    await message.answer('Выберите ваш статус', reply_markup=status_menu)

    await ChangeStatus.first()


@dp.message_handler(state=ChangeStatus.status)
async def set_status(message: Message, state: FSMContext):
    status = message.text
    await state.update_data(status=status)

    await message.answer('Загрузите фото справки, оно будет направленно на проверку')

    await ChangeStatus.next()


@dp.message_handler(content_types=ContentType.PHOTO, state=ChangeStatus.photo)
async def set_status(message: Message, state: FSMContext):
    state_data = await state.get_data()

    student_id = User.get_current().id
    status = state_data.get('status')

    photo_id = message.photo[0].file_id
    await state.update_data(photo_id=photo_id)

    name = await db.get_student_name_by_id(student_id)

    status_request = get_inline_buttons(student_id, status)

    for admin_id in ADMINS:
        await bot.send_photo(admin_id, photo_id,
                             caption=f'{name} запрашивает статус \"{status}\"',
                             reply_markup=status_request)

    await message.answer('Заявка отправленна на рассмотрение', reply_markup=menu)


@dp.message_handler(Text(equals='Получить расписание'))
async def set_status(message: Message):
    user = User.get_current()

    for row in await db.get_schedule(user.id):
        classroom = row[1].replace('-', '\\-').replace('(', '\\(').replace(')', '\\)')
        time = row[2].replace('.', ' ').replace(':', '\\:').replace('-', '\\-')
        subject = row[3].replace('(', '\\(').replace(')', '\\)')
        group_id = row[4]
        sicked = ''
        for student in await db.get_sicked(group_id):
            sicked += student[0]
        await message.answer(f'{time} {classroom} {subject}\nНе сможет присутствовать\: {sicked}')


@dp.callback_query_handler(data.filter(), lambda callback_query: True)
async def choice_status(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await ApproveStatus.first()

    student_id = callback_data['id']
    status = callback_data['status']
    action = callback_data['action']

    await state.update_data(student_id=student_id)
    await state.update_data(status=status)

    if action == 'accept':
        await callback_query.message.edit_reply_markup(None)
        await callback_query.answer('Введите срок действия статуса в днях')
        await ApproveStatus.next()
    else:
        await callback_query.message.edit_reply_markup(None)
        await bot.send_message(student_id, 'Заявка отклонена')

        await state.finish()


@dp.message_handler(state=ApproveStatus.expires)
async def set_status(message: Message, state: FSMContext):
    expire = float(message.text)

    state_data = await state.get_data()

    student_id = int(state_data.get('student_id'))
    status = state_data.get('status')

    expire_date = datetime.today() + timedelta(days=expire)

    if status == 'Болен':
        await db.update_is_sick(student_id, True, expire_date)
        await bot.send_message(student_id, f'Статус успешно обновлен до ' + expire_date.strftime("%d\.%m"))
    elif status == 'Здоров':
        await db.update_is_sick(student_id, False, expire_date)
        await bot.send_message(student_id, f'Статус успешно обновлен до ' + expire_date.strftime("%d\.%m"))
    else:
        await db.update_is_vaccinated(student_id, True, expire_date)
        await bot.send_message(student_id, f'Статус успешно обновлен до ' + expire_date.strftime("%d\.%m"))

    await state.finish()


# # Для работы с БД
# @dp.message_handler(Command('db'), state=None)
# async def get_command(message: Message):
#     await message.answer('Введите данные')
#     await Insert.first()
#
#
# @dp.message_handler(state=Insert.input)
# async def get_data(message: Message, state: FSMContext):
#     data = message.text.split('/')
#     name, classroom, time, subject = data[0], data[1], data[2], data[3]
#     group_id = 'БИВ181'
#     name = await db.get_teacher_id_by_name(name)
#     print(id, name, classroom, time, subject, group_id)
#     await db.insert('schedule', (id, classroom, time, subject, group_id))

# url = 'https://www.hse.ru/org/persons/?ltr=%D0%92%D1%81%D0%B5;udept=59315150'
# page = requests.get(url)
# soup = BeautifulSoup(page.text, 'html.parser')
# teachers = soup.find_all('div', class_='person')
# for teacher in teachers:
#     main = teacher.find('div', class_='main')
#     extra = teacher.find('div', class_='l-extra')
#     name = main.find('a', class_='link').text.split(' ')
#     name = name[0] + ' ' + name[1]
#     name = name.strip()
#     try:
#         email = extra.find('a', class_='link').get('data-at')
#         email = email.replace('[', '').replace(']', '').replace('"', '').replace(',', '').replace('-at-', '@')
#     except AttributeError:
#         email = ''
#     password = get_password()
#     await db.insert('teachers', (name, email, password))

# print(teachers[0])

# name = message.text.split(' ')
# name = name[0] + ' ' + name[1]
# email = ''
# group = 'БИВ186'
# password = get_password()
# await db.insert('students', (name, email, password, group))
# await state.finish()
