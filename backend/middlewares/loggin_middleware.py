from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from config.settings import settings
from keyboards.inline import channel_link_kb
from loader import bot
from names import START, START_BTN
from utils.logger import logger

# pre-process update
# process update
# pre-process message|callback_query
# filter (lambda)
# handler
# post process message
# post process update


class LoggingMiddleware(BaseMiddleware):
    @staticmethod
    async def logging_message(user_id, user_name, message, log_name='msg'):
        text = f"{user_id} - {user_name} - {log_name}({message})"
        logger.info(text)

    async def on_process_message(self, message: types.Message, data: dict):
        try:
            if message is None:
                return

            chat_id, username, text = message.chat.id, message.from_user.username, message.text
            await self.logging_message(chat_id, username, text, log_name='msg')

            if START in text:
                return

            user_info = await bot.get_chat_member(settings.CHANNEL_ID, chat_id)
            if not user_info.is_chat_member():
                await message.answer(
                    'Привет! Мы рады приветствовать тебя в нашем боте!\n\n'
                    'Перед тем, как начать работу, подпишись на наш канал, нажав на кнопку ниже⬇\n\n'
                    'А потом возвращайся в бот и нажми СТАРТ',
                    reply_markup=await channel_link_kb(settings.CHANNEL_LINK)
                )
                raise CancelHandler()
        except Exception as ex:
            logger.error(ex)

    async def on_process_callback_query(self, callback: types.CallbackQuery, data: dict):
        chat_id, username, query = callback.from_user.id, callback.from_user.username, callback.data
        await self.logging_message(chat_id, username, query, log_name='call_query')

        if START_BTN in query:
            return

        try:
            user_info = await bot.get_chat_member(settings.CHANNEL_ID, chat_id)
            if not user_info.is_chat_member():
                await callback.message.answer(
                    'Привет! Мы рады приветствовать тебя в нашем боте!\n\n'
                    'Перед тем, как начать работу, подпишись на наш канал, нажав на кнопку ниже⬇\n\n'
                    'А потом возвращайся в бот и нажми СТАРТ',
                    reply_markup=await channel_link_kb(settings.CHANNEL_LINK)
                )
                raise CancelHandler()
        except Exception as ex:
            logger.error(ex)
