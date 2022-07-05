from typing import Literal
from decimal import Decimal

from pydantic import BaseModel

from ..categories.schemas import CategoryOut
from ..card_operations_generics.schemas import CardOperationIn, CardOperationOut


class CostIn(CardOperationIn):
    """Model for cost data getting from request"""

    category_id: int


class CostOut(CardOperationOut):
    """Model for cost data returning in response"""

    category: CategoryOut


class TotalCosts(BaseModel):
    """Model for total costs response"""

    total_costs: Decimal


class CreateCost400Error(BaseModel):
    detail: Literal[
        "Cost amount is more than card amount",
        "Cost for card with differrent currency than default must contain `card_currency_amount` field"
    ]


class Cost404Error(BaseModel):
    detail: Literal["Cost with this id doesn't exist"]
