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
