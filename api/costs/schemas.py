from typing import Mapping, Literal, Any
from decimal import Decimal
from datetime import date as dt_date

from pydantic import BaseModel, validator

from cards.schemas import CardOut
from categories.schemas import CategoryOut
from utils import validate_amount_max_min


class BaseCost(BaseModel):
    """Base pydantic model for cost with generic fields"""

    amount: Decimal
    date: dt_date

    @validator('amount')
    def validate_amount_max_and_min_value(cls, v):
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
