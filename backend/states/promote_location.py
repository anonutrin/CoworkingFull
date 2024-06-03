from aiogram.dispatcher.filters.state import StatesGroup, State


class PromoteLocationForm(StatesGroup):
    waiting_for_ad_text = State()
    confirm_promote = State()
