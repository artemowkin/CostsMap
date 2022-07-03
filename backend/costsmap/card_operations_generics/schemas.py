from decimal import Decimal
from datetime import date as dt_date

from pydantic import BaseModel, Field, validator

from ..utils import validate_amount_max_min
from ..cards.schemas import CardOut


card_currency_amount_description = "required when card currency is differrent than default user currency"


class CardOperation(BaseModel):
    """Generic schema for card operations"""

    user_currency_amount: Decimal
    card_currency_amount: Decimal | None = Field(None, description=card_currency_amount_description)
    date: dt_date = dt_date.today()

    @validator('user_currency_amount')
    def validate_user_currency_amount_max_and_min_value(cls, v):
        validate_amount_max_min(v)
        return v

    @validator('card_currency_amount')
    def validate_card_currency_amount_max_and_min_value(cls, v):
        if v is None: return v
        validate_amount_max_min(v)
        return v


class CardOperationIn(CardOperation):
    """Generic schema for card operations in request data"""

    card_id: int


class CardOperationOut(CardOperation):
    """Generic schema for card operations in response data"""

    id: int
    card: CardOut

    class Config:
        orm_mode = True
