from aiogram.types import CallbackQuery, Update
from aiogram import exceptions

from botapp.misc import dp


async def handle_error(update: Update, error_name: str, error_args: str):
    if update.message:
        print(f'[!] Handled {error_name} from {update.message.chat.id}: {error_args}')
    elif update.callback_query:
        print(f'[!] Handled {error_name} from {update.callback_query.message.chat.id}: {error_args}')
    return True


@dp.errors_handler(exception=IndexError)
async def handle_index_error(update: Update, error: IndexError):
    return await handle_error(update, 'IndexError', str(error.args))


@dp.errors_handler(exception=TypeError)
async def handle_type_error(update: Update, error: TypeError):
    return await handle_error(update, 'TypeError', str(error.args))


@dp.errors_handler(exception=exceptions.InvalidQueryID)
async def handle_invalid_query_id_error(update: Update, error: exceptions.InvalidQueryID):
    return await handle_error(update, 'InvalidQueryID', str(error.args))


@dp.errors_handler(exception=exceptions.MessageToDeleteNotFound)
async def handle_message_to_delete_not_found_error(update: Update, error: exceptions.MessageToDeleteNotFound):
    return await handle_error(update, 'MessageToDeleteNotFound', str(error.args))


@dp.errors_handler(exception=exceptions.MessageCantBeDeleted)
async def handle_message_cant_be_deleted_error(update: Update, error: exceptions.MessageCantBeDeleted):
    return await handle_error(update, 'MessageCantBeDeleted', str(error.args))


@dp.errors_handler(exception=exceptions.MessageNotModified)
async def handle_message_not_modified_error(update: Update, error: exceptions.MessageNotModified):
    return await handle_error(update, 'MessageNotModified', str(error.args))


@dp.callback_query_handler(text='ignore', state='*')
async def process_ignore_callback(call: CallbackQuery):
    await call.answer()
