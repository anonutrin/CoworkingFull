from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode

import names
from database.commands import location
from database.commands import telegram_users
from keyboards.prmoted.location_kb import keyboard_for_promoted_location, confirm_promote_keyboard
from keyboards.reply import start_menu_kb
from loader import dp
from names import PROMOTE_LOCATION
from promote.locations import newsletter_for_all_users_promoted_location
from states.promote_location import PromoteLocationForm


@dp.message_handler(commands=['cancel'], state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    await message.answer('<b>Отменено</b>')
    return await state.finish()


@dp.message_handler(commands=[PROMOTE_LOCATION])
async def promote_location_handler(message: types.Message, state: FSMContext):
    if not await telegram_users.user_is_admin(message.from_user.id):
        return

    command_parts = message.get_args().split(maxsplit=1)
    if not command_parts:
        await message.answer(f"Вы не указали ID локации. Используйте /{PROMOTE_LOCATION} [location_id]")
        return
    try:
        location_id = int(command_parts[0])
        location_item = await location.select_location_by_id(location_id)

        if location_item is None:
            raise Exception(f'Локации с ID {location_id} не существует.')

        await message.answer(f'Продвигаемая локация: <code>{location_item.title}</code>\n'
                             f'Отправьте рекламный текст или нажмите /cancel чтобы отменить.')

    except ValueError:
        return await message.answer(f'ID локации должно быть числом. Используйте /{PROMOTE_LOCATION} [location_id]')
    except Exception as ex:
        return await message.answer(str(ex))

    async with state.proxy() as data:
        data['location_id'] = location_id

    await PromoteLocationForm.waiting_for_ad_text.set()


@dp.message_handler(state=PromoteLocationForm.waiting_for_ad_text, content_types=types.ContentTypes.TEXT)
async def process_promote_text_handler(message: types.Message, state: FSMContext):

    promote_text = message.text
    confirm_text = f"Ваш рекламный текст:\n\n{promote_text}\n\n"
    async with state.proxy() as data:
        location_id = data['location_id']
        data['promote_text'] = promote_text

    inline_keyboard = await keyboard_for_promoted_location(location_id)
    await message.answer(confirm_text, reply_markup=inline_keyboard, parse_mode=ParseMode.MARKDOWN)
    await message.answer('<b>Подтвердить продвижение локации?</b>', reply_markup=await confirm_promote_keyboard())
    await PromoteLocationForm.next()


@dp.message_handler(state=PromoteLocationForm.confirm_promote)
async def confirmation_promote_handler(message: types.Message, state: FSMContext):
    decision = message.text
    yes_or_no = [names.YES, names.NO]
    if decision not in yes_or_no:
        return await message.answer(f'Выберите одно из двух значений: <b>{"/".join(yes_or_no)}</b>')

    if decision in names.YES:
        async with state.proxy() as data:
            await newsletter_for_all_users_promoted_location(data['location_id'], data['promote_text'])
    else:
        await message.answer(
            '<b>Продвижение локации отменено!</b>'
        )

    return await state.finish()
