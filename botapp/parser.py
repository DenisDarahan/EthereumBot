import asyncio
import json
# from time import time

from aiomysql import Cursor
from aio_pika import connect, Message, IncomingMessage
from aiogram import exceptions
from web3 import Web3

from botapp.misc import bot
from botapp.middlewares import i18n, get_lang
from botapp import db, utils


LAST_BLOCK = 0
_ = i18n.gettext


async def get_users_to_notify(cur: Cursor, wallet: str, amount: float, tr_type: str) -> tuple:
    await cur.execute('select w.user_id, w.name, nf.off_sound '
                      'from wallet w join notifications_filter nf on w.wallet_id = nf.wallet_id '
                      'where w.wallet = %s and nf.notify = 1 and nf.min_amount <= %s and nf.tr_type <> %s',
                      (wallet, amount, tr_type))
    users = await cur.fetchall()
    return users


async def process_parse_transactions(transactions):
    con, cur = await db.create_con()

    for tr in transactions:
        value = float(Web3.fromWei(int(tr['value'], 16), 'ether'))

        for user in await get_users_to_notify(cur, tr['from'], value, 'in'):
            user_id, name, off_sound = user
            try:
                await bot.send_message(user_id,
                                       _('withdraw_message', locale=(await get_lang(user_id))).format(
                                           tr['from'], name, tr['hash'], str(value).rstrip('0').rstrip('.'), tr['to']
                                       ),
                                       disable_web_page_preview=True,
                                       disable_notification=off_sound)
            except exceptions.BotBlocked:
                pass

        for user in await get_users_to_notify(cur, tr['to'], value, 'out'):
            user_id, name, off_sound = user
            try:
                await bot.send_message(user_id,
                                       _('replenishment_message', locale=(await get_lang(user_id))).format(
                                           tr['to'], name, tr['hash'], str(value).rstrip('0').rstrip('.'), tr['from']
                                       ),
                                       disable_web_page_preview=True,
                                       disable_notification=off_sound)
            except exceptions.BotBlocked:
                pass

    await con.ensure_closed()


async def get_internal_transactions(block_number, tr_number):
    transactions = await utils.get_block_internal_transactions(block_number, tr_number)
    for in_tr in transactions:
        in_tr['value'] = hex(int(in_tr['value']))
    return transactions


def grab_transactions(channel, queue):
    async def on_message(message: IncomingMessage):
        global LAST_BLOCK

        # Get block hash from queue
        block_hash = json.loads(message.body.decode())

        # Buffer time needed to wait until the block will be registered on the network
        await asyncio.sleep(60)

        # Avoid parsing same blocks
        if block_hash['number'] <= LAST_BLOCK:
            return

        # Perform request
        response = await utils.get_block_transactions(block_hash['hash'])

        # Get result from received block
        result = response.get('result')

        # Put block back to the queue if it's not registered yet
        if not result:
            await channel.default_exchange.publish(
                Message(json.dumps(block_hash).encode()),
                routing_key=queue.name
            )
            return

        # Parse received transactions
        transactions = result.get('transactions', [])

        # Add internal transactions
        if transactions:
            internal_transactions = await get_internal_transactions(block_hash['number'], len(transactions))
            transactions.extend(internal_transactions)

        # print(transactions)

        # Process transactions
        await process_parse_transactions(transactions)

        LAST_BLOCK = block_hash['number']
    return on_message


async def main():
    # RabbitMQ connection
    connection = await connect("amqp://guest:guest@localhost/", loop=loop)
    # Creating a channel
    channel = await connection.channel()
    # Declaring queue
    queue = await channel.declare_queue('block_hash_queue')
    # Start listening the queue
    await queue.consume(grab_transactions(channel, queue), no_ack=True)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
