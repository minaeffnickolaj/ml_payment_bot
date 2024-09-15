from tortoise import Tortoise, fields
from tortoise.models import Model

class Database:
    def __init__(self, url: str, user: str, password: str, name: str, port: int):
        self.name = name
        self.user = user
        self.password = password
        self.host = url
        self.port = port
        self.url = f'mysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'

    async def init(self):
        await Tortoise.init(
            db_url=self.url,
            modules={'models': ['database.payment', 'database.subscriber']}
        )
        await Tortoise.generate_schemas(safe=True)

    async def close(self):
        await Tortoise.close_connections()

    @staticmethod
    async def get_db():
        return await Tortoise.get_connection()

