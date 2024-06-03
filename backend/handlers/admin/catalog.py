from aiogram import types

from database.commands.location import select_location_by_id
from database.commands.telegram_users import user_is_admin
from keyboards.inline import catalog_actions_kb, contact_kb, type_of_adding
from loader import dp, bot
from names import CATALOG_MANAGE, ADD_HOTEL
from storage.utils import return_media_by_location
from utils.logger import logger


async def send_location_info(chat_id, location_id):
    try:
        location = await select_location_by_id(location_id)
        text = f"<b>{location.title}\n\n" \
               f"<i>{location.description}</i></b>\n\n" \
               f"<i>{location.price}</i>\n\n" \
               f"<b>{location.work_schedule or ''}</b>"
        if location:
            media = await return_media_by_location(location)
            markup = None
            try:
                contact_link = location.contact_link
                if 'https://' in location.contact_link:
                    markup = contact_kb(contact_link)
            except:
                pass

            if len(media) == 1:
                await bot.send_photo(chat_id, media[0], caption=text, reply_markup=markup if markup is not None else None)

            else:
                message_kwargs = dict(
                    chat_id=chat_id,
                    text=text,
                    reply_markup=markup if markup is not None else None
                )

                if len(media) > 0:
                    nested_message = await bot.send_media_group(media=media[:10], chat_id=chat_id)
                    message_kwargs['reply_to_message_id'] = nested_message[0].message_id

                await bot.send_message(**message_kwargs)
            return True
        else:
            await bot.send_message(
                chat_id=chat_id,
                text="Извините, информация об этой локации не доступна."
            )
            return False

    except Exception as ex:
        logger.error(f'An unexpected error occurred while sending location info: {ex}')
        return False


@dp.message_handler(text=[CATALOG_MANAGE])
async def catalog_manage(message: types.Message):
    chat_id = message.from_user.id
    if await user_is_admin(chat_id):
        await bot.send_message(chat_id, 'Выберите действие:', reply_markup=await catalog_actions_kb())


@dp.callback_query_handler(text_contains=ADD_HOTEL)
async def get_location_list(callback: types.CallbackQuery):
    chat_id = callback.from_user.id
    if await user_is_admin(chat_id):
        await callback.message.edit_text('Выберите тип добавления:', reply_markup=await type_of_adding())
