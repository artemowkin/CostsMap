from decimal import Decimal
from typing import NamedTuple

import orm

from ..project.models import models
from ..accounts.models import Users, UserNamedTuple
from ..accounts.schemas import Currencies


class Cards(orm.Model):
    tablename = 'cards'
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "title": orm.String(max_length=50, unique=True, allow_blank=False, allow_null=False),
        "currency": orm.String(max_length=1, min_length=1),
        "color": orm.String(max_length=10, allow_blank=False, allow_null=False),
        "amount": orm.Decimal(max_digits=9, decimal_places=2, default=0),
        "user": orm.ForeignKey(Users, on_delete=orm.CASCADE),
    }


class CardNamedTuple(NamedTuple):
    id: int
    title: str
    currency: Currencies
    color: str
    amount: Decimal
    user: UserNamedTuple
