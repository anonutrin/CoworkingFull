from .loggin_middleware import LoggingMiddleware


async def setup_middlewares(dp):
    dp.middleware.setup(LoggingMiddleware())
