from typing import Literal
from decimal import Decimal

from ..project.schemas import CamelModel
from ..card_operations_generics.schemas import CardOperationIn, CardOperationOut


class IncomeIn(CardOperationIn):
    """Model for income data getting from request"""

    pass


class IncomeOut(CardOperationOut):
    """Model for income data returning in response"""

    pass


class TotalIncomes(CamelModel):
    """Model for total incomes response"""

    total_incomes: Decimal


class CreateIncome400Error(CamelModel):
    detail: Literal["Income for card with differrent currency than default must contain `card_currency_amount` field"]


class Income404Error(CamelModel):
    detail: Literal["Income with this id doesn't exist"]
