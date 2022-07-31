from datetime import date
from dateutil.relativedelta import relativedelta

from ..accounts.models import UserNamedTuple
from ..categories.models import CategoryNamedTuple
from ..cards.models import CardNamedTuple
from ..card_operations_generics.services import CardOperationGetter
from ..project.models import database
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
            "\"user\" = :user_id and date >= date(:start_date) and date < date(:end_date);"
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


async def get_categories_costs_for_the_month(month: str, user: UserNamedTuple) -> list:
    month_start_date = date.fromisoformat(month + '-01')
    month_end_date = month_start_date + relativedelta(months=1)
    query = (
        "select category as category_id, sum(user_currency_amount) as category_costs from "
        "costs where user = :user_id and date >= date(:start_date) and date < date(:end_date) "
        "group by category;"
    )
    categories_costs = await database.fetch_all(query, {
        'user_id': user.id, 'start_date': month_start_date, 'end_date': month_end_date
    })
    return categories_costs
