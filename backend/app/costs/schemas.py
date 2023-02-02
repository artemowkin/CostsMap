from uuid import UUID

from ..categories.schemas import CategoryWithoutCostsSum
from ..transactions.schemas import BaseTransactionIn, BaseTransactionOut


class CostIn(BaseTransactionIn):
    category_id: UUID


class CostOut(BaseTransactionOut):
    category: CategoryWithoutCostsSum

    class Config:
        orm_mode = True
