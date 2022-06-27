from datetime import date

import orm

from project.models import models
from cards.models import Cards
from accounts.models import Users


class Incomes(orm.Model):
    tablename = 'incomes'
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "user_currency_amount": orm.Decimal(max_digits=9, decimal_places=2, minimum=0, allow_null=False),
        "card_currency_amount": orm.Decimal(max_digits=9, decimal_places=2, minimum=0, allow_null=False),
        "date": orm.Date(default=date.today()),
        "card": orm.ForeignKey(Cards, on_delete=orm.CASCADE),
        "user": orm.ForeignKey(Users, on_delete=orm.CASCADE)
    }
