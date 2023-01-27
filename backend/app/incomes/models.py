from uuid import uuid4
from datetime import date as date_, datetime
from decimal import Decimal

import ormar

from ..authentication.models import User
from ..cards.models import Card
from ..project.models import BaseMeta


class Income(ormar.Model):
    uuid: str = ormar.String(primary_key=True, max_length=36, default=lambda: str(uuid4()))
    amount: Decimal = ormar.Decimal(minimum=0.01, max_digits=12, decimal_places=2)
    date: date_ = ormar.Date()
    card: Card = ormar.ForeignKey(Card, ondelete='CASCADE')
    owner: User = ormar.ForeignKey(User, ondelete='CASCADE')
    pub_datetime: datetime = ormar.DateTime(default=datetime.now)

    class Meta(BaseMeta): ...