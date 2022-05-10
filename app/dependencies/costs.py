from datetime import date

from fastapi import Query, Depends

from ..services.costs import (
    get_all_user_costs_by_month
)
from ..services.categories import get_category_by_id
from ..schemas.costs import CostOut
from ..schemas.categories import CategoryOut
from ..schemas.accounts import UserOut
from .accounts import get_current_user


today_string = date.today().strftime("%Y-%m")


async def get_all_costs_for_the_month(
    month: str = Query(today_string, regex=r"\d{4}-\d{2}"),
    user: UserOut = Depends(get_current_user)
):
    """Return all costs for the month (current by default)"""
    db_costs = await get_all_user_costs_by_month(user, month)
    out_costs = []
    for db_cost in db_costs:
        costs_dict = dict(zip(db_cost.keys(), db_cost.values()))
        db_category = await get_category_by_id(db_cost.category_id, user)
        costs_dict['category'] = CategoryOut.from_orm(db_category)
        out_costs.append(CostOut(**costs_dict))

    return out_costs
