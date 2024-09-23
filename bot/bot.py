import datetime
import uuid
from pyrogram import Client, filters
from payment_server.server import *
from database.models import *
from database.subscriber import Subscriber
from database.payment import Payment
from pyrogram import utils


def get_peer_type_new(peer_id: int) -> str:
    peer_id_str = str(peer_id)
    if not peer_id_str.startswith("-"):
        return "user"
    elif peer_id_str.startswith("-100"):
        return "channel"
    else:
        return "chat"


utils.get_peer_type = get_peer_type_new


class Bot:
    def __init__(self, api_id, api_hash, bot_token, payment_server):
        self.api_id = api_id
        self.api_hash = api_hash
        self.bot_token = bot_token
        self.client = Client("ml_bot", api_id=self.api_id, api_hash=self.api_hash, bot_token=self.bot_token)
        self.setup_handlers()
        self.payment_server = payment_server

    def setup_handlers(self):
        @self.client.on_message(filters.command("start"))
        async def handle_message(client, message):
            await message.reply_text(f"Привет, {message.from_user.first_name}! \n" +
                                     "Нажми /pay чтобы оплатить доступ к нашему привату. \n" +
                                     "Ссылка действительна в течение 15 минут")

        @self.client.on_message(filters.command("pay"))
        async def handle_pay_message(client, message):
            try:
                unique_id = str(uuid.uuid4())
                amount = '30.00'
                description = 'Melnitsa Pass'
                user_id = await self.get_bot_id()
                additional = message.from_user.id

                response = await self.payment_server.create_payment(unique_id, amount, description, user_id, additional)
                if response.get('data', {}).get('error') == 0:
                    payment_link = response.get('data', {}).get('link', 'Нет ссылки на оплату')
                    await message.reply(f"Ссылка на оплату: {payment_link}")

                    # Запускаем отслеживание платежа
                    is_subscribe_paid = await self.payment_server.monitor_payment(unique_id)

                    if is_subscribe_paid:
                        subscriber, created = await Subscriber.get_or_create(
                            telegram_id=message.from_user.id,
                            defaults={
                                'nickname': message.from_user.username,
                                'first_subscribe_date': (datetime.datetime.now()).date(),
                                'subscribe_valid_to_date': (
                                            datetime.datetime.now() + datetime.timedelta(days=30)).date()
                            }
                        )

                        await Payment.create(
                            amount=amount,
                            subscriber=subscriber,
                        )

                        await message.reply(f"Платеж по заказу {unique_id} был получен.")

                        channel_id = int(-1002316341502)

                        invite_link = await self.client.create_chat_invite_link(
                            channel_id,
                            member_limit=1
                        )

                        await message.reply(f"Доступ к привату: {invite_link.invite_link}")

                    else:
                        await message.reply(
                            f"Платеж по заказу {unique_id} не был получен в течении часа - ссылка на оплату недействительна.")

                else:
                    error_message = response.get('data', {}).get('error_message', 'Неизвестная ошибка')
                    await message.reply(f"Ошибка: {error_message}")

            except Exception as e:
                print(e)
                await message.reply_text('Ошибка при создании платежа')

    async def run(self):
        await self.client.start()
        await self.client.get_me()

    async def get_bot_id(self):
        try:
            # Получаем информацию о боте
            me = await self.client.get_me()
            # Извлекаем ID
            bot_id = me.id
            return bot_id
        except Exception as e:
            print(f"Ошибка при получении информации о боте: {e}")
            return None
