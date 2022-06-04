from datetime import date
from dateutil.relativedelta import relativedelta

from databases import Database

from accounts.schemas import UserOut
from costs.db import costs


async def get_all_user_costs_by_month(user: UserOut, month: str, db: Database):
    """Return all user costs for the month"""
    month_start_date = date.fromisoformat(month + '-01')
    month_end_date = month_start_date + relativedelta(months=1)
    get_query = costs.select().where(
        costs.c.user_id == user.id, costs.c.date >= month_start_date,
        costs.c.date < month_end_date
    )
    db_costs = await db.fetch_all(get_query)
    return db_costs
