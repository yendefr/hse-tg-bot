from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

role_menu = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text='Преподаватель'),
            KeyboardButton(text='Студент'),
        ],
    ],
    resize_keyboard=True,
)

menu = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text='Указать статус'),
        ],
    ],
    resize_keyboard=True,
)
teacher_menu = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text='Получить расписание'),
        ],
    ],
    resize_keyboard=True,
)
status_menu = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text='Болен'),
            KeyboardButton(text='Здоров'),
        ]
    ],
    resize_keyboard=True,
)
