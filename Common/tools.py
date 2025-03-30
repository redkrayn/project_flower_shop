from random import sample

from aiogram import types
from dotenv import load_dotenv
import os
import django
from asgiref.sync import sync_to_async
from aiogram.types import FSInputFile
import re

from FlowerShop.models import Bouquet
from Keyboards.keyboards import create_inline_keyboard, back_button


django.setup()
load_dotenv()


async def show_bouquet_in_price_range(message: types.Message, price_range: str, event: str):
    bouquets = await sync_to_async(list)(Bouquet.objects.all())

    message_for_user = ("Выберите букет. Если хотите что-то еще более уникальное,\n"
                        "подберите другой букет из нашей коллекции или закажите консультацию флориста.")
    path_to_photo = os.getenv('PATH_TO_GET_IMAGE')

    filtered_bouquets = []
    for bouquet in bouquets:
        if bouquet.occasion == event and (
            (price_range == 'до 500' and bouquet.price <= 500) or
            (price_range == 'до 1000' and 500 < bouquet.price <= 1000) or
            (price_range == 'до 2000' and 1000 < bouquet.price <= 2000) or
            (price_range == 'свыше 2000' and bouquet.price > 2000)):
            filtered_bouquets.append(bouquet)

    bouquets_to_show = filtered_bouquets[:3]

    for bouquet in bouquets_to_show:
        text_for_desc_and_price = (f'Описание: {bouquet.description}\n'
                                   f'Цена: {bouquet.price}\n'
                                   f'Состав: {bouquet.composition}')
        photo = FSInputFile(f'{path_to_photo}{bouquet.image}')

        await message.reply_photo(photo=photo, caption=text_for_desc_and_price,
                                  reply_markup=create_inline_keyboard(bouquet.name))
        return await message.answer(message_for_user,reply_markup=back_button)

    else:
        return await message.answer("К сожалению, в диапазоне нет подходящих букетов для повода", reply_markup=back_button)


async def show_full_list_of_bouquets_in_price_range(message: types.Message, price_range: str, event: str):
    bouquets = await sync_to_async(list)(Bouquet.objects.all())
    for bouquet in bouquets:
        path_to_photo = os.getenv('PATH_TO_GET_IMAGE')
        photo = FSInputFile(f'{path_to_photo}{bouquet.image}')

        if bouquet.occasion == event and (
                ((price_range == 'до 500' and 'до 1000') and bouquet.price <= 1000) or
                (price_range == 'до 2000' and 1000 < bouquet.price <= 2000) or
                (price_range == 'свыше 2000' and bouquet.price > 2000)):

                await message.reply_photo(photo=photo,
                                          caption=(f'Описание: {bouquet.description}\n'
                                                   f'Цена: {bouquet.price}\n'
                                                   f'Состав: {bouquet.composition}'),
                                          reply_markup=create_inline_keyboard(bouquet.name))
    return True



async def price_does_not_matter(message: types.Message):
    bouquets = await sync_to_async(list)(Bouquet.objects.all())
    bouquet = sample(bouquets, min(3, len(bouquets)))
    message_for_user = ("Выберите букет. Если хотите что-то еще более уникальное,\n"
                        "подберите другой букет из нашей коллекции или закажите консультацию флориста.")
    for var in bouquet:
        path_to_photo = os.getenv('PATH_TO_GET_IMAGE')
        photo = FSInputFile(f'{path_to_photo}{var.image}')
        await message.reply_photo(photo=photo,
                                  caption=(f'Описание: {var.description}\n'
                                           f'Цена: {var.price}\n'
                                           f'Состав: {var.composition}'),
                                  reply_markup=create_inline_keyboard(var.name))
    await message.answer(message_for_user, reply_markup=back_button)


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
        flower_bouquets.append('Не важно')
    return set(flower_bouquets)


async def get_occasion_bouquets():
    return await sync_to_async(list)(Bouquet.objects.values_list('occasion', flat=True).distinct())


async def get_order_price_by_title(title_bouquet):
    bouquets = await sync_to_async(list)(Bouquet.objects.all())
    for bouquet in bouquets:
        if bouquet.name == title_bouquet:
            return bouquet.price


def is_valid_russian_phone(phone: str) -> bool:
    pattern = re.compile(
        r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'
    )
    return bool(pattern.match(phone))
