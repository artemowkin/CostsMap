from datetime import datetime
from decimal import Decimal

from datetime import date
from dateutil.relativedelta import relativedelta

from databases import Database
from sqlalchemy import desc

from accounts.schemas import UserOut
from categories.services import get_category_by_id
from .db import costs
from .schemas import Cost, CostOut


async def get_all_user_costs_by_month(user: UserOut, month: str, db: Database):
    """Return all user costs for the month"""
    month_start_date = date.fromisoformat(month + '-01')
    month_end_date = month_start_date + relativedelta(months=1)
    get_query = costs.select().where(
        costs.c.user_id == user.id, costs.c.date >= month_start_date,
        costs.c.date < month_end_date
    ).order_by(desc(costs.c.date))
    db_costs = await db.fetch_all(get_query)
    return db_costs


async def get_total_costs_for_the_month(user_id: int, month: str, db: Database) -> Decimal:
    """Return total costs sum for the month"""
    month_start_date = date.fromisoformat(month + '-01')
    month_end_date = month_start_date + relativedelta(months=1)
    query = (
        "select sum(amount) as total_costs from costs where "
        "user_id = :user_id and date >= date(:start_date) and date < date(:end_date);"
    )
    total_costs = await db.fetch_val(query, {
        'user_id': user_id, 'start_date': month_start_date, 'end_date': month_end_date
    })
    return Decimal(total_costs or 0)


async def create_db_cost(user: UserOut, cost_data: Cost, db: Database) -> int:
    """Create new cost for the user and return created cost id"""
    query = costs.insert().values(user_id=user.id, **cost_data.dict())
    created_cost_id = await db.execute(query)
    return created_cost_id
