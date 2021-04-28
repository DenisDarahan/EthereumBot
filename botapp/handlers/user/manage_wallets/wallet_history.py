from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from botapp.misc import dp
from botapp.states import User
from botapp.middlewares import i18n
from botapp import db, markups, utils
from .base import process_return_to_user_wallets, get_user_wallet


_ = i18n.gettext


tr_types = {
    '0': [utils.get_wallet_transactions, 'get_norm_trs_button'],
    '1': [utils.get_wallet_internal_transactions, 'get_in_trs_button'],
    '2': [utils.get_wallet_erc20_transactions, 'get_erc20_trs_button'],
    '3': [utils.get_wallet_erc721_transactions, 'get_erc721_trs_button']
}


@dp.callback_query_handler(lambda call: 'get-user-wallet-history_' in call.data, state=User.main)
async def process_get_wallet_history(call: CallbackQuery):
    wallet_id = call.data.split('_')[-1]

    history_filter = await db.get_wallet_history_filter(wallet_id)
    if history_filter:
        await call.answer(_('ask_wait_history'))
        name, wallet, filter_id, records_number, show_participant = history_filter

        normal_transactions = await utils.get_wallet_transactions(wallet, records_number)
        transactions_repr = await utils.get_transactions_repr(wallet, normal_transactions, show_participant)

        await call.message.edit_text(
            _('get_transactions_history').format(
                name=name, wallet=wallet, tr_type=_('get_norm_trs_button'), trs=transactions_repr
            ),
            reply_markup=markups.user.get_wallet_history_menu(filter_id),
            disable_web_page_preview=True
        )
        return

    await call.answer(_('wallet_not_found_error'))
    await process_return_to_user_wallets(call)


@dp.callback_query_handler(lambda call: 'get-normal-transactions-history_' in call.data, state=User.main)
async def process_get_normal_transactions_history(call: CallbackQuery):
    filter_id = call.data.split('_')[-1]

    history_filter = await db.get_wallet_history_filter_on_filter(filter_id)
    if history_filter:
        await call.answer(_('ask_wait_history'))
        name, wallet, records_number, show_participant = history_filter

        normal_transactions = await utils.get_wallet_transactions(wallet, records_number)
        transactions_repr = await utils.get_transactions_repr(wallet, normal_transactions, show_participant)

        await call.message.edit_text(
            _('get_transactions_history').format(
                name=name, wallet=wallet, tr_type=_('get_norm_trs_button'), trs=transactions_repr
            ),
            reply_markup=markups.user.get_wallet_history_menu(filter_id),
            disable_web_page_preview=True
        )
        return

    await call.answer(_('wallet_not_found_error'))
    await process_return_to_user_wallets(call)


@dp.callback_query_handler(lambda call: 'get-internal-transactions-history_' in call.data, state=User.main)
async def process_get_internal_transactions_history(call: CallbackQuery):
    filter_id = call.data.split('_')[-1]

    history_filter = await db.get_wallet_history_filter_on_filter(filter_id)
    if history_filter:
        await call.answer(_('ask_wait_history'))
        name, wallet, records_number, show_participant = history_filter

        internal_transactions = await utils.get_wallet_internal_transactions(wallet, records_number)
        transactions_repr = await utils.get_transactions_repr(wallet, internal_transactions, show_participant)

        await call.message.edit_text(
            _('get_transactions_history').format(
                name=name, wallet=wallet, tr_type=_('get_in_trs_button'), trs=transactions_repr
            ),
            reply_markup=markups.user.get_wallet_history_menu(filter_id, 1),
            disable_web_page_preview=True
        )
        return

    await call.answer(_('wallet_not_found_error'))
    await process_return_to_user_wallets(call)


@dp.callback_query_handler(lambda call: 'get-erc-20-transactions-history_' in call.data, state=User.main)
async def process_get_erc_20_transactions_history(call: CallbackQuery):
    filter_id = call.data.split('_')[-1]

    history_filter = await db.get_wallet_history_filter_on_filter(filter_id)
    if history_filter:
        await call.answer(_('ask_wait_history'))
        name, wallet, records_number, show_participant = history_filter

        internal_transactions = await utils.get_wallet_erc20_transactions(wallet, records_number)
        transactions_repr = await utils.get_transactions_repr(wallet, internal_transactions, show_participant)

        await call.message.edit_text(
            _('get_transactions_history').format(
                name=name, wallet=wallet, tr_type=_('get_erc20_trs_button'), trs=transactions_repr
            ),
            reply_markup=markups.user.get_wallet_history_menu(filter_id, 2),
            disable_web_page_preview=True
        )
        return

    await call.answer(_('wallet_not_found_error'))
    await process_return_to_user_wallets(call)


