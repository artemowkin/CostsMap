from decimal import Decimal
from datetime import date
from typing import NamedTuple

from ..accounts.models import UserNamedTuple
from ..cards.models import CardNamedTuple


class CardOperationNamedTuple(NamedTuple):
    id: int
    user_currency_amount: Decimal
    card_currency_amount: Decimal
    date: date
    user: UserNamedTuple
    card: CardNamedTuple
