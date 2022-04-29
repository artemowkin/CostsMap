from fastapi import HTTPException
from asyncpg.exceptions import UniqueViolationError

from ..schemas.accounts import UserOut
from ..schemas.categories import BaseCategory
from app.db.categories import categories
from app.db.main import database


def category_exists_decorator(func):
    """Handle UniqueViolation when create a new category"""

    async def inner(*args, **kwargs):
        try:
            await func(*args, **kwargs)
        except UniqueViolationError:
            raise HTTPException(
                status_code=400,
                detail="Category with this title already exists"
            )

    return inner


async def get_categories_with_costs_for_the_month(user: UserOut, month: str):
    """Return user categories with costs for the month"""
    get_query = categories.select().where(categories.c.user_id == user.id)
    db_categories = await database.fetch_all(get_query)
    return db_categories


@category_exists_decorator
async def create_category(category: BaseCategory, user: UserOut):
    """Create a new category and return its id"""
    create_query = categories.insert().values(
        **category.dict(), user_id=user.id
    )
    category_id = await database.execute(create_query)
    return category_id


async def get_category_by_id(category_id: int, user: UserOut):
    """Return the concrete category by id"""
    get_query = categories.select().where(
        categories.c.id == category_id, categories.c.user_id == user.id
    )
    category = await database.fetch_one(get_query)
    return category
