from aiogram.dispatcher.filters.state import StatesGroup, State


class StateAddOneHotel(StatesGroup):
    title = State()
    description = State()
    price = State()
    short_description = State()
    work_schedule = State()
    latitude = State()
    longitude = State()
    contact_link = State()
    photos = State()
