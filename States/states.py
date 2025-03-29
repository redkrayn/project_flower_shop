from aiogram.fsm.state import StatesGroup, State


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