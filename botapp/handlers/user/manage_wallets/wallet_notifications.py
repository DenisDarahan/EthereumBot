from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from botapp.misc import bot, dp
from botapp.states import User
from botapp.middlewares import i18n
from botapp import db, markups
from .base import process_return_to_user_wallets, get_user_wallet


_ = i18n.gettext


async def end_get_min_amount(message: Message, state: FSMContext, filter_id: str):
    await state.finish()
    await User.main.set()

    wallet_notifications_params = await db.get_wallet_notifications_params_on_filter(filter_id)
    if wallet_notifications_params:
        name, wallet, min_amount, tr_type, off_sound, notify = wallet_notifications_params

        await bot.send_message(
            message.chat.id,
            _('wallet_notifications').format(
                name=name, wallet=wallet, amount=f'{min_amount:.10f}'.rstrip('0').rstrip('.'),
                tr_type=_(f'tr_type_{tr_type}')
            ),
            reply_markup=markups.user.get_wallet_notifications_menu(filter_id, off_sound, notify),
            disable_web_page_preview=True
        )
        return

    await bot.send_message(message.chat.id,
                           _('wallet_not_found_error'),
                           reply_markup=markups.user.process_main_menu())


@dp.callback_query_handler(lambda call: 'get-user-wallet-notifications_' in call.data, state=User.main)
async def process_get_wallet_notifications(call: CallbackQuery):
    wallet_id = call.data.split('_')[-1]

    wallet_notifications_params = await db.get_wallet_notifications_params(wallet_id)
    if wallet_notifications_params:
        name, wallet, filter_id, min_amount, tr_type, off_sound, notify = wallet_notifications_params

        await call.message.edit_text(
            _('wallet_notifications').format(
                name=name, wallet=wallet, amount=f'{min_amount:.10f}'.rstrip('0').rstrip('.'),
                tr_type=_(f'tr_type_{tr_type}')
            ),
            reply_markup=markups.user.get_wallet_notifications_menu(filter_id, off_sound, notify),
            disable_web_page_preview=True
        )
        return

    await call.answer(_('wallet_not_found_error'))
    await process_return_to_user_wallets(call)


@dp.callback_query_handler(lambda call: 'change-wallet-notifications-filter-amount_' in call.data, state=User.main)
async def process_change_wallet_notifications_amount(call: CallbackQuery, state: FSMContext):
    filter_id = call.data.split('_')[-1]
    await User.min_amount.set()
    await state.set_data({'filter_id': filter_id})
    await call.message.delete()
    await bot.send_message(call.message.chat.id,
                           _('ask_get_min_amount'),
                           reply_markup=markups.base.cancel_menu())


@dp.message_handler(lambda message: message.text == _('cancel_button'), state=User.min_amount)
async def process_cancel_get_min_amount(message: Message, state: FSMContext):
    await bot.send_message(message.chat.id,
                           _('cancel_get_amount'),
                           reply_markup=markups.user.process_main_menu())
    filter_id = (await state.get_data()).get('filter_id', '0')
    await end_get_min_amount(message, state, filter_id)


@dp.message_handler(state=User.min_amount)
async def process_get_min_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text.replace(',', '.'))
        if amount < 10 ** (-10) or amount > 9999999999.9999999999:
            raise ValueError
    except ValueError:
        await bot.send_message(message.chat.id,
                               _('wrong_amount_error'),
                               reply_markup=markups.base.cancel_menu())
    else:
        await bot.send_message(message.chat.id,
                               _('success_get_amount'),
                               reply_markup=markups.user.process_main_menu())
        filter_id = (await state.get_data()).get('filter_id', '0')
        await db.set_notifications_filter_min_amount(filter_id, amount)
        await end_get_min_amount(message, state, filter_id)


