from datetime import datetime

from fastapi import Depends, Query

from .accounts import get_current_user
from ..schemas.accounts import UserOut
from ..schemas.categories import CategoryOut
from ..services.categories import get_categories_with_costs_for_the_month


current_month = datetime.utcnow().strftime("%Y-%m")


async def get_all_categories_for_month(
    month: str = Query(current_month, regex=r"\d{4}-\d{2}"),
    user: UserOut = Depends(get_current_user),
):
    """Return all categories with costs for the month"""
    categories = await get_categories_with_costs_for_the_month(user, month)
    categories_out = [
        CategoryOut.from_orm(category) for category in categories
    ]
    return categories_out
