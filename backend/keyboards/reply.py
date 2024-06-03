import urllib.parse

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

from config.settings import settings
from database.commands.telegram_users import user_is_admin, select_user

from names import OBJECTS_MAP, CATALOG_MANAGE, CANCEL, CONFIRM, NEXT, CHANGE_LOCATION, RESET, GO_BACK, \
    FILTER_PRICE, FILTER_SPHERE, MAKE_UP, MANICURE, COLORIST, VISAGISTE, HAIRDRESSER, ALL


def web_app_link(coordinates=None, price_to=None, sphere=None, user_avatar=None):
    if coordinates is None:
        coordinates = [55.76, 37.64]

    params = {'latitude': coordinates[0], 'longitude': coordinates[1]} if len(coordinates) else {}
    if price_to:
        params['priceTo'] = price_to

    if sphere:
        params['sphere'] = sphere

    if user_avatar:
        params['user_avatar'] = user_avatar

    url = f'{settings.WEB_APP_SITE}?{(urllib.parse.urlencode(params))}'

    return WebAppInfo(
        url=url
    )


async def start_menu_kb(chat_id):
    is_admin = await user_is_admin(chat_id)
    user = await select_user(chat_id)
    city = user.chose_location
    coordinates = settings.CITIES[city]

    keyboards = [
        [
            KeyboardButton(text=OBJECTS_MAP, web_app=web_app_link(coordinates=coordinates))
        ],
        [
            KeyboardButton(text=CHANGE_LOCATION)
        ]
    ]
    if is_admin:
        keyboards.append([
            KeyboardButton(text=CATALOG_MANAGE)
        ])
    return ReplyKeyboardMarkup(keyboards, resize_keyboard=True)


cancel_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=CANCEL)]
], resize_keyboard=True)

confirm_photo_load_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=CONFIRM)],
    [KeyboardButton(text=CANCEL)]
], resize_keyboard=True)


def get_filters_kb():
    keyboards = [
        [
            KeyboardButton(text=FILTER_PRICE),
            KeyboardButton(text=FILTER_SPHERE)
        ],
        [
            KeyboardButton(text=RESET)
        ],
        [
            KeyboardButton(text=CANCEL)
        ]
    ]
    return ReplyKeyboardMarkup(keyboards, resize_keyboard=True)


next_load_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=NEXT)],
], resize_keyboard=True)


def get_sphere_kb():
    keyboards = [
        [
            KeyboardButton(text=MAKE_UP),
            KeyboardButton(text=MANICURE),
        ],
        [
            KeyboardButton(text=COLORIST),
            KeyboardButton(text=VISAGISTE),
        ],
        [
            KeyboardButton(text=HAIRDRESSER),
            KeyboardButton(text=ALL)
        ],
        [
            KeyboardButton(text=GO_BACK)
        ]

    ]
    return ReplyKeyboardMarkup(keyboards, resize_keyboard=True)


def filter_go_back_kb():
    return ReplyKeyboardMarkup([[KeyboardButton(text=GO_BACK)]], resize_keyboard=True)


def get_city_kb():
    buttons = [[KeyboardButton(text=city)] for city in settings.CITIES]
    buttons.append([KeyboardButton(text=CANCEL)])
    return ReplyKeyboardMarkup(keyboard=buttons)
