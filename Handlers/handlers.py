import django
from asgiref.sync import sync_to_async
django.setup()

from aiogram import types, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from FlowerShop.models import Bouquet, Order
from States.states import OrderFlower, GetConsultation
from Keyboards.keyboards import create_reply_keyboard, create_inline_keyboard, back_button, collection_kb
from Common.tools import get_price_range, get_occasion_bouquets, show_full_list_of_bouquets_in_price_range, \
    show_bouquet_in_price_range, get_order_price_by_title

user_private_router = Router()


@user_private_router.message(CommandStart())
@user_private_router.message(StateFilter(None))
async def start_cmd(message: types.Message,  state: FSMContext):
    all_occassions = await get_occasion_bouquets()
    await message.answer(f'Приветствую {message.from_user.first_name}!\n'
                         f'К какому событию готовимся? Выберите один из вариантов, либо укажите свой',
                         reply_markup=create_reply_keyboard(all_occassions))
    await state.set_state(OrderFlower.event)


@user_private_router.message(Command('feedback'))
@user_private_router.message(F.text.contains('Обратная связь'))
async def cmd_feedback(message: types.Message):
    await message.answer(
        'Для отзывов по работе сервиса и получению информации о времени доставки можно обратиться:\n'
             '<b>Телефон</b> : +7123456789\n'
             '<b>TG</b> : @abvgd\n' 
             '<b>Email</b> : support@gmail.com',
        parse_mode=ParseMode.HTML)


@user_private_router.message(OrderFlower.event, F.text)
async def get_estimated_cost(message: types.Message, state: FSMContext):
    valid_occasions = await get_occasion_bouquets()

    if message.text not in valid_occasions:
        await message.answer("Пожалуйста, выберите вариант из предложенных:",
                             reply_markup=create_reply_keyboard(valid_occasions))
        return

    await state.update_data(event=message.text)
    price_ranges = await get_price_range()
    await message.answer('На какую сумму рассчитываете?',
                         reply_markup=create_reply_keyboard(price_ranges))
    await state.set_state(OrderFlower.estimated_cost)


@user_private_router.message(OrderFlower.estimated_cost, F.text.contains('свыше 2000'))
async def get_above_2000(message: types.Message, state: FSMContext):
    await state.update_data(estimated_cost=message.text)
    data = await state.get_data()
    event = data.get('event')
    await show_bouquet_in_price_range(message,'свыше 2000', event)
    await message.answer(f"Выберите букет. Если хотите что-то еще более уникальное,\n"
                         f"подберите другой букет из нашей коллекции или закажите консультацию флориста.",
                         reply_markup=back_button)
    await state.set_state(OrderFlower.bouquet)


@user_private_router.message(OrderFlower.estimated_cost, F.text.contains('до 500'))
async def get_under_500(message: types.Message, state: FSMContext):
    await state.update_data(estimated_cost=message.text)
    data = await state.get_data()
    event = data.get('event')
    await show_bouquet_in_price_range(message,'до 500', event)
    await message.answer("Выберите букет. Если хотите что-то еще более уникальное,\n"
                         f"подберите другой букет из нашей коллекции или закажите консультацию флориста.",
                         reply_markup=back_button)
    await state.set_state(OrderFlower.bouquet)


@user_private_router.message(OrderFlower.estimated_cost, F.text.contains('до 1000'))
async def get_under_1000(message: types.Message, state: FSMContext):
    await state.update_data(estimated_cost=message.text)
    data = await state.get_data()
    event = data.get('event')
    await show_bouquet_in_price_range(message,'до 1000', event)
    await message.answer("Выберите букет. Если хотите что-то еще более уникальное,\n"
                         f"подберите другой букет из нашей коллекции или закажите консультацию флориста.",
                         reply_markup=back_button)
    await state.set_state(OrderFlower.bouquet)


