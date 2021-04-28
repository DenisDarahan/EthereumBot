from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from botapp.middlewares import i18n


_ = i18n.gettext


def lang_choose():
    m = InlineKeyboardMarkup()
    m.row(InlineKeyboardButton('🇷🇺 Ru', callback_data='lang_ru'),
          InlineKeyboardButton('🇺🇸 En', callback_data='lang_en'))
    return m


def process_main_menu(lang=None):
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.row(KeyboardButton(_('add_wallet_button', locale=lang)))
    m.row(KeyboardButton(_('manage_wallets_button', locale=lang)))
    return m


def process_manage_wallets_menu(wallets):
    m = InlineKeyboardMarkup()
    for wallet_id, name in wallets:
        m.row(InlineKeyboardButton(name, callback_data=f'get-user-wallet_{wallet_id}'))
    return m


def get_wallet_menu(wallet_id):
    m = InlineKeyboardMarkup()
    m.row(InlineKeyboardButton(_('wallet_history_button'),
                               callback_data=f'get-user-wallet-history_{wallet_id}'),
          InlineKeyboardButton(_('wallet_notifications_button'),
                               callback_data=f'get-user-wallet-notifications_{wallet_id}'))
    m.row(InlineKeyboardButton(_('delete_wallet_button'), callback_data=f'ask-delete-user-wallet_{wallet_id}'))
    m.row(InlineKeyboardButton(_('back_button'), callback_data='return-to-user-wallets'))
    return m


def get_wallet_history_menu(filter_id, current_page=0):
    m = InlineKeyboardMarkup()
    transactions_buttons = [
        InlineKeyboardButton(_('get_norm_trs_button'),
                             callback_data=f'get-normal-transactions-history_{filter_id}'),
        InlineKeyboardButton(_('get_in_trs_button'),
                             callback_data=f'get-internal-transactions-history_{filter_id}'),
        InlineKeyboardButton(_('get_erc20_trs_button'),
                             callback_data=f'get-erc-20-transactions-history_{filter_id}'),
        InlineKeyboardButton(_('get_erc721_trs_button'),
                             callback_data=f'get-erc-721-transactions-history_{filter_id}')
    ]
    m.row(*transactions_buttons[:current_page] + transactions_buttons[current_page + 1:])
    m.row(InlineKeyboardButton(_('history_filters_button'),
                               callback_data=f'get-wallet-history-filters_{filter_id}-{current_page}'),
          InlineKeyboardButton(_('last_trs_button'),
                               callback_data=f'get-wallet-last-transactions_{filter_id}-{current_page}'))
    m.row(InlineKeyboardButton(_('back_button'), callback_data=f'h-return-to-wallet-menu_{filter_id}'))
    return m


def get_wallet_history_filters_menu(filter_id, current_page):
    m = InlineKeyboardMarkup()
    m.row(InlineKeyboardButton(_('history_records_number_button'),
                               callback_data=f'edit-history-records-number_{filter_id}-{current_page}'),
          InlineKeyboardButton(_('history_show_participant_button'),
                               callback_data=f'edit-history-show-participant_{filter_id}-{current_page}'))
    m.row(InlineKeyboardButton(_('back_button'), callback_data=f'return-to-history_{filter_id}-{current_page}'))
    return m


def edit_history_records_number_menu(filter_id, records_number, current_page):
    m = InlineKeyboardMarkup()
    m.row(InlineKeyboardButton('➖',
                               callback_data=f'set-history-records-number_'
                                             f'{filter_id}-{records_number - 1}-{current_page}'),
          InlineKeyboardButton(f'{records_number}', callback_data='ignore'),
          InlineKeyboardButton('➕',
                               callback_data=f'set-history-records-number_'
                                             f'{filter_id}-{records_number + 1}-{current_page}'))
    m.row(InlineKeyboardButton(_('done_button'),
                               callback_data=f'success-edit-history-filters_{filter_id}-{current_page}'))
    return m


