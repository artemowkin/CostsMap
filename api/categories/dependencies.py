from datetime import datetime

from fastapi import Depends, Query

from accounts.dependencies import get_current_user
from accounts.schemas import UserOut
from .schemas import CategoryOut, BaseCategory
from .services import (
    get_costs_for_categories, get_all_user_categories, create_category,
    get_category_by_id, update_category_by_id, delete_category
)


today_month = datetime.now().strftime("%Y-%m")


async def get_all_categories(
    user: UserOut = Depends(get_current_user),
    month: str = Query(today_month, regex=r"\d{4}-\d{2}")
):
    """Return all categories with costs for the month"""
    all_categories = await get_all_user_categories(user)
    categories_out = [CategoryOut.from_orm(category) for category in all_categories]
    categories_costs = await get_costs_for_categories(user, month)
    for category_costs in categories_costs:
        changing_category = list(filter(lambda category: category.id == category_costs.id, categories_out))[0]
        changing_category.costs_sum = category_costs.costs_sum

    return categories_out


async def create_concrete_category(
    category: BaseCategory,
    user: UserOut = Depends(get_current_user),
):
    """Create the new category"""
    created_category = await create_category(category, user)
    category_data = CategoryOut.from_orm(created_category)
    return category_data


async def get_concrete_category(
    category_id: int, user: UserOut = Depends(get_current_user)
):
    """Return a concrete category by category id"""
    category = await get_category_by_id(category_id, user)
    category_out = CategoryOut.from_orm(category)
    return category_out


async def update_concrete_category(
    updating_category_data: BaseCategory,
    category: CategoryOut = Depends(get_concrete_category)
):
    """Update the concrete category by id"""
    assert category.id
    await update_category_by_id(category.id, updating_category_data)
    updated_category = CategoryOut(
        **updating_category_data.dict(), id=category.id
    )
    return updated_category


async def delete_category_by_id(
    category: CategoryOut = Depends(get_concrete_category)
):
    """Delete the concrete category using category id"""
    assert category.id
    await delete_category(category.id)