@dp.callback_query_handler(lambda call: 'change-wallet-notifications-filter-tr-type_' in call.data, state=User.main)
async def process_change_wallet_notifications_filter_tr_type(call: CallbackQuery):
    filter_id = call.data.split('_')[-1]
    await call.answer(_('ask_get_tr_type'))
    _min_amount, tr_type = await db.get_wallet_notifications_filters(filter_id)
    await call.message.edit_reply_markup(markups.user.get_notifications_filter_tr_type(filter_id, tr_type))


@dp.callback_query_handler(lambda call: 'set-notifications-filter-tr-type_' in call.data, state=User.main)
async def process_set_notifications_filter_tr_type(call: CallbackQuery):
    tr_type, filter_id = call.data.split('_')[-1].split('-')
    await db.set_notifications_filter_tr_type(filter_id, tr_type)
    call.data = f'get-wallet-notifications-filters_{filter_id}'
    await process_get_wallet_notifications_filters(call)


@dp.callback_query_handler(lambda call: 'get-wallet-notifications-filters_' in call.data, state=User.main)
async def process_get_wallet_notifications_filters(call: CallbackQuery):
    filter_id = call.data.split('_')[-1]

    wallet_notifications_params = await db.get_wallet_notifications_params_on_filter(filter_id)
    if wallet_notifications_params:
        await call.answer(_('notifications_filters'))
        name, wallet, min_amount, tr_type, _off_sound, _notify = wallet_notifications_params

        await call.message.edit_text(
            _('wallet_notifications').format(
                name=name, wallet=wallet, amount=f'{min_amount:.10f}'.rstrip('0').rstrip('.'),
                tr_type=_(f'tr_type_{tr_type}')
            ),
            reply_markup=markups.user.get_wallet_notifications_filters_menu(filter_id),
            disable_web_page_preview=True)
        return
    await call.answer(_('wallet_not_found_error'))
    await process_return_to_user_wallets(call)


@dp.callback_query_handler(lambda call: 'return-to-wallet-notifications_' in call.data, state=User.main)
async def process_return_to_wallet_notifications(call: CallbackQuery):
    filter_id = call.data.split('_')[-1]
    wallet_id = await db.get_wallet_id_on_notifications_filter(filter_id)
    call.data = f'get-user-wallet-notifications_{wallet_id}'
    await process_get_wallet_notifications(call)


@dp.callback_query_handler(lambda call: 'change-wallet-notifications_' in call.data, state=User.main)
async def process_change_wallet_notifications(call: CallbackQuery):
    filter_id = call.data.split('_')[-1]
    await db.change_wallet_notifications(filter_id)
    wallet_notifications_params = await db.get_wallet_notifications_alert_params(filter_id)
    if wallet_notifications_params:
        off_sound, notify = wallet_notifications_params
        await call.message.edit_reply_markup(markups.user.get_wallet_notifications_menu(filter_id, off_sound, notify))
        return
    await call.answer(_('wallet_not_found_error'))
    await process_return_to_user_wallets(call)


@dp.callback_query_handler(lambda call: 'change-wallet-off-sound_' in call.data, state=User.main)
async def process_change_wallet_off_sound(call: CallbackQuery):
    filter_id = call.data.split('_')[-1]
    await db.change_wallet_off_sound(filter_id)
    wallet_notifications_params = await db.get_wallet_notifications_alert_params(filter_id)
    if wallet_notifications_params:
        off_sound, notify = wallet_notifications_params
        await call.message.edit_reply_markup(markups.user.get_wallet_notifications_menu(filter_id, off_sound, notify))
        return
    await call.answer(_('wallet_not_found_error'))
    await process_return_to_user_wallets(call)


@dp.callback_query_handler(lambda call: 'n-return-to-wallet-menu_' in call.data, state=User.main)
async def process_n_return_to_wallet_menu(call: CallbackQuery):
    filter_id = call.data.split('_')[-1]
    wallet_id = await db.get_wallet_id_on_notifications_filter(filter_id)
    call.data = f'get-user-wallet_{wallet_id}'
    await get_user_wallet(call)
