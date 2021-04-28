from .base import create_con


async def is_user(user_id):
    con, cur = await create_con()
    await cur.execute('select user_id from user where user_id = %s', (user_id,))
    user_id = await cur.fetchone()
    await con.ensure_closed()
    return user_id


async def create_user(user_id, lang):
    con, cur = await create_con()
    await cur.execute('insert into user (user_id, lang) values (%s, %s)', (user_id, lang))
    await con.commit()
    await con.ensure_closed()


async def get_lang(user_id):
    con, cur = await create_con()
    await cur.execute('select lang from user where user_id = %s', (user_id,))
    lang = await cur.fetchone()
    await con.ensure_closed()
    return lang[0] if lang else 'ru'
