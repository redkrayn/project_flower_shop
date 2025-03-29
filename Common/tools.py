from datetime import datetime, timedelta
from aiogram import types
import django
from asgiref.sync import sync_to_async

django.setup()

from FlowerShop.models import Bouquet
from Keyboards.keyboards import create_inline_keyboard


def is_within_24_hours(delivery_date):
    current_time = datetime.now()
    time_difference = delivery_date - current_time
    return time_difference <= timedelta(hours=24) and time_difference >= timedelta(0)


async def show_bouquet_in_price_range(message: types.Message, price_range: str, event: str):
    bouquets = await sync_to_async(list)(Bouquet.objects.all())

    for bouquet in bouquets:
        if price_range == 'до 500' and bouquet.price <= 500 and bouquet.occasion == event:
            await message.answer(
                text=f'Цена: {bouquet.price}\n'
                     f'Описание: {bouquet.description}\n'
                     f'Фотография: {bouquet.image}\n',
                reply_markup=create_inline_keyboard(bouquet.name)
            )
            return True
        elif price_range == 'до 1000' and 500 < bouquet.price <= 1000 and bouquet.occasion == event:
            await message.answer(
                text=f'Цена: {bouquet.price}\n'
                     f'Описание: {bouquet.description}\n'
                     f'Фотография: {bouquet.image}\n',
                reply_markup=create_inline_keyboard(bouquet.name)
            )
            return True
        elif price_range == 'до 2000' and 1000 < bouquet.price <= 2000 and bouquet.occasion == event:
            await message.answer(
                text=f'Цена: {bouquet.price}\n'
                     f'Описание: {bouquet.description}\n'
                     f'Фотография: {bouquet.image}\n',
                reply_markup=create_inline_keyboard(bouquet.name)
            )
            return True
        elif price_range == 'свыше 2000' and bouquet.price > 2000 and bouquet.occasion == event:
            await message.answer(
                text=f'Цена: {bouquet.price}\n'
                     f'Описание: {bouquet.description}\n'
                     f'Фотография: {bouquet.image}\n',
                reply_markup=create_inline_keyboard(bouquet.name)
            )
            return True


async def show_full_list_of_bouquets_in_price_range(message: types.Message, price_range: str, event: str):
    bouquets = await sync_to_async(list)(Bouquet.objects.all())
    for bouquet in bouquets:
        if ((price_range == 'до 500' or 'до 1000' or 'до 2000') and bouquet.price <= 2000 and bouquet.occasion == event) or \
            (price_range == 'свыше 2000' and bouquet.price > 2000 and bouquet.occasion == event):
            await message.answer(
                text=f'Цена: {bouquet.price}\n'
                     f'Описание: {bouquet.description}\n'
                     f'Фотография: {bouquet.image}\n',
                reply_markup=create_inline_keyboard(bouquet.name)
            )
    return True


async def get_price_range():
    bouquets = await sync_to_async(list) (Bouquet.objects.all())
    flower_bouquets = []
    for bouquet in bouquets:
        if bouquet.price <= 500:
            price_range = 'до 500'
        elif bouquet.price <= 1000:
            price_range = 'до 1000'
        elif bouquet.price <= 2000:
            price_range = 'до 2000'
        elif bouquet.price > 2000:
            price_range = 'свыше 2000'
        flower_bouquets.append(price_range)
    return set(flower_bouquets)


async def get_occasion_bouquets():
    return await sync_to_async(list)(Bouquet.objects.values_list('occasion', flat=True).distinct())


async def get_order_price_by_title(title_bouquet):
    bouquets = await sync_to_async(list)(Bouquet.objects.all())
    for bouquet in bouquets:
        if bouquet.name == title_bouquet:
            return bouquet.price
