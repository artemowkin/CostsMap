from fastapi import HTTPException
from asyncpg.exceptions import UniqueViolationError
from sqlite3 import IntegrityError

from ..schemas.accounts import UserOut
from ..schemas.categories import BaseCategory
from app.db.categories import categories
from ..settings import config


def category_exists_decorator(func):
    """Handle UniqueViolation when create a new category"""

    async def inner(*args, **kwargs):
        try:
            await func(*args, **kwargs)
        except (UniqueViolationError, IntegrityError):
            raise HTTPException(
                status_code=400,
                detail="Category with this title already exists"
            )

    return inner


async def get_categories_with_costs_for_the_month(user: UserOut, month: str):
    """Return user categories with costs for the month"""
    get_query = categories.select().where(categories.c.user_id == user.id)
    db_categories = await config.database.fetch_all(get_query)
    return db_categories


@category_exists_decorator
async def create_category(category: BaseCategory, user: UserOut):
    """Create a new category and return its id"""
    create_query = categories.insert().values(
        **category.dict(), user_id=user.id
    )
    category_id = await config.database.execute(create_query)
    return category_id


async def get_category_by_id(category_id: int, user: UserOut):
    """Return the concrete category by id"""
    get_query = categories.select().where(
        categories.c.id == category_id, categories.c.user_id == user.id
    )
    category = await config.database.fetch_one(get_query)
    if not category:
        raise HTTPException(
            status_code=404, detail="Category with this id doesn't exist"
        )

    return category


@category_exists_decorator
async def update_category_by_id(
    category_id: int, category_data: BaseCategory
):
    """Update the concrete category using category id"""
    update_query = categories.update().values(
        **category_data.dict()).where(categories.c.id == category_id)
    await config.database.execute(update_query)


async def delete_category(category_id: int):
    """Delete the category using id"""
    delete_query = categories.delete().where(categories.c.id == category_id)
    await config.database.execute(delete_query)
