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
        self.check_order_url = 'https://techwhizpay.ru/api/checkOrder'

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
        additional = data['additional']

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

    async def check_order_status(self, unique_id):
        """Проверяет статус заказа на стороне платежного сервиса."""
        payload = {
            'unique_id': unique_id
        }

        headers = {
            'Content-type': 'application/x-www-form-urlencoded'
        }

        async with ClientSession() as session:
            try:
                async with session.post(self.check_order_url, data=payload, headers=headers) as response:
                    if response.status == 200:
                        result = await response.json()
                        status = result.get('data', {}).get('status')
                        return status  # Вернем статус заказа
                    else:
                        print(f"Ошибка при запросе статуса заказа: {response.status}")
                        return None
            except Exception as e:
                print(f"Ошибка при выполнении запроса: {e}")
                return None

    async def monitor_payment(self, unique_id):
        """Запускает мониторинг статуса платежа на 60 минут."""
        check_intervals = [5, 10, 15, 30, 45, 60]  # Интервалы в минутах

        for interval in check_intervals:
            await asyncio.sleep(interval * 60)  # Ожидание в минутах
            status = await self.check_order_status(unique_id)

            if status == 1:
                print(f"Заказ {unique_id} был оплачен!")
                # Здесь можно добавить пользователя в канал или выполнить другие действия
                return True
            else:
                print(f"Заказ {unique_id} пока не оплачен. Статус: {status}")

        print(f"Заказ {unique_id} не был оплачен за 60 минут.")
        return False

    async def create_payment(self, unique_id, amount, description, user_id, additional):
        payload = {
            'token': self.api_key,
            'unique_id': unique_id,
            'amount': amount,
            'shop_id': self.shop_id,
            'description': description,
            'user_ip': '94.131.11.149',  # TODO: get user ip
            'user_id': user_id,
            'additional': additional
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
