from aiogram.dispatcher.webhook import get_new_configured_app
from aiohttp import web

from botapp.misc import setup_bot, dp
from botapp.config import BOT_SERVER, PATH
from botapp import handlers


if __name__ == '__main__':
    print(handlers.handlers_loaded())
    app = get_new_configured_app(dispatcher=dp, path=f'/{PATH}/')
    setup_bot(app)
    web.run_app(app, **BOT_SERVER)
