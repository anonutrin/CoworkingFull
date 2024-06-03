from config.settings import settings


async def on_startup(dp):
    from utils.setup import set_default_commands
    await set_default_commands(dp)

    from middlewares import setup_middlewares
    await setup_middlewares(dp)

    import asyncio
    from api_server.app import run_api_server

    asyncio.create_task(run_api_server(host=settings.SERVER_HOST, port=settings.SERVER_PORT, debug=False))


def run_telegram_bot():
    from handlers import dp
    from aiogram.utils import executor

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


if __name__ == '__main__':
    from utils.logger import logger

    try:
        import django_configure

        django_configure.configure_django()

        run_telegram_bot()
    except Exception as ex:
        logger.error(ex)
