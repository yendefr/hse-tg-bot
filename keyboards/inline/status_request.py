from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

data = CallbackData('status', 'id', 'status', 'action')


def get_inline_buttons(student_id, status):
    status_request = InlineKeyboardMarkup()
    status_request.add(
        InlineKeyboardButton('Одобрить', callback_data=data.new(id=student_id, status=status, action='accept')),
    )
    status_request.add(
        InlineKeyboardButton('Отклонить', callback_data=data.new(id=student_id, status=status, action='decline')),
    )
    # status_request = InlineKeyboardMarkup(
    #     row_width=1,
    #     inline_keyboard=[
    #         [
    #             InlineKeyboardButton('Одобрить', callback_data=data.new(id=student_id, action='accept')),
    #             InlineKeyboardButton('Отклонить', callback_data=data.new(id=student_id, action='decline')),
    #         ]
    #     ]
    # )

    return status_request
