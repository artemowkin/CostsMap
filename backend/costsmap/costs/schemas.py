from typing import Literal
from decimal import Decimal

from ..project.schemas import CamelModel
from ..categories.schemas import CategoryOut
from ..card_operations_generics.schemas import CardOperationIn, CardOperationOut


class CostIn(CardOperationIn):
    """Model for cost data getting from request"""

    category_id: int


class CostOut(CardOperationOut):
    """Model for cost data returning in response"""

    category: CategoryOut


class TotalCosts(CamelModel):
    """Model for total costs response"""

    total_costs: Decimal


class CategoryCosts(CamelModel):
    """Model for costs statistic by categories"""

    category_title: str
    category_color: str
    category_costs: Decimal


class CreateCost400Error(CamelModel):
    detail: Literal[
        "Cost amount is more than card amount",
        "Cost for card with differrent currency than default must contain `card_currency_amount` field"
    ]


class Cost404Error(CamelModel):
    detail: Literal["Cost with this id doesn't exist"]
