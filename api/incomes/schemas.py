from decimal import Decimal
from datetime import date as dt_date

from pydantic import BaseModel, validator

from cards.schemas import CardOut
from utils import validate_amount_max_min


class BaseIncome(BaseModel):
    """Base pydantic model for income with generic fields"""

    user_currency_amount: Decimal
    card_currency_amount: Decimal | None = None
    date: dt_date

    @validator('user_currency_amount')
    def validate_user_currency_amount_max_and_min_value(cls, v):
        validate_amount_max_min(v)
        return v

    @validator('card_currency_amount')
    def validate_card_currency_amount_max_and_min_value(cls, v):
        if v is None: return v

        validate_amount_max_min(v)
        return v


class Income(BaseIncome):
    """Model for income data getting from request"""

    card_id: int


class IncomeOut(BaseIncome):
    """Model for income data returning in response"""

    id: int
    card: CardOut

    class Config:
        orm_mode = True


class TotalIncomes(BaseModel):
    """Model for total incomes response"""

    total_incomes: Decimal
