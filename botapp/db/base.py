from aiomysql import connect, Connection, Cursor

from botapp.config import MYSQL


async def create_con():
    con: Connection = await connect(**MYSQL)
    cur: Cursor = await con.cursor()
    return con, cur