@dp.callback_query_handler(lambda call: 'get-erc-721-transactions-history_' in call.data, state=User.main)
async def process_get_erc_721_transactions_history(call: CallbackQuery):
    filter_id = call.data.split('_')[-1]

    history_filter = await db.get_wallet_history_filter_on_filter(filter_id)
    if history_filter:
        await call.answer(_('ask_wait_history'))
        name, wallet, records_number, show_participant = history_filter

        internal_transactions = await utils.get_wallet_erc721_transactions(wallet, records_number)
        transactions_repr = await utils.get_transactions_repr(wallet, internal_transactions, show_participant)

        await call.message.edit_text(
            _('get_transactions_history').format(
                name=name, wallet=wallet, tr_type=_('get_erc721_trs_button'), trs=transactions_repr
            ),
            reply_markup=markups.user.get_wallet_history_menu(filter_id, 3),
            disable_web_page_preview=True
        )
        return

    await call.answer(_('wallet_not_found_error'))
    await process_return_to_user_wallets(call)


@dp.callback_query_handler(lambda call: 'get-wallet-history-filters_' in call.data, state=User.main)
async def process_get_wallet_history_filters(call: CallbackQuery):
    filter_id, current_page = call.data.split('_')[-1].split('-')
    await call.message.edit_reply_markup(markups.user.get_wallet_history_filters_menu(filter_id, current_page))


@dp.callback_query_handler(lambda call: 'edit-history-records-number_' in call.data, state=User.main)
async def process_edit_history_records_number(call: CallbackQuery):
    filter_id, current_page = call.data.split('_')[-1].split('-')
    records_number = await db.get_wallet_history_records_number(filter_id)
    if records_number:
        await call.message.edit_reply_markup(
            markups.user.edit_history_records_number_menu(filter_id, records_number[0], current_page)
        )
        return

    await call.answer(_('wallet_not_found_error'))
    await process_return_to_user_wallets(call)


@dp.callback_query_handler(lambda call: 'set-history-records-number_' in call.data, state=User.main)
async def process_set_history_records_number(call: CallbackQuery):
    filter_id, records_number, current_page = call.data.split('_')[-1].split('-')
    if int(records_number) < 1 or int(records_number) > 10:
        await call.answer('not_valid_records_number_error')
        return

    await db.set_wallet_history_records_number(filter_id, records_number)
    await call.message.edit_reply_markup(
        markups.user.edit_history_records_number_menu(filter_id, int(records_number), current_page)
    )


@dp.callback_query_handler(lambda call: 'success-edit-history-filters_' in call.data, state=User.main)
async def process_success_edit_history_records_number(call: CallbackQuery):
    filter_id, current_page = call.data.split('_')[-1].split('-')

    history_filter = await db.get_wallet_history_filter_on_filter(filter_id)
    if history_filter:
        await call.answer(_('ask_wait_history'))
        name, wallet, records_number, show_participant = history_filter

        tr_type = tr_types[current_page]
        transactions = await tr_type[0](wallet, records_number)
        transactions_repr = await utils.get_transactions_repr(wallet, transactions, show_participant)

        await call.message.edit_text(
            _('get_transactions_history').format(
                name=name, wallet=wallet, tr_type=_(tr_type[1]), trs=transactions_repr
            ),
            reply_markup=markups.user.get_wallet_history_filters_menu(filter_id, int(current_page)),
            disable_web_page_preview=True
        )
        return

    await call.answer(_('wallet_not_found_error'))
    await process_return_to_user_wallets(call)


@dp.callback_query_handler(lambda call: 'edit-history-show-participant_' in call.data, state=User.main)
async def process_edit_history_show_participant(call: CallbackQuery):
    filter_id, current_page = call.data.split('_')[-1].split('-')

    show_participant = await db.get_wallet_history_show_participant(filter_id)
    if show_participant:
        await call.message.edit_reply_markup(
            markups.user.edit_history_show_participant_menu(filter_id, show_participant[0], current_page)
        )
        return

    await call.answer(_('wallet_not_found_error'))
    await process_return_to_user_wallets(call)


