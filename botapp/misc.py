from asyncio import get_event_loop

from aiohttp import web
from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from botapp.middlewares import i18n
from botapp.config import BOT_NAME, TOKEN, WEBHOOK_URL, CERTIFICATE, REDIS


loop = get_event_loop()
bot = Bot(TOKEN, parse_mode='HTML', loop=loop)
storage = RedisStorage2(db=REDIS, prefix=BOT_NAME, loop=loop)
dp = Dispatcher(bot, loop, storage)
redis = loop.run_until_complete(storage.redis())

dp.middleware.setup(i18n)


async def on_startup(_dispatcher):
    web_hook = await bot.get_webhook_info()
    if web_hook.url != WEBHOOK_URL:
        if not web_hook.url:
            await bot.delete_webhook()
        await bot.set_webhook(WEBHOOK_URL, certificate=CERTIFICATE.open())
    print(await bot.get_webhook_info())
    print(await bot.get_me())


async def on_shutdown(_dispatcher):
    await bot.delete_webhook()
    await bot.session.close()
    await dp.storage.close()
    await dp.storage.wait_closed()


def setup_bot(app: web.Application):
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
