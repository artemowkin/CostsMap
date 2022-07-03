from fastapi import HTTPException

from ..accounts.models import UserNamedTuple
from ..categories.models import CategoryNamedTuple
from ..cards.models import CardNamedTuple
from ..card_operations_generics.services import CardOperationGetter
from .models import Costs
from .schemas import CostIn


class CostsGetter(CardOperationGetter):
    """Service with get costs operations"""

    def _get_model(self) -> type[Costs]:
        """Return cost model"""
        return Costs

    def _get_total_sum_query(self) -> str:
        """Return query string to get total costs sum"""
        return (
            "select sum(user_currency_amount) as total_costs from costs where "
            "user_id = :user_id and date >= date(:start_date) and date < date(:end_date);"
        )


async def create_db_cost(
    user: UserNamedTuple, card: CardNamedTuple, category: CategoryNamedTuple,
    cost_data: CostIn
) -> Costs:
    """Create new cost for the user and return created cost id"""
    created_cost = await Costs.objects.create(**cost_data.dict(), user=user, card=card, category=category)
    return created_cost


async def delete_db_cost(cost) -> None:
    """Delete the concrete user cost by id"""
    await cost.delete()


def validate_creating_cost_amount_currency(cost_data: CostIn, cost_card: CardNamedTuple, user: UserNamedTuple):
    if cost_card.currency != user.currency and cost_data.card_currency_amount is None:
        err_msg = "Cost for card with differrent currency than default must contain `card_currency_amount` field"
        raise HTTPException(status_code=400, detail=err_msg)
