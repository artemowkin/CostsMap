import datetime
from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel, Field

from ..cards.schemas import CardOut


class BaseTransaction(BaseModel):
    amount: Decimal = Field(..., gt=0.01)
    date: datetime.date


class BaseTransactionIn(BaseTransaction):
    card_id: UUID


class BaseTransactionOut(BaseTransaction):
    uuid: UUID
    card: CardOut

    class Config:
        orm_mode = True