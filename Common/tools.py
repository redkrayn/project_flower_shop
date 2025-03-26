from datetime import datetime, timedelta
from aiogram import types

from Common.dict_of_bouquets import flower_bouquets
from Keyboards.keyboards import create_inline_keyboard


def is_within_24_hours(delivery_date):
    current_time = datetime.now()
    time_difference = delivery_date - current_time
    return time_difference <= timedelta(hours=24) and time_difference >= timedelta(0)


async def show_bouquets_in_price_range(message: types.Message, price_range: str):
    for bouquet in flower_bouquets.values():
        if bouquet['price_range'] == price_range:
            await message.answer(
                text=f'Цена: {bouquet["price"]}\n'
                     f'Описание: {bouquet["description"]}\n'
                     f'Фотография: {bouquet["image"]}\n',
                reply_markup=create_inline_keyboard(bouquet["id"])
            )

