from datetime import datetime
from dateutil.relativedelta import relativedelta

from fastapi import HTTPException
from asyncpg.exceptions import UniqueViolationError
from sqlite3 import IntegrityError
from databases import Database

from accounts.schemas import UserOut
from categories.schemas import BaseCategory
from categories.db import categories


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


async def get_all_user_categories(user: UserOut, db: Database):
    """Return all user categories"""
    get_query = categories.select().where(categories.c.user_id == user.id)
    db_categories = await db.fetch_all(get_query)
    return db_categories


async def get_costs_for_categories(user: UserOut, month: str, db: Database):
    """Return user categories with costs for the month"""
    start_date = datetime.fromisoformat(month + '-01')
    end_date = start_date + relativedelta(months=1)
    get_query = (
        'select categories.id, sum(costs.amount) as costs_sum from '
        'categories join costs on costs.category_id = categories.id '
        'where costs.date >= date(:start_date) and costs.date < date(:end_date) and categories.user_id = :user_id '
        'group by categories.id;'
    )
    values = {'start_date': start_date, 'end_date': end_date, 'user_id': user.id}
    db_categories = await db.fetch_all(get_query, values)
    return db_categories


@category_exists_decorator
async def create_category(category: BaseCategory, user: UserOut, db: Database):
    """Create a new category and return its id"""
    create_query = categories.insert().values(
        **category.dict(), user_id=user.id
    )
    category_id = await db.execute(create_query)
    return category_id


async def get_category_by_id(category_id: int, user: UserOut, db: Database):
    """Return the concrete category by id"""
    get_query = categories.select().where(
        categories.c.id == category_id, categories.c.user_id == user.id
    )
    category = await db.fetch_one(get_query)
    if not category:
        raise HTTPException(
            status_code=404, detail="Category with this id doesn't exist"
        )

    return category


@category_exists_decorator
async def update_category_by_id(
    category_id: int, category_data: BaseCategory, db: Database
):
    """Update the concrete category using category id"""
    update_query = categories.update().values(
        **category_data.dict()).where(categories.c.id == category_id)
    await db.execute(update_query)


async def delete_category(category_id: int, db: Database):
    """Delete the category using id"""
    delete_query = categories.delete().where(categories.c.id == category_id)
    await db.execute(delete_query)
