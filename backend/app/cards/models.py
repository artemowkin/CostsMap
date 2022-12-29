from uuid import uuid4
from decimal import Decimal

import ormar

from ..authentication.schemas import CurrenciesEnum
from ..authentication.models import User
from ..project.models import BaseMeta


class Card(ormar.Model):
    uuid: str = ormar.String(primary_key=True, max_length=36, default=lambda: str(uuid4())) # type: ignore
    title: str = ormar.String(max_length=50) # type: ignore
    currency: CurrenciesEnum = ormar.String(max_length=1, min_length=1) # type: ignore
    color: str = ormar.String(max_length=8) # type: ignore
    amount: Decimal = ormar.Decimal(max_digits=12, decimal_places=2, default=0) # type: ignore
    owner: User = ormar.ForeignKey(User, ondelete='CASCADE')

    class Meta(BaseMeta):
        constraints = [ormar.UniqueColumns('title', 'owner')]
