import hashlib

from aiohttp import web, ClientSession
import asyncio


class PaymentServer:
    def __init__(self, port, techwizapi_key, techwizapi_shop_id):
        self.server_port = port
        self.api_key = techwizapi_key
        self.shop_id = techwizapi_shop_id
        self.app = web.Application()
        self.create_order = "https://techwhizpay.ru/api/createOrder"

    async def success_payment_handler(self, request):
        data = await request.json()

        id = data['id']
        unique_id = data['unique_id']
        sign = data['sign']
        amount = data['amount']
        status = data['status']
        created_at = data['created_at']
        paid_at = data['paid_at']
        email = data['email']
        description = data['description']
        additional_info = data['additional_info']

        my_sign = f"{unique_id}:{amount}:{self.api_key}:{self.shop_id}"
        verif_sign = hashlib.sha256(my_sign.encode()).hexdigest();

        if verif_sign == sign:
            return web.json_response({
                'status': 'OK'
            })
        else:
            return web.json_response({
                'status': 'Sign are corrupted!'
            })

    async def create_payment(self, unique_id, amount, description, user_id):
        payload = {
            'token': self.api_key,
            'unique_id': unique_id,
            'amount': amount,
            'shop_id': self.shop_id,
            'description': description,
            'user_ip': '94.131.11.149',  # TODO: get user ip
            'user_id': user_id
        }

        async with ClientSession() as session:
            try:
                async with session.post(self.create_order, json=payload) as response:
                    response_data = await response.json()
                    return response_data
            except Exception as e:
                return {'error': str(e)}

    async def get_payment_handler(self, request):
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
