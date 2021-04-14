from aiogram.types import Message
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from states.state import Insert
from utils.db.db import DB
import string, random

from loader import dp

def get_password(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

db = DB()

@dp.message_handler(Command('db'), state=None)
async def get_command(message: Message):
    await message.answer('Введите Фамилию Имя')
    Insert.first()

@dp.message_handler(state=Insert.input)
async def get_data(message: Message, state: FSMContext):
    name, group = message.text.split('/')[0], message.text.split('/')[1]
    email = ''
    password = get_password()
    
    db.insert('students', (name, email, password, group))
    state.finish()
