import asyncio
import asyncpg
import logging
from data.config import PG_HOST, PG_USER, PG_PASSWORD
# PG_HOST, PG_USER, PG_PASSWORD = '192.168.99.100', 'postgres', 'yen1234'

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)

async def create_db():
    command = open('utils/db/create.sql', 'r').read()

    conn: asyncpg.Connection = await asyncpg.connect(
                                                    user=PG_USER,
                                                    host=PG_HOST,
                                                    )
    await conn.execute(command)
    await conn.close()
    logging.info("Table users created")

async def create_pool():
    return await asyncpg.create_pool(
                                    user=PG_USER,
                                    host=PG_HOST,
                                    )


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_db())