from typing import Literal
from decimal import Decimal

from pydantic import BaseModel, Field


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


class CategoryUniqueTitleError(BaseModel):
    detail: Literal["Category with this title already exists"]


class Category404Error(BaseModel):
    detail: Literal["Category with this id doesn't exist"]
