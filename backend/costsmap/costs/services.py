from decimal import Decimal
from datetime import date

from dateutil.relativedelta import relativedelta
from fastapi import HTTPException

from ..project.models import database
from ..accounts.models import UserNamedTuple
from ..categories.models import CategoryNamedTuple
from ..cards.models import CardNamedTuple
from .models import Costs, CostNamedTuple
from .schemas import Cost


async def get_all_user_costs_by_month(user_id: int, month: str) -> list[CostNamedTuple]:
    """Return all user costs for the month"""
    month_start_date = date.fromisoformat(month + '-01')
    month_end_date = month_start_date + relativedelta(months=1)
    db_costs = await Costs.objects.filter(
        user__id=user_id, date__gte=month_start_date, date__lt=month_end_date
    ).order_by('-date').all()
    return db_costs


async def get_concrete_user_cost(cost_id: int, user_id: int) -> CostNamedTuple:
    """Return the concrete user cost by id"""
    db_cost = await Costs.objects.get(id=cost_id, user__id=user_id)
    if not db_cost:
        raise HTTPException(
            status_code=404, detail="Cost with this id doesn't exist"
        )

    return db_cost


async def get_total_costs_for_the_month(user_id: int, month: str) -> Decimal:
    """Return total costs sum for the month"""
    month_start_date = date.fromisoformat(month + '-01')
    month_end_date = month_start_date + relativedelta(months=1)
    query = (
        "select sum(user_currency_amount) as total_costs from costs where "
        "user_id = :user_id and date >= date(:start_date) and date < date(:end_date);"
    )
    total_costs = await database.fetch_val(query, {
        'user_id': user_id, 'start_date': month_start_date, 'end_date': month_end_date
    })
    return Decimal(total_costs or 0)


async def create_db_cost(
    user: UserNamedTuple, card: CardNamedTuple, category: CategoryNamedTuple,
    cost_data: Cost
) -> Costs:
    """Create new cost for the user and return created cost id"""
    created_cost = await Costs.objects.create(**cost_data.dict(), user=user, card=card, category=category)
    return created_cost


async def delete_db_cost(cost_id: int, user_id: int) -> None:
    """Delete the concrete user cost by id"""
    await Costs.objects.filter(user__id=user_id, id=cost_id).delete()


def validate_creating_cost_amount_currency(cost_data: Cost, cost_card: CardNamedTuple, user: UserNamedTuple):
    if cost_card.currency != user.currency and cost_data.card_currency_amount is None:
        err_msg = "Cost for card with differrent currency than default must contain `card_currency_amount` field"
        raise HTTPException(status_code=400, detail=err_msg)
