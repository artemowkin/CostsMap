from uuid import uuid4
from datetime import date, datetime
from decimal import Decimal

import ormar

from ..authentication.models import User
from ..categories.models import Category
from ..cards.models import Card
from ..project.models import BaseMeta


class Cost(ormar.Model):
    uuid: str = ormar.String(primary_key=True, max_length=36, default=lambda: str(uuid4())) # type: ignore
    amount: Decimal = ormar.Decimal(minimum=0.01, max_digits=12, decimal_places=2) # type: ignore
    date: date = ormar.Date() # type: ignore
    category: Category = ormar.ForeignKey(Category, ondelete='CASCADE', skip_reverse=False)
    card: Card = ormar.ForeignKey(Card, ondelete='CASCADE')
    owner: User = ormar.ForeignKey(User, ondelete='CASCADE')
    pub_datetime: datetime = ormar.DateTime(default=datetime.now) # type: ignore

    class Meta(BaseMeta): ...
