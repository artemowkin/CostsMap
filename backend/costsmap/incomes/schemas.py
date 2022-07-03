from decimal import Decimal

from pydantic import BaseModel

from ..card_operations_generics.schemas import CardOperationIn, CardOperationOut


class IncomeIn(CardOperationIn):
    """Model for income data getting from request"""

    pass


class IncomeOut(CardOperationOut):
    """Model for income data returning in response"""

    pass


class TotalIncomes(BaseModel):
    """Model for total incomes response"""

    total_incomes: Decimal
