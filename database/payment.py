from tortoise.models import Model
from tortoise import fields

class Payment(Model):
    id = fields.IntField(pk=True)
    amount = fields.DecimalField(max_digits=10, decimal_places=2)
    date = fields.DatetimeField(auto_now_add=True)
    subscriber = fields.ForeignKeyField("models.Subscriber", related_name="payments", on_delete=fields.CASCADE)