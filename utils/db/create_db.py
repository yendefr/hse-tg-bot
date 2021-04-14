import asyncio
import asyncpg
import logging
from data.config import PG_HOST, PG_DB, PG_USER, PG_PASSWORD

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)

async def create_db():
    create_db_command = open("create.sql", "r").read()

    logging.info("Подключение к базе...")
    conn: asyncpg.Connection = await asyncpg.connect(user=PG_USER,
                                                     password=PG_PASSWORD,
                                                     host=PG_HOST,
                                                     database=PG_DB,
                                                    )
    await conn.execute(create_db_command)
    await conn.close()
    logging.info("Таблицы созданы")

async def create_pool():
    return await asyncpg.create_pool(user=PG_USER,
                                     password=PG_PASSWORD,
                                     host=PG_HOST,
                                     database=PG_DB,
                                    )


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_db())