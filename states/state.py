from aiogram.dispatcher.filters.state import StatesGroup, State

class Auth(StatesGroup):
    role = State()
    name = State()
    email = State()
    password = State()

class Insert(StatesGroup):
    input = State()