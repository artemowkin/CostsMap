from datetime import date

import orm

from ..project.models import models
from ..accounts.models import Users
from ..categories.models import Categories, CategoryNamedTuple
from ..cards.models import Cards
from ..card_operations_generics.models import CardOperationNamedTuple


class Costs(orm.Model):
    tablename = 'costs'
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "user_currency_amount": orm.Decimal(max_digits=9, decimal_places=2, minimum=0, allow_null=False),
        "card_currency_amount": orm.Decimal(max_digits=9, decimal_places=2, minimum=0, allow_null=True),
        "date": orm.Date(default=date.today),
        "category": orm.ForeignKey(Categories, on_delete=orm.CASCADE),
        "card": orm.ForeignKey(Cards, on_delete=orm.CASCADE),
        "user": orm.ForeignKey(Users, on_delete=orm.CASCADE),
    }


class CostNamedTuple(CardOperationNamedTuple):
    category: CategoryNamedTuple
