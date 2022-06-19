from decimal import Decimal
from datetime import date

from databases import Database
from dateutil.relativedelta import relativedelta
from sqlalchemy import desc

from accounts.schemas import UserOut
from .db import incomes


async def get_all_user_incomes_by_month(user: UserOut, month: str, db: Database) -> list:
    """Return all user incomes for the month"""
    month_start_date = date.fromisoformat(month + '-01')
    month_end_date = month_start_date + relativedelta(months=1)
    get_query = incomes.select().where(
        incomes.c.user_id == user.id, incomes.c.date >= month_start_date,
        incomes.c.date < month_end_date
    ).order_by(desc(incomes.c.date))
    db_incomes = await db.fetch_all(get_query)
    return db_incomes


async def get_total_incomes_for_the_month(user_id: int, month: str, db: Database) -> Decimal:
    """Return total incomes for the month"""
    month_start_date = date.fromisoformat(month + '-01')
    month_end_date = month_start_date + relativedelta(months=1)
    query = (
        "select sum(user_currency_amount) as total_incomes from incomes where "
        "user_id = :user_id and date >= date(:start_date) and date < date(:end_date);"
    )
    total_incomes = await db.fetch_val(query, {
        'user_id': user_id, 'start_date': month_start_date, 'end_date': month_end_date
    })
    return Decimal(total_incomes or 0)
