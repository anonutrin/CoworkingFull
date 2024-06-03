from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.reply import web_app_link
from keyboards.utils import ctc
from names import __SH, ADD_HOTEL, ARROW_LEFT, ARROW_RIGHT, GO_BACK, __BACK, \
    SEVERAL_HOTELS, CATALOG_MANAGE, SUBSCRIBE, START_BTN, CHANGE_LOCATION, OBJECTS_MAP
from utils.telegram import get_user_avatar


async def generate_menu_kb(chat_id: int):
    user_avatar = await get_user_avatar(chat_id)

    print(user_avatar)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=OBJECTS_MAP, web_app=web_app_link(user_avatar=user_avatar))],
        [InlineKeyboardButton(text=CHANGE_LOCATION, callback_data='change_location')],
    ])


async def generate_location_kb(locations: list):
    buttons = [[InlineKeyboardButton(text=location, callback_data=location)] for location in locations]
    buttons = [*buttons, [InlineKeyboardButton(text=GO_BACK, callback_data="menu")]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def inline_web_app(chat_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Поиск локаций', web_app=web_app_link())]
    ])


def contact_kb(contact_link, text='Связаться с продавцом'):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=text, url=contact_link),
        ]
    ])


async def catalog_actions_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=ADD_HOTEL, callback_data=ADD_HOTEL)]
    ])


async def hotels_list_kb(hotels_title):
    inline_keyboard = [[InlineKeyboardButton(text=hotel[1], callback_data=ctc(hotel[0], __SH))] for hotel in
                       hotels_title]
    inline_keyboard.append(
        [
            InlineKeyboardButton(text=ARROW_LEFT, callback_data=ARROW_LEFT),
            InlineKeyboardButton(text=ARROW_RIGHT, callback_data=ARROW_RIGHT),

        ]
    )
    inline_keyboard.append([InlineKeyboardButton(text=GO_BACK, callback_data=ctc(CATALOG_MANAGE, __BACK))])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def type_of_adding():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=SEVERAL_HOTELS, callback_data=SEVERAL_HOTELS)],
        [InlineKeyboardButton(text=GO_BACK, callback_data=ctc(CATALOG_MANAGE, __BACK))]
    ])


async def start_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=START_BTN, callback_data=START_BTN)],
    ])


async def channel_link_kb(url):
    print(url)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=SUBSCRIBE, callback_data='channel_link', url=url)],
        [InlineKeyboardButton(text=START_BTN, callback_data=START_BTN)],
    ])
