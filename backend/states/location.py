from aiogram.dispatcher.filters.state import StatesGroup, State


class StateLocation(StatesGroup):
    city = State()
