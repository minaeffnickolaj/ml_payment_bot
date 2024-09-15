import asyncio

from config.utils import read_config
from payment_server.server import PaymentServer

def main():
    # читаем конфиг
    (database_url, database_user, database_password, database_name, database_port, pyrogram_api_id,
     pyrogram_api_hash, pyrogram_bot_token, techwizapi_url, techwizapi_key, techwizapi_shop_id, payment_port) = read_config()
    # инициализируем сервер для коллбека от техвизапи
    server = PaymentServer(payment_port, techwizapi_key, techwizapi_shop_id)
    try:
        asyncio.run(server.run())
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
