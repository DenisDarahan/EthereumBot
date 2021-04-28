from .base import create_con


async def add_wallet(user_id, wallet, name):
    con, cur = await create_con()
    await cur.execute('insert into wallet (user_id, wallet, name) values (%s, %s, %s) '
                      'on duplicate key update name = values(name), reg_date = now()', (user_id, wallet, name))
    await con.commit()
    wallet_id = cur.lastrowid
    await cur.execute('insert ignore into notifications_filter (wallet_id) values (%s)', (wallet_id, ))
    await cur.execute('insert ignore into history_filter (wallet_id) values (%s)', (wallet_id, ))
    await con.commit()
    await con.ensure_closed()


async def get_user_wallets(user_id):
    con, cur = await create_con()
    await cur.execute('select wallet_id, name from wallet where user_id = %s', (user_id, ))
    wallets = await cur.fetchall()
    await con.ensure_closed()
    return wallets


async def get_user_wallet(wallet_id):
    con, cur = await create_con()
    await cur.execute('select wallet, name from wallet where wallet_id = %s', (wallet_id, ))
    wallet = await cur.fetchone()
    await con.ensure_closed()
    return wallet if wallet else None


async def delete_user_wallet(wallet_id):
    con, cur = await create_con()
    await cur.execute('delete from wallet where wallet_id = %s', (wallet_id, ))
    await con.commit()
    await con.ensure_closed()
