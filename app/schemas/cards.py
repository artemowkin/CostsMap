from decimal import Decimal

from pydantic import BaseModel, Field

from .accounts import Currencies


class Card(BaseModel):
    """Card pydantic model"""

    title: str = Field(..., min_length=1, max_length=50)
    currency: Currencies
    color: str = Field(..., max_length=10)


class CardOut(Card):
    """Card pydantic model for output responses"""

    id: int
    amount: Decimal

    class Config:
        orm_mode = True


class Transfer(BaseModel):
    """Pydantic model for transfers between cards"""

    from_id: int
    to_id: int
    from_amount: int
    to_amount: int | None = None
