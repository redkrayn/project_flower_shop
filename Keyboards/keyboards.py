from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def create_reply_keyboard(options: list):
    builder = ReplyKeyboardBuilder()
    for var in options:
        builder.add(KeyboardButton(text=f"{var}"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def create_inline_keyboard(options):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Заказать', callback_data=f'Выбран {options}')],
        ])
