from tortoise.models import Model
from tortoise import fields

class Subscriber(Model):
    id = fields.IntField(pk=True)
    telegram_id = fields.IntField()
    nickname = fields.CharField(max_length=64)
    first_name = fields.CharField(max_length=64)
    last_name = fields.CharField(max_length=64)
    first_subscribe_date = fields.DateField(auto_now=True)
    subscribe_valid_to_date = fields.DateField()
    payments = fields.ReverseRelation["Payment"]