from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


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


back_button = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='Назад')],
                  [KeyboardButton(text='Заказать консультацию')],
                  [KeyboardButton(text='Посмотреть всю коллекцию')]],
        resize_keyboard=True)


collection_kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='Посмотреть всю коллекцию')]],
        resize_keyboard=True)