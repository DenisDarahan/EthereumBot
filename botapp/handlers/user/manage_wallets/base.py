from aiogram.types import Message, CallbackQuery, ChatType

from botapp.misc import bot, dp
from botapp.middlewares import i18n
from botapp.states import User
from botapp import db, markups, utils


_ = i18n.gettext


@dp.message_handler(ChatType.is_private, lambda message: message.text == _('manage_wallets_button'),
                    state=User.main)
async def process_manage_wallets(message: Message):
    user_wallets = await db.get_user_wallets(message.chat.id)
    if not user_wallets:
        await bot.send_message(message.chat.id,
                               _('absent_wallets_error'),
                               reply_markup=markups.user.process_main_menu())
        return
    await bot.send_message(message.chat.id,
                           _('manage_wallets'),
                           reply_markup=markups.user.process_manage_wallets_menu(user_wallets))


@dp.callback_query_handler(lambda call: 'get-user-wallet_' in call.data, state=User.main)
async def get_user_wallet(call: CallbackQuery):
    await call.answer(_('ask_user_wait_for_wallet_info'))
    wallet_id = call.data.split('_')[-1]
    user_wallet = await db.get_user_wallet(wallet_id)
    if user_wallet:
        wallet, name = user_wallet
        balance = await utils.get_user_balance(wallet)
        await call.message.edit_text(
            _('get_user_wallet').format(wallet=wallet, name=name, balance=balance),
            reply_markup=markups.user.get_wallet_menu(wallet_id),
            disable_web_page_preview=True
        )
        return
    await call.answer(_('wallet_not_found_error'))
    await process_return_to_user_wallets(call)


@dp.callback_query_handler(lambda call: 'ask-delete-user-wallet_' in call.data, state=User.main)
async def process_ask_delete_user_wallet(call: CallbackQuery):
    wallet_id = call.data.split('_')[-1]
    await call.message.edit_text(_('ask_delete_wallet'),
                                 reply_markup=markups.user.ask_delete_user_wallet_menu(wallet_id))


@dp.callback_query_handler(lambda call: 'accept-delete-user-wallet_' in call.data, state=User.main)
async def process_accept_delete_user_wallet(call: CallbackQuery):
    wallet_id = call.data.split('_')[-1]
    await db.delete_user_wallet(wallet_id)
    await call.answer(_('success_wallet_delete'))
    await process_return_to_user_wallets(call)


@dp.callback_query_handler(lambda call: 'decline-delete-user-wallet_' in call.data, state=User.main)
async def process_decline_delete_user_wallet(call: CallbackQuery):
    await call.answer(_('cancel_wallet_delete'))
    await get_user_wallet(call)


@dp.callback_query_handler(text='return-to-user-wallets', state=User.main)
async def process_return_to_user_wallets(call: CallbackQuery):
    user_wallets = await db.get_user_wallets(call.message.chat.id)
    if user_wallets:
        await call.message.edit_text(_('manage_wallets'),
                                     reply_markup=markups.user.process_manage_wallets_menu(user_wallets))
        return
    await call.message.delete()
    await bot.send_message(call.message.chat.id,
                           _('absent_wallets_error'),
                           reply_markup=markups.user.process_main_menu())
