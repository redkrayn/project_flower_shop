from aiogram import types, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from Keyboards.keyboards import create_reply_keyboard, create_inline_keyboard

from Common.dict_of_bouquets import flower_bouquets, get_occasion, get_price_range


class GetConsultation(StatesGroup):
    phone_number = State()


class OrderFlower(StatesGroup):
    event = State()
    estimated_cost = State()
    name = State()
    bouquet  = State()
    address = State()
    delivery = State()
    phone_number = State()


user_private_router = Router()


@user_private_router.message(CommandStart())
@user_private_router.message(StateFilter(None))
async def start_cmd(message: types.Message,  state: FSMContext):
    await message.answer(f'Приветствую {message.from_user.first_name}!\n'
                         f'К какому событию готовимся? Выберите один из вариантов, либо укажите свой',
                         reply_markup=create_reply_keyboard(get_occasion(flower_bouquets)))
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


@user_private_router.message(OrderFlower.event, F.text.in_(get_occasion(flower_bouquets)))
async def get_estimated_cost(message: types.Message, state: FSMContext):
    await state.update_data(event=message.text)
    await message.answer('На какую сумму рассчитываете?',
                         reply_markup=create_reply_keyboard(get_price_range(flower_bouquets)))
    await state.set_state(OrderFlower.estimated_cost)


@user_private_router.message(OrderFlower.estimated_cost, F.text.contains('свыше 2000'))
async def get_above_2000(message: types.Message, state: FSMContext):
    await state.update_data(estimated_cost=message.text)
    back_button = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='Назад')],
                  [KeyboardButton(text='Заказать консультацию')],
                  [KeyboardButton(text='Посмотреть всю коллекцию')]],
        resize_keyboard=True
    )
    for bouquet in flower_bouquets.values():
        if bouquet['price_range'] == 'свыше 2000':
            await message.answer(text=
                                 f'Цена: {bouquet['price']}\n'
                                 f'Описание: {bouquet['description']}\n'
                                 f'Фотография: {bouquet['image']}\n',
                                 reply_markup=create_inline_keyboard(bouquet['id'])
                                 )

    await message.answer(f"Выберите букет. Если хотите что-то еще более уникальное,\n"
                         f"подберите другой букет из нашей коллекции или закажите консультацию флориста.", reply_markup=back_button)
    await state.set_state(OrderFlower.bouquet)


@user_private_router.message(OrderFlower.estimated_cost, F.text.contains('500'))
async def get_under_500(message: types.Message, state: FSMContext):
    await state.update_data(estimated_cost=message.text)
    back_button = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='Назад')],
                  [KeyboardButton(text='Заказать консультацию')],
                  [KeyboardButton(text='Посмотреть всю коллекцию')]],
        resize_keyboard=True
    )
    for bouquet in flower_bouquets.values():
        if bouquet['price_range'] == 'до 500':
            await message.answer(text=
                                 f'Цена: {bouquet['price']}\n'
                                 f'Описание: {bouquet['description']}\n'
                                 f'Фотография: {bouquet['image']}\n',
                                 reply_markup=create_inline_keyboard(bouquet['id'])
                                 )

    await message.answer("Выберите букет. Если хотите что-то еще более уникальное,\n"
                         f"подберите другой букет из нашей коллекции или закажите консультацию флориста.", reply_markup=back_button)
    await state.set_state(OrderFlower.bouquet)


@user_private_router.message(OrderFlower.estimated_cost, F.text.contains('1000'))
async def get_under_1000(message: types.Message, state: FSMContext):
    await state.update_data(estimated_cost=message.text)
    back_button = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='Назад')],
                  [KeyboardButton(text='Заказать консультацию')],
                  [KeyboardButton(text='Посмотреть всю коллекцию')]],
        resize_keyboard=True
    )
    for bouquet in flower_bouquets.values():
        if bouquet['price_range'] == 'до 1000':
            await message.answer(text=
                                 f'Цена: {bouquet['price']}\n'
                                 f'Описание: {bouquet['description']}\n'
                                 f'Фотография: {bouquet['image']}\n',
                                 reply_markup=create_inline_keyboard(bouquet['id'])
                                 )

    await message.answer("Выберите букет. Если хотите что-то еще более уникальное,\n"
                         f"подберите другой букет из нашей коллекции или закажите консультацию флориста.", reply_markup=back_button)
    await state.set_state(OrderFlower.bouquet)


@user_private_router.message(OrderFlower.estimated_cost, F.text.contains('2000'))
async def get_under_2000(message: types.Message, state: FSMContext):
    await state.update_data(estimated_cost=message.text)
    back_button = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='Назад')],
                  [KeyboardButton(text='Заказать консультацию')],
                  [KeyboardButton(text='Посмотреть всю коллекцию')]],
        resize_keyboard=True
    )
    for bouquet in flower_bouquets.values():
        if bouquet['price_range'] == 'до 2000':
            await message.answer(text=
                                 f'Цена: {bouquet['price']}\n'
                                 f'Описание: {bouquet['description']}\n'
                                 f'Фотография: {bouquet['image']}\n',
                                 reply_markup=create_inline_keyboard(bouquet['id'])
                                 )

    await message.answer("Выберите букет. Если хотите что-то еще более уникальное,\n"
                         f"подберите другой букет из нашей коллекции или закажите консультацию флориста.", reply_markup=back_button)
    await state.set_state(OrderFlower.bouquet)


@user_private_router.message(F.text == 'Назад')
async def go_back(message: types.Message, state: FSMContext):
    await message.answer("Вы вернулись назад. Выберите примерную стоимость букета.",
                         reply_markup=create_reply_keyboard(get_price_range(flower_bouquets)))
    await state.set_state(OrderFlower.estimated_cost)


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
    await state.clear()
    collection_kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='Посмотреть всю коллекцию')]],
        resize_keyboard=True
    )
    await message.answer(f"Ваш номер: {number_phone['phone_number']}\n"
                         f"Флорист скоро свяжется с вами.\n"
                         f"А пока можете присмотреть что-нибудь из готовой коллекции",
                         reply_markup=collection_kb)
    await state.set_state(OrderFlower.bouquet)


@user_private_router.message(OrderFlower.bouquet, F.text.contains('Посмотреть всю коллекцию'))
async def get_choose_bouquet(message: types.Message, state: FSMContext):
    for bouquet in flower_bouquets.values():
        await message.answer(text=
                             f'Цена: {bouquet['price']}\n'
                             f'Описание: {bouquet['description']}\n'
                             f'Фотография: {bouquet['image']}\n',
                             reply_markup=create_inline_keyboard(bouquet['id'])
                             )
    await state.set_state(OrderFlower.bouquet)


@user_private_router.callback_query(F.data.startswith('Выбран '))
async def select_bouquet(callback: types.CallbackQuery, state: FSMContext):
    bouquet_id = callback.data.split('_')
    await state.update_data(bouquet=bouquet_id)
    await callback.message.answer(f'Вы выбрали букет, введите своё имя', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    await callback.answer()
    await state.set_state(OrderFlower.name)


@user_private_router.message(OrderFlower.name, F.text)
async def get_user_info_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите адрес доставки.')
    await state.set_state(OrderFlower.address)
    'Введите дату доставки в формате ДД.ММ.ГГ ЧЧ:ММ (+20% если в течении 24 часов):'

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
    await message.answer(f'Заказ принят🤙 {data}')
    await state.clear()
