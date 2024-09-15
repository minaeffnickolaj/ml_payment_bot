from aiohttp import web
import asyncio

class PaymentServer:
    def __init__(self, port):
        self.server_port = port
        self.app = web.Application()

    async def success_payment_handler(self, request):
        data = await request.json()

    async def init_app(self):
        self.app.router.add_get('/success_payment', self.success_payment_handler)
        return self.app

    async def run(self):
        await self.init_app()
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, '127.0.0.1', self.server_port)
        await site.start()

        while True:
            await asyncio.sleep(3600)