@user_private_router.message(OrderFlower.estimated_cost, F.text.contains('до 2000'))
async def get_under_2000(message: types.Message, state: FSMContext):
    await state.update_data(estimated_cost=message.text)
    data = await state.get_data()
    event = data.get('event')
    await show_bouquet_in_price_range(message,'до 2000', event)
    await message.answer("Выберите букет. Если хотите что-то еще более уникальное,\n"
                         f"подберите другой букет из нашей коллекции или закажите консультацию флориста.",
                         reply_markup=back_button)
    await state.set_state(OrderFlower.bouquet)


@user_private_router.message(F.text == 'Назад к выбору цены')
async def go_back(message: types.Message, state: FSMContext):
    price_ranges = await get_price_range()
    await message.answer("Вы вернулись назад. Выберите примерную стоимость букета.",
                         reply_markup=create_reply_keyboard(price_ranges))
    await state.set_state(OrderFlower.estimated_cost)


@user_private_router.message(F.text == 'Назад к выбору повода')
async def go_back(message: types.Message, state: FSMContext):
    all_occassions = await get_occasion_bouquets()
    await message.answer("Вы вернулись назад. Выберите повод для букета.",
                         reply_markup=create_reply_keyboard(all_occassions))
    await state.set_state(OrderFlower.event)


@user_private_router.message(F.text.contains('Заказать консультацию'))
async def choose_consultation(message: types.Message, state: FSMContext):
    await message.answer("Вы выбрали консультацию флориста.\n"
                         "В течении 20 минут вам перезвонит первый свободный флорист.\n"
                         "Введите ваш номер телефона",
                         reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    await state.set_state(GetConsultation.phone_number)


@user_private_router.message(GetConsultation.phone_number, F.text)
async def select_consultation(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    number_phone = await state.get_data()
    await message.answer(f"Ваш номер: {number_phone['phone_number']}\n"
                         f"Флорист скоро свяжется с вами.\n"
                         f"А пока можете присмотреть что-нибудь из готовой коллекции",
                         reply_markup=collection_kb)
    await state.set_state(OrderFlower.bouquet)


@user_private_router.message(OrderFlower.bouquet, F.text.contains('Посмотреть всю коллекцию'))
async def get_choose_bouquet(message: types.Message, state: FSMContext):
    data = await state.get_data()
    event = data.get('event')
    estimated_cost = data.get('estimated_cost')
    await show_full_list_of_bouquets_in_price_range(message, estimated_cost, event)
    await state.set_state(OrderFlower.bouquet)


@user_private_router.callback_query(F.data.startswith('Выбран '))
async def select_bouquet(callback: types.CallbackQuery, state: FSMContext):
    bouquet_id = callback.data.split('_')
    await state.update_data(bouquet=bouquet_id)
    await callback.message.answer(f'Вы выбрали букет, введите своё имя',
                                  reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    await callback.answer()
    await state.set_state(OrderFlower.name)


@user_private_router.message(OrderFlower.name, F.text)
async def get_user_info_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите адрес доставки.')
    await state.set_state(OrderFlower.address)


@user_private_router.message(OrderFlower.address, F.text)
async def get_user_info_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer('Введите номер телефона')
    await state.set_state(OrderFlower.phone_number)


@user_private_router.message(OrderFlower.phone_number, F.text)
async def get_user_info_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await message.answer('Введите дату доставки в формате ДД.ММ.ГГ ЧЧ:ММ:')
    await state.set_state(OrderFlower.delivery)


@user_private_router.message(OrderFlower.delivery, F.text)
async def get_user_info_delivery(message: types.Message, state: FSMContext):
    await state.update_data(delivery=message.text)
    data = await state.get_data()
    bouquet_title = (data['bouquet'][0])[7:]
    order_price = await get_order_price_by_title(bouquet_title)
    title_of_bouquet = await sync_to_async(Bouquet.objects.get)(name=bouquet_title)
    order = Order(customer=data['name'], order_price = order_price, delivery_address = data['address'],
                  customer_chat_id = message.from_user.id, flower_name = title_of_bouquet, delivery_date = data['delivery'])
    await sync_to_async(order.save)()
    await message.answer(f'Заказ принят🤙')
    await state.clear()
