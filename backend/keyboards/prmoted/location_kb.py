from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from keyboards.utils import ctc
import names


async def keyboard_for_promoted_location(location_id):
    return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=names.SHOW_PROMOTED_LOCATION, callback_data=ctc(location_id, names.__SH))]
        ])


async def confirm_promote_keyboard():
    return ReplyKeyboardMarkup([
        [
            KeyboardButton(text=names.YES),
            KeyboardButton(text=names.NO)
        ]
    ], resize_keyboard=True)
