from typing import NamedTuple
from decimal import Decimal
from datetime import date

import orm

from ..project.models import models
from ..cards.models import Cards, CardNamedTuple
from ..accounts.models import Users, UserNamedTuple


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


class IncomeNamedTuple(NamedTuple):
    id: int
    user_currency_amount: Decimal
    card_currency_amount: Decimal
    date: date
    card: CardNamedTuple
    user: UserNamedTuple
