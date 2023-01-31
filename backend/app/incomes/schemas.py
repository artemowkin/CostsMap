import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from ..cards.schemas import CardOut


class BaseIncome(BaseModel):
    amount: Decimal = Field(..., gt=0)
    date: datetime.date


class IncomeIn(BaseIncome):
    card_id: UUID


class IncomeOut(BaseIncome):
    uuid: UUID
    card: CardOut

    class Config:
        orm_mode = True