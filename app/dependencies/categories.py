from datetime import datetime

from fastapi import Depends, Query

from .accounts import get_current_user
from ..schemas.accounts import UserOut
from ..schemas.categories import CategoryOut, BaseCategory
from ..services.categories import (
    get_categories_with_costs_for_the_month, create_category,
    get_category_by_id, update_category_by_id, delete_category
)


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


async def create_concrete_category(
    category: BaseCategory,
    user: UserOut = Depends(get_current_user)
):
    """Create the new category"""
    category_id = await create_category(category, user)
    category_data = CategoryOut(
        **category.dict(), id=category_id
    )
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
    await update_category_by_id(category.id, updating_category_data)
    updated_category = CategoryOut(
        **updating_category_data.dict(), id=category.id
    )
    return updated_category


async def delete_category_by_id(
    category: CategoryOut = Depends(get_concrete_category)
):
    """Delete the concrete category using category id"""
    await delete_category(category.id)
