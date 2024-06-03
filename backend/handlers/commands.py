from aiogram import types
from aiogram.dispatcher import FSMContext
from config.settings import settings
from database.commands.bot_activation_stats import increment_activation_count
from database.commands.location_visit_stats import select_or_create_location_visit_stat, update_location_visit_stat
from database.commands.telegram_users import add_user, increase_bot_activation_count
from handlers.admin.catalog import send_location_info
from keyboards.inline import channel_link_kb, inline_web_app, generate_menu_kb
from keyboards.reply import start_menu_kb
from loader import dp, bot
from names import START, CANCEL, start_bot_text_template, START_BTN
from utils.logger import logger


@dp.message_handler(commands=[START], state='*')
async def start_bot(message: types.Message, state: FSMContext):
    try:
        await state.finish()
        chat_id, username = message.from_user.id, message.from_user.username
        await add_user(chat_id, username)
        await increase_bot_activation_count(chat_id)
        await increment_activation_count()
        # user_info = await bot.get_chat_member(settings.CHANNEL_ID, chat_id)

        # if not user_info.is_chat_member():
        #     return await message.answer(
        #         'Привет! Мы рады приветствовать тебя в нашем боте!\n\n'
        #         'Перед тем, как начать работу, подпишись на наш канал, нажав на кнопку ниже⬇\n\n'
        #         'А потом возвращайся в бот и нажми СТАРТ',
        #         reply_markup=await channel_link_kb(settings.CHANNEL_LINK)
        #     )
        await bot.send_message(chat_id, start_bot_text_template(), reply_markup=await generate_menu_kb(chat_id))
        # await bot.send_message(chat_id, start_bot_text_template(), reply_markup=await start_menu_kb(chat_id))
        args = message.get_args()
        if args and 'location_' in args:
            try:
                location_id = int(message.get_args().split('location_')[1])
                if await send_location_info(chat_id, location_id):
                    location_visit_stat = await select_or_create_location_visit_stat(chat_id, location_id)
                    await update_location_visit_stat(location_visit_stat)

            except Exception as ex:
                logger.error(f'Can not get location_id from args: {ex}')

    except Exception as ex:
        logger.error(ex)


@dp.callback_query_handler(text_contains='menu', state='*')
async def get_menu_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.edit_text(
        start_bot_text_template(),
        reply_markup=await generate_menu_kb(callback.from_user.id)
    )


@dp.message_handler(text=CANCEL, state='*')
async def cancel(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    await bot.send_message(chat_id, 'Отменено!')
    await state.finish()


@dp.callback_query_handler(text_contains=START_BTN)
async def handle_start_button(callback: types.CallbackQuery):
    chat_id = callback.from_user.id
    user_info = await bot.get_chat_member(settings.CHANNEL_ID, chat_id)
    if not user_info.is_chat_member():
        return await callback.answer('Вам нужно подписаться на канал')

    await bot.send_message(chat_id, start_bot_text_template(),
                           reply_markup=await generate_menu_kb(chat_id))
