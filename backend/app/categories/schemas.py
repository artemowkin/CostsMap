from decimal import Decimal

from pydantic import BaseModel, Field

from .models import Category


CategoryIn = Category.get_pydantic(exclude={'owner', 'uuid'})

BaseCategoryOut = Category.get_pydantic(exclude={'owner'})


class CategoryIn(BaseModel):
    title: str
    costs_limit: Decimal
    color: str = Field(..., regex=r"#[a-fA-F0-9]{6}")


class CategoryOut(BaseCategoryOut):
    costs_sum: int
