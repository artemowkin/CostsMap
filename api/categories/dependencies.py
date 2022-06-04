from datetime import datetime

from fastapi import Depends, Query
from databases import Database

from project.db import get_database
from accounts.dependencies import get_current_user
from accounts.schemas import UserOut
from .schemas import CategoryOut, BaseCategory
from .services import (
    get_categories_with_costs_for_the_month, create_category,
    get_category_by_id, update_category_by_id, delete_category
)


current_month = datetime.utcnow().strftime("%Y-%m")


async def get_all_categories_for_month(
    month: str = Query(current_month, regex=r"\d{4}-\d{2}"),
    user: UserOut = Depends(get_current_user),
    db: Database = Depends(get_database)
):
    """Return all categories with costs for the month"""
    categories = await get_categories_with_costs_for_the_month(user, month, db)
    categories_out = [
        CategoryOut.from_orm(category) for category in categories
    ]
    return categories_out


async def create_concrete_category(
    category: BaseCategory,
    user: UserOut = Depends(get_current_user),
    db: Database = Depends(get_database)
):
    """Create the new category"""
    category_id = await create_category(category, user, db)
    category_data = CategoryOut(
        **category.dict(), id=category_id
    )
    return category_data


async def get_concrete_category(
    category_id: int, user: UserOut = Depends(get_current_user),
    db: Database = Depends(get_database)
):
    """Return a concrete category by category id"""
    category = await get_category_by_id(category_id, user, db)
    category_out = CategoryOut.from_orm(category)
    return category_out


async def update_concrete_category(
    updating_category_data: BaseCategory,
    category: CategoryOut = Depends(get_concrete_category),
    db: Database = Depends(get_database)
):
    """Update the concrete category by id"""
    assert category.id
    await update_category_by_id(category.id, updating_category_data, db)
    updated_category = CategoryOut(
        **updating_category_data.dict(), id=category.id
    )
    return updated_category


async def delete_category_by_id(
    category: CategoryOut = Depends(get_concrete_category),
    db: Database = Depends(get_database)
):
    """Delete the concrete category using category id"""
    assert category.id
    await delete_category(category.id, db)
