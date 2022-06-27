from datetime import date

import orm

from project.models import models
from accounts.models import Users
from categories.models import Categories
from cards.models import Cards


class Costs(orm.Model):
    tablename = 'costs'
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "amount": orm.Decimal(max_digits=9, decimal_places=2, minimum=0),
        "date": orm.Date(default=date.today()),
        "category": orm.ForeignKey(Categories, on_delete=orm.CASCADE),
        "card": orm.ForeignKey(Cards, on_delete=orm.CASCADE),
        "user": orm.ForeignKey(Users, on_delete=orm.CASCADE),
    }
