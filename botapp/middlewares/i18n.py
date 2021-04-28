from typing import Any, Tuple
from pathlib import Path

from babel import Locale
from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware

from botapp import db
from botapp.misc import redis


I18N_DOMAIN = 'ethereum'
LOCALES_DIR = Path(__file__).parent.parent.parent / 'locales'
locales = {'ru': Locale('ru', 'RU'),
           'en': Locale('en', 'US')}


async def set_lang(user_id, lang):
    await redis.hset('lang', user_id, lang)


async def get_lang(user_id):
    lang = await redis.hget('lang', user_id)
    if not lang:
        lang = await db.user.get_lang(user_id)
        await redis.hset('lang', user_id, lang)
        return lang
    return lang.decode('utf-8')


class MyI18nLocale(I18nMiddleware):
    def __init__(self, domain, path=None, default='ru'):
        super().__init__(domain, path, default)

    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        user: types.User = types.User.get_current()
        try:
            locale: Locale = locales[await get_lang(user.id)]
        except AttributeError:
            locale = Locale('ru')

        if locale:
            *_, data = args
            language = data['locale'] = locale.language
            return language


i18n = MyI18nLocale(I18N_DOMAIN, LOCALES_DIR)
