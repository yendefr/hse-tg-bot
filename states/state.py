from aiogram.dispatcher.filters.state import StatesGroup, State


class Auth(StatesGroup):
    role = State()
    email = State()
    password = State()


class Insert(StatesGroup):
    input = State()


class ChangeStatus(StatesGroup):
    status = State()
    photo = State()


class ApproveStatus(StatesGroup):
    choice = State()
    expires = State()
