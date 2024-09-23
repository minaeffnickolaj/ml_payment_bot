import asyncio
from bot.bot import Bot  # Убедитесь, что вы импортируете правильный модуль
from payment_server.server import PaymentServer  # Убедитесь, что вы импортируете правильный модуль
from database.models import Database  # Убедитесь, что вы импортируете правильный модуль
from config.utils import read_config

async def main():
    # читаем конфиг
    (database_url, database_user, database_password, database_name, database_port, pyrogram_api_id,
     pyrogram_api_hash, pyrogram_bot_token, techwizapi_key, techwizapi_shop_id, payment_port) = read_config()

    # инициализируем сервер для коллбека от техвизапи
    server = PaymentServer(payment_port, techwizapi_key, techwizapi_shop_id)

    # инициализируем базу данных
    database = Database(database_url, database_user, database_password, database_name, database_port)

    # инициализируем бота
    bot = Bot(pyrogram_api_id, pyrogram_api_hash, pyrogram_bot_token, server)

    # Инициализация базы данных
    await database.init()

    try:
        # Запуск сервера и бота параллельно
        await asyncio.gather(
            server.run(),
            bot.run(),
        )
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        # Закрытие соединения с базой данных
        await database.close()

if __name__ == '__main__':
    # Запуск основного асинхронного цикла событий
    asyncio.run(main())
