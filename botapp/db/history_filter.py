from .base import create_con


async def get_wallet_history_filter(wallet_id):
    con, cur = await create_con()
    await cur.execute('select w.name, w.wallet, hf.filter_id, hf.records_number, hf.show_participant '
                      'from history_filter hf join wallet w on hf.wallet_id = w.wallet_id '
                      'where hf.wallet_id = %s', (wallet_id, ))
    history_filter = await cur.fetchone()
    await con.ensure_closed()
    return history_filter


async def get_wallet_history_filter_on_filter(filter_id):
    con, cur = await create_con()
    await cur.execute('select w.name, w.wallet, hf.records_number, hf.show_participant '
                      'from history_filter hf join wallet w on hf.wallet_id = w.wallet_id '
                      'where hf.filter_id = %s', (filter_id, ))
    history_filter = await cur.fetchone()
    await con.ensure_closed()
    return history_filter


async def get_wallet_history_records_number(filter_id):
    con, cur = await create_con()
    await cur.execute('select records_number from history_filter where filter_id = %s', (filter_id, ))
    records_number = await cur.fetchone()
    await con.ensure_closed()
    return records_number


async def set_wallet_history_records_number(filter_id, records_number):
    con, cur = await create_con()
    await cur.execute('update history_filter set records_number = %s where filter_id = %s',
                      (records_number, filter_id))
    await con.commit()
    await con.ensure_closed()


async def get_wallet_history_show_participant(filter_id):
    con, cur = await create_con()
    await cur.execute('select show_participant from history_filter where filter_id = %s', (filter_id, ))
    show_participant = await cur.fetchone()
    await con.ensure_closed()
    return show_participant


async def set_wallet_history_show_participant(filter_id):
    con, cur = await create_con()
    await cur.execute('update history_filter set show_participant = not show_participant where filter_id = %s',
                      (filter_id, ))
    await con.commit()
    await con.ensure_closed()


async def get_wallet_id_on_history_filter(filter_id):
    con, cur = await create_con()
    await cur.execute('select wallet_id from history_filter where filter_id = %s', (filter_id,))
    wallet_id = await cur.fetchone()
    await con.ensure_closed()
    return wallet_id[0] if wallet_id else 0
