from typing import Mapping, Literal, Any
from decimal import Decimal

from pydantic import BaseModel, Field


CategoryOutMapping = Mapping[
    Literal['id'] | Literal['title'] | Literal['costs_limit'] | Literal['color'] | Literal['user_id'],
    Any
]


class BaseCategory(BaseModel):
    """Base model for category"""
    title: str = Field(..., max_length=50)
    costs_limit: int | None = Field(None, gt=0, lt=1000000)
    color: str = Field(..., max_length=10)


class CategoryOut(BaseCategory):
    """Model for category in response"""
    id: int
    costs_sum: Decimal | None = Decimal('0.0')

    class Config:
        orm_mode = True
