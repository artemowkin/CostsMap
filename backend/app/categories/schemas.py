from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel, Field


class CategoryIn(BaseModel):
    title: str
    costs_limit: Decimal
    color: str = Field(..., regex=r"#[a-fA-F0-9]{6}")


class CategoryWithoutCostsSum(CategoryIn):
    uuid: UUID

    class Config:
        orm_mode = True


class CategoryOut(CategoryIn):
    uuid: UUID
    costs_sum: int = 0

    class Config:
        orm_mode = True
