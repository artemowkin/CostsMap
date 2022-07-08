from typing import Literal
from decimal import Decimal

from pydantic import Field

from ..project.schemas import CamelModel


class BaseCategory(CamelModel):
    """Base model for category"""
    title: str = Field(..., max_length=50)
    costs_limit: int | None = Field(None, gt=0, lt=1000000)
    color: str = Field(..., max_length=10)


class CategoryOut(BaseCategory):
    """Model for category in response"""
    id: int
    costs_sum: Decimal | None = Decimal('0.0')

    class Config(BaseCategory.Config):
        orm_mode = True


class CategoryUniqueTitleError(CamelModel):
    detail: Literal["Category with this title already exists"]


class Category404Error(CamelModel):
    detail: Literal["Category with this id doesn't exist"]
