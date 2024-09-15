import asyncio

from config.utils import read_config
from database.subscriber import Subscriber
from payment_server.server import PaymentServer
from database import subscriber, payment
from database.models import Database


async def main():
    # читаем конфиг
    (database_url, database_user, database_password, database_name, database_port, pyrogram_api_id,
     pyrogram_api_hash, pyrogram_bot_token, techwizapi_url, techwizapi_key, techwizapi_shop_id, payment_port) = read_config()
    # инициализируем сервер для коллбека от техвизапи
    server = PaymentServer(payment_port, techwizapi_key, techwizapi_shop_id)
    # инициализируем базу данных
    database = Database(database_url, database_user, database_password, database_name, database_port)

    await database.init()

    try:
        loop = asyncio.get_running_loop()
        await asyncio.gather(
            server.run(),
        )
    except Exception as e:
        print(e)
    finally:
        await database.close()

if __name__ == '__main__':
     asyncio.run(main())
