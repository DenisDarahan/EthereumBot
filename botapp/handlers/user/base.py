from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ChatType, CallbackQuery

from botapp.misc import bot, dp
from botapp.middlewares import i18n, set_lang
from botapp.states import User
from botapp import db, markups


_ = i18n.gettext


@dp.message_handler(ChatType.is_private, commands=['start'], state='*')
async def process_start(message: Message, state: FSMContext):
    await state.finish()
    if not await db.is_user(message.chat.id):
        await bot.send_message(message.chat.id,
                               'Пожалуйста, выберите язык\n'
                               'Please, choose your language',
                               reply_markup=markups.user.lang_choose())
        return

    await User.main.set()
    await bot.send_message(message.chat.id,
                           _('start_message'),
                           reply_markup=markups.user.process_main_menu())


@dp.callback_query_handler(lambda call: 'lang_' in call.data, state='*')
async def choose_language(call: CallbackQuery):
    lang = call.data.split('_')[-1]

    await set_lang(call.message.chat.id, lang)
    await db.create_user(call.message.chat.id, lang)
    await User.main.set()

    await call.message.delete()
    await bot.send_message(call.message.chat.id,
                           _('start_message', locale=lang),
                           reply_markup=markups.user.process_main_menu(lang))
