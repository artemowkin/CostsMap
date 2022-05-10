from decimal import Decimal
from datetime import date as dt_date

from pydantic import BaseModel, validator

from .categories import CategoryOut


class BaseCost(BaseModel):
    """Base pydantic model for cost with generic fields"""

    amount: Decimal
    date: dt_date

    @validator('amount')
    def validate_amount_max_and_min_value(cls, v):
        if v < Decimal('0.01') or v > Decimal('9999999.99'):
            raise ValueError(
                "Amount must be more than 0 and less than 10000000"
            )

        return v


class Cost(BaseCost):
    """Model for cost data getting from request"""

    category_id: int


class CostOut(BaseCost):
    """Model for cost data returning in response"""

    category: CategoryOut

    class Config:
        orm_mode = True
