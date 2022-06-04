from datetime import date

from fastapi import Query, Depends
from databases import Database

from project.db import get_database
from .services import (
    get_all_user_costs_by_month
)
from categories.services import get_category_by_id
from .schemas import CostOut
from categories.schemas import CategoryOut
from accounts.schemas import UserOut
from accounts.dependencies import get_current_user


today_string = date.today().strftime("%Y-%m")


async def get_all_costs_for_the_month(
    month: str = Query(today_string, regex=r"\d{4}-\d{2}"),
    user: UserOut = Depends(get_current_user),
    db: Database = Depends(get_database)
):
    """Return all costs for the month (current by default)"""
    db_costs = await get_all_user_costs_by_month(user, month, db)
    out_costs = []
    for db_cost in db_costs:
        costs_dict = dict(zip(db_cost.keys(), db_cost.values()))
        db_category = await get_category_by_id(db_cost.category_id, user, db)
        costs_dict['category'] = CategoryOut.from_orm(db_category)
        out_costs.append(CostOut(**costs_dict))

    return out_costs
