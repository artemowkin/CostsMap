from decimal import Decimal
from datetime import date

from dateutil.relativedelta import relativedelta
from fastapi import HTTPException

from project.models import database
from accounts.models import Users
from categories.models import Categories
from cards.models import Cards
from .models import Costs
from .schemas import Cost


async def get_all_user_costs_by_month(user_id: int, month: str) -> list[Costs]:
    """Return all user costs for the month"""
    month_start_date = date.fromisoformat(month + '-01')
    month_end_date = month_start_date + relativedelta(months=1)
    db_costs = await Costs.objects.filter(
        user__id=user_id, date__gte=month_start_date, date__lt=month_end_date
    ).order_by('-date').all()
    return db_costs


async def get_concrete_user_cost(cost_id: int, user_id: int) -> Costs:
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
        "select sum(amount) as total_costs from costs where "
        "user_id = :user_id and date >= date(:start_date) and date < date(:end_date);"
    )
    total_costs = await database.fetch_val(query, {
        'user_id': user_id, 'start_date': month_start_date, 'end_date': month_end_date
    })
    return Decimal(total_costs or 0)


async def create_db_cost(user: Users, card: Cards, category: Categories, cost_data: Cost) -> Costs:
    """Create new cost for the user and return created cost id"""
    created_cost = await Costs.objects.create(**cost_data.dict(), user=user, card=card, category=category)
    return created_cost


async def delete_db_cost(cost_id: int, user_id: int) -> None:
    """Delete the concrete user cost by id"""
    await Costs.objects.filter(user__id=user_id, id=cost_id).delete()
