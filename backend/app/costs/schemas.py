import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from ..cards.schemas import CardOut
from ..categories.schemas import CategoryWithoutCostsSum


class BaseCost(BaseModel):
    amount: Decimal = Field(..., gt=0.01)
    date: datetime.date


class CostIn(BaseCost):
    category_id: UUID
    card_id: UUID


class CostOut(BaseCost):
    uuid: UUID
    card: CardOut
    category: CategoryWithoutCostsSum

    class Config:
        orm_mode = True
