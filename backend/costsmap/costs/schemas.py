from decimal import Decimal
from datetime import date as dt_date

from pydantic import BaseModel, validator, Field

from ..cards.schemas import CardOut
from ..categories.schemas import CategoryOut
from ..utils import validate_amount_max_min


card_currency_amount_description = "required when card currency is differrent than default user currency"


class BaseCost(BaseModel):
    """Base pydantic model for cost with generic fields"""

    user_currency_amount: Decimal
    card_currency_amount: Decimal | None = Field(None, description=card_currency_amount_description)
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


class Cost(BaseCost):
    """Model for cost data getting from request"""

    category_id: int
    card_id: int


class CostOut(BaseCost):
    """Model for cost data returning in response"""

    id: int
    category: CategoryOut
    card: CardOut

    class Config:
        orm_mode = True


class TotalCosts(BaseModel):
    """Model for total costs response"""

    total_costs: Decimal
