from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ChatType
from web3 import Web3

from botapp.misc import bot, dp
from botapp.states import User
from botapp.middlewares import i18n
from botapp import db, markups


_ = i18n.gettext


@dp.message_handler(ChatType.is_private, lambda message: message.text == _('add_wallet_button'), state=User.main)
async def process_register_wallet(message: Message):
    await User.GetWallet.wallet.set()
    await bot.send_message(message.chat.id,
                           _('ask_get_wallet_number'),
                           reply_markup=markups.base.cancel_menu())


@dp.message_handler(ChatType.is_private, lambda message: message.text == _('cancel_button'), state=User.GetWallet)
async def cancel_register_wallet(message: Message, state: FSMContext):
    await state.finish()
    await User.main.set()
    await bot.send_message(message.chat.id,
                           _('cancel_get_wallet'),
                           reply_markup=markups.user.process_main_menu())


@dp.message_handler(ChatType.is_private, lambda message: message.text, state=User.GetWallet.wallet)
async def process_get_wallet_number(message: Message, state: FSMContext):
    if Web3.isAddress(message.text):
        await User.GetWallet.name.set()
        await state.set_data({'wallet': message.text})
        await bot.send_message(message.chat.id,
                               _('ask_get_wallet_name'),
                               reply_markup=markups.base.cancel_or_skip_menu())
        return
    await bot.send_message(message.chat.id, _('wallet_number_not_valid_error'))


@dp.message_handler(ChatType.is_private, lambda message: message.text == _('skip_button'),
                    state=User.GetWallet.name)
async def skip_get_wallet_name(message: Message, state: FSMContext):
    wallet = (await state.get_data()).get('wallet')
    if wallet:
        message.text = f'{wallet[:7]}...{wallet[-3:]}'
    await get_wallet_name(message, state)


@dp.message_handler(ChatType.is_private, lambda message: message.text, state=User.GetWallet.name)
async def get_wallet_name(message: Message, state: FSMContext):
    wallet = (await state.get_data()).get('wallet')
    await state.finish()
    await User.main.set()
    if wallet:
        await db.add_wallet(message.chat.id, wallet, message.text)
        await bot.send_message(message.chat.id,
                               _('success_register_wallet'),
                               reply_markup=markups.user.process_main_menu())
        return
    await bot.send_message(message.chat.id,
                           _('wallet_number_not_found_error'),
                           reply_markup=markups.user.process_main_menu())
