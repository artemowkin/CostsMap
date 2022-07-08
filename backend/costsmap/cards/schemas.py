from typing import Literal
from decimal import Decimal

from pydantic import Field

from ..project.schemas import CamelModel
from ..accounts.schemas import Currencies


class Card(CamelModel):
    """Card pydantic model"""

    title: str = Field(..., min_length=1, max_length=50)
    currency: Currencies
    color: str = Field(..., max_length=10)


class CardOut(Card):
    """Card pydantic model for output responses"""

    id: int
    amount: Decimal = Decimal('0')

    class Config(Card.Config):
        orm_mode = True


class Transfer(CamelModel):
    """Pydantic model for transfers between cards"""

    from_id: int
    to_id: int
    from_amount: int
    to_amount: int | None = None


class UniqueCardTitleError(CamelModel):
    detail: Literal["Card with this title already exists"]


class Card404Error(CamelModel):
    detail: Literal["Card with this id doesn't exist"]
