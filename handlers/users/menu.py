from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.default import menu, status_menu
from loader import dp

@dp.message_handler(Command('menu'))
async def show_menu(message: Message):
    await message.answer('Выберите действие в меню', reply_markup=menu)

@dp.message_handler(Text(equals='Указать статус'))
async def set_status(message: Message):
    await message.answer('Выберите ваш статус', reply_markup=status_menu)

@dp.message_handler(Text(equals='Болен'))
async def set_status(message: Message):
    await message.answer('Ваш статус: Болен\nПреподаватель будет оповещён', reply_markup=menu)

@dp.message_handler(Text(equals='Здоров'))
async def set_status(message: Message):
    await message.answer('Ваш статус: Здоров', reply_markup=menu)

@dp.message_handler(Text(equals='Получить расписание'))
async def set_status(message: Message):
    await message.answer('Позже вы получите своё расписание', reply_markup=menu)