def edit_history_show_participant_menu(filter_id, show_participant, current_page):
    m = InlineKeyboardMarkup()
    m.row(InlineKeyboardButton(_(f'{"not_" * show_participant}show_participant_button'),
                               callback_data=f'set-history-show-participant_{filter_id}-{current_page}'))
    m.row(InlineKeyboardButton(_('back_button'),
                               callback_data=f'success-edit-history-filters_{filter_id}-{current_page}'))
    return m


def get_last_transactions_menu(filter_id, current_page, pointer):
    m = InlineKeyboardMarkup()
    prev_pointer, next_pointer = pointer - 1, pointer + 1
    m.row(
        InlineKeyboardButton(f'{prev_pointer}',
                             callback_data=f'last-trs-to-page_{filter_id}-{current_page}-{prev_pointer}')
        if prev_pointer else InlineKeyboardButton('᠌', callback_data='ignore'),

        InlineKeyboardButton(f'·{pointer}·', callback_data='ignore'),

        InlineKeyboardButton(f'{next_pointer}',
                             callback_data=f'last-trs-to-page_{filter_id}-{current_page}-{next_pointer}')
        if next_pointer < 6 else InlineKeyboardButton('᠌', callback_data='ignore')
    )
    m.row(InlineKeyboardButton(_('back_button'), callback_data=f'return-to-history_{filter_id}-{current_page}'))
    return m


def get_wallet_notifications_menu(filter_id, off_sound, notify):
    m = InlineKeyboardMarkup()
    m.row(InlineKeyboardButton(_('notifications_filters'),
                               callback_data=f'get-wallet-notifications-filters_{filter_id}'))
    m.row(InlineKeyboardButton(_('off_notify_button') if notify else _('on_notify_button'),
                               callback_data=f'change-wallet-notifications_{filter_id}'))
    if notify:
        m.row(InlineKeyboardButton(_('on_sound_button') if off_sound else _('off_sound_button'),
                                   callback_data=f'change-wallet-off-sound_{filter_id}'))
    m.row(InlineKeyboardButton(_('back_button'), callback_data=f'n-return-to-wallet-menu_{filter_id}'))
    return m


def get_wallet_notifications_filters_menu(filter_id):
    m = InlineKeyboardMarkup()
    m.row(InlineKeyboardButton(_('change_nf_amount_button'),
                               callback_data=f'change-wallet-notifications-filter-amount_{filter_id}'),
          InlineKeyboardButton(_('change_nf_tr_type_button'),
                               callback_data=f'change-wallet-notifications-filter-tr-type_{filter_id}'))
    m.row(InlineKeyboardButton(_('back_button'), callback_data=f'return-to-wallet-notifications_{filter_id}'))
    return m


def get_notifications_filter_tr_type(filter_id, tr_type):
    m = InlineKeyboardMarkup()
    m.row(InlineKeyboardButton('✅ ' * (tr_type == 'in') + _('tr_type_in'),
                               callback_data=f'set-notifications-filter-tr-type_in-{filter_id}'),
          InlineKeyboardButton('✅ ' * (tr_type == 'out') + _('tr_type_out'),
                               callback_data=f'set-notifications-filter-tr-type_out-{filter_id}'),
          InlineKeyboardButton('✅ ' * (tr_type == 'inout') + _('tr_type_inout'),
                               callback_data=f'set-notifications-filter-tr-type_inout-{filter_id}'))
    m.row(InlineKeyboardButton(_('back_button'),
                               callback_data=f'get-wallet-notifications-filters_{filter_id}'))
    return m


def ask_delete_user_wallet_menu(wallet_id):
    m = InlineKeyboardMarkup()
    m.row(
        InlineKeyboardButton(_('accept_delete_button'), callback_data=f'accept-delete-user-wallet_{wallet_id}'),
        InlineKeyboardButton(_('decline_delete_button'), callback_data=f'decline-delete-user-wallet_{wallet_id}')
    )
    return m
