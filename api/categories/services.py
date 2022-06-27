from typing import Mapping, Literal, Any
from datetime import datetime
from dateutil.relativedelta import relativedelta

from fastapi import HTTPException
from asyncpg.exceptions import UniqueViolationError
from sqlite3 import IntegrityError

from project.settings import config
from accounts.schemas import UserOut
from .schemas import BaseCategory
from .models import Categories


def category_exists_decorator(func):
    """Handle UniqueViolation when create a new category"""

    async def inner(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except (UniqueViolationError, IntegrityError):
            raise HTTPException(
                status_code=400,
                detail="Category with this title already exists"
            )

    return inner


async def get_all_user_categories(user: UserOut) -> list[Categories]:
    """Return all user categories"""
    db_categories = await Categories.objects.filter(user__id=user.id).order_by('id').all()
    return db_categories


async def get_costs_for_categories(
    user: UserOut, month: str
) -> list[Mapping[Literal['id'] | Literal['costs_sum'], Any]]:
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
    db_categories = await config.database.fetch_all(get_query, values)
    return db_categories


@category_exists_decorator
async def create_category(category: BaseCategory, user: UserOut) -> Categories:
    """Create a new category and return its id"""
    created_category = await Categories.objects.create(**category.dict(), user=user)
    return created_category


async def get_category_by_id(category_id: int, user: UserOut) -> list[Categories]:
    """Return the concrete category by id"""
    db_category = await Categories.objects.get(id=category_id, user__id=user.id)
    if not db_category:
        raise HTTPException(
            status_code=404, detail="Category with this id doesn't exist"
        )

    return db_category


@category_exists_decorator
async def update_category_by_id(category_id: int, category_data: BaseCategory) -> None:
    """Update the concrete category using category id"""
    await Categories.objects.filter(id=category_id).update(**category_data.dict())


async def delete_category(category_id: int) -> None:
    """Delete the category using id"""
    await Categories.objects.filter(id=category_id).delete()
