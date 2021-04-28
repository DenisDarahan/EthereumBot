from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from botapp.middlewares import i18n


_ = i18n.gettext


def cancel_menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.row(KeyboardButton(_('cancel_button')))
    return m


def cancel_or_skip_menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.row(KeyboardButton(_('skip_button')))
    m.row(KeyboardButton(_('cancel_button')))
    return m