@dp.callback_query_handler(lambda call: 'set-history-show-participant_' in call.data, state=User.main)
async def process_edit_history_show_participant(call: CallbackQuery):
    filter_id, current_page = call.data.split('_')[-1].split('-')
    await db.set_wallet_history_show_participant(filter_id)
    await process_success_edit_history_records_number(call)


@dp.callback_query_handler(lambda call: 'get-wallet-last-transactions_' in call.data, state=User.main)
async def process_get_wallet_last_transactions(call: CallbackQuery, state: FSMContext):
    filter_id, current_page = call.data.split('_')[-1].split('-')

    history_filter = await db.get_wallet_history_filter_on_filter(filter_id)
    if history_filter:
        await call.answer(_('ask_wait_history'))
        name, wallet, records_number, show_participant = history_filter

        tr_type = tr_types[current_page]
        transactions = await tr_type[0](wallet, 100)
        await state.set_data({current_page: [transactions, wallet, show_participant, name, tr_type[1]]})
        transactions_repr = await utils.get_transactions_repr(wallet, transactions[:20], show_participant)

        await call.message.edit_text(
            _('get_transactions_history').format(
                name=name, wallet=wallet, tr_type=_(tr_type[1]), trs=transactions_repr
            ),
            reply_markup=markups.user.get_last_transactions_menu(filter_id, current_page, 1),
            disable_web_page_preview=True
        )
        return
    await call.answer(_('wallet_not_found_error'))
    await process_return_to_history(call)


@dp.callback_query_handler(lambda call: 'last-trs-to-page_' in call.data, state=User.main)
async def process_get_last_trs_page(call: CallbackQuery, state: FSMContext):
    filter_id, current_page, pointer = call.data.split('_')[-1].split('-')
    data = (await state.get_data()).get(current_page)
    if data:
        transactions, wallet, show_participant, name, tr_type = data
        pointer = int(pointer)
        transactions_repr = await utils.get_transactions_repr(wallet, transactions[20 * (pointer - 1):20 * pointer],
                                                              show_participant, 20 * (pointer - 1) + 1)
        await call.message.edit_text(
            _('get_transactions_history').format(name=name, wallet=wallet, tr_type=_(tr_type), trs=transactions_repr),
            reply_markup=markups.user.get_last_transactions_menu(filter_id, current_page, pointer),
            disable_web_page_preview=True
        )
        return
    await call.answer(_('transactions_data_not_found_error'))
    call.data = f'success-edit-history-filters_{filter_id}-{current_page}'
    await process_return_to_history(call)


@dp.callback_query_handler(lambda call: 'return-to-history_' in call.data, state=User.main)
async def process_return_to_history(call: CallbackQuery, state: FSMContext):
    filter_id, current_page = call.data.split('_')[-1].split('-')
    await state.finish()
    await User.main.set()
    history_filter = await db.get_wallet_history_filter_on_filter(filter_id)
    if history_filter:
        await call.answer(_('ask_wait_history'))
        name, wallet, records_number, show_participant = history_filter
        tr_type = tr_types[current_page]
        transactions = await tr_type[0](wallet, records_number)
        transactions_repr = await utils.get_transactions_repr(wallet, transactions, show_participant)
        await call.message.edit_text(
            _('get_transactions_history').format(
                name=name, wallet=wallet, tr_type=_(tr_type[1]), trs=transactions_repr
            ),
            reply_markup=markups.user.get_wallet_history_menu(filter_id, int(current_page)),
            disable_web_page_preview=True
        )
        return
    await call.answer(_('wallet_not_found_error'))
    await process_return_to_user_wallets(call)


@dp.callback_query_handler(lambda call: 'h-return-to-wallet-menu_' in call.data, state=User.main)
async def process_h_return_to_wallet_menu(call: CallbackQuery):
    filter_id = call.data.split('_')[-1]
    wallet_id = await db.get_wallet_id_on_history_filter(filter_id)
    call.data = f'get-user-wallet_{wallet_id}'
    await get_user_wallet(call)
