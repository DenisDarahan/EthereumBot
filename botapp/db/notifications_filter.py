from .base import create_con


async def get_wallet_notifications_params(wallet_id):
    con, cur = await create_con()
    await cur.execute('select w.name, w.wallet, nf.filter_id, nf.min_amount, nf.tr_type, nf.off_sound, nf.notify '
                      'from notifications_filter nf join wallet w on nf.wallet_id = w.wallet_id '
                      'where nf.wallet_id = %s', (wallet_id, ))
    notifications_params = await cur.fetchone()
    await con.ensure_closed()
    return notifications_params


async def get_wallet_notifications_params_on_filter(filter_id):
    con, cur = await create_con()
    await cur.execute('select w.name, w.wallet, nf.min_amount, nf.tr_type, nf.off_sound, nf.notify '
                      'from notifications_filter nf join wallet w on nf.wallet_id = w.wallet_id '
                      'where nf.filter_id = %s', (filter_id, ))
    notifications_params = await cur.fetchone()
    await con.ensure_closed()
    return notifications_params


async def get_wallet_notifications_filters(filter_id):
    con, cur = await create_con()
    await cur.execute('select min_amount, tr_type from notifications_filter where filter_id = %s', (filter_id, ))
    filters = await cur.fetchone()
    await con.ensure_closed()
    return filters


async def set_notifications_filter_min_amount(filter_id, amount):
    con, cur = await create_con()
    await cur.execute('update notifications_filter set min_amount = %s where filter_id = %s', (amount, filter_id))
    await con.commit()
    await con.ensure_closed()


async def set_notifications_filter_tr_type(filter_id, tr_type):
    con, cur = await create_con()
    await cur.execute('update notifications_filter set tr_type = %s where filter_id = %s', (tr_type, filter_id))
    await con.commit()
    await con.ensure_closed()


async def get_wallet_notifications_alert_params(filter_id):
    con, cur = await create_con()
    await cur.execute('select off_sound, notify from notifications_filter where filter_id = %s', (filter_id, ))
    params = await cur.fetchone()
    await con.ensure_closed()
    return params


async def change_wallet_off_sound(filter_id):
    con, cur = await create_con()
    await cur.execute('update notifications_filter set off_sound = not off_sound where filter_id = %s', (filter_id, ))
    await con.commit()
    await con.ensure_closed()


async def change_wallet_notifications(filter_id):
    con, cur = await create_con()
    await cur.execute('update notifications_filter set notify = not notify where filter_id = %s', (filter_id, ))
    await con.commit()
    await con.ensure_closed()


async def get_wallet_id_on_notifications_filter(filter_id):
    con, cur = await create_con()
    await cur.execute('select wallet_id from notifications_filter where filter_id = %s', (filter_id, ))
    wallet_id = await cur.fetchone()
    await con.ensure_closed()
    return wallet_id[0] if wallet_id else 0
