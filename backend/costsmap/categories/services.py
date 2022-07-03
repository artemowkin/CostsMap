from typing import Mapping, Literal, Any
from datetime import datetime
from dateutil.relativedelta import relativedelta

from fastapi import HTTPException
from asyncpg.exceptions import UniqueViolationError
from sqlite3 import IntegrityError

from ..project.models import database
from ..accounts.models import UserNamedTuple
from .schemas import BaseCategory
from .models import Categories, CategoryNamedTuple


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


async def get_all_user_categories(user_id: int) -> list[CategoryNamedTuple]:
    """Return all user categories"""
    db_categories = await Categories.objects.filter(user__id=user_id).order_by('id').all()
    return db_categories


async def get_costs_for_categories(
    user_id: int, month: str
) -> list[Mapping[Literal['id'] | Literal['costs_sum'], Any]]:
    """Return user categories with costs for the month"""
    start_date = datetime.fromisoformat(month + '-01')
    end_date = start_date + relativedelta(months=1)
    get_query = (
        'select categories.id, sum(costs.user_currency_amount) as costs_sum from '
        'categories join costs on costs.category = categories.id '
        'where costs.date >= date(:start_date) and costs.date < date(:end_date) and categories.user = :user_id '
        'group by categories.id;'
    )
    values = {'start_date': start_date, 'end_date': end_date, 'user_id': user_id}
    db_categories = await database.fetch_all(get_query, values)
    return db_categories


@category_exists_decorator
async def create_category(category: BaseCategory, user: UserNamedTuple) -> CategoryNamedTuple:
    """Create a new category and return its id"""
    created_category = await Categories.objects.create(**category.dict(), user=user)
    return created_category


async def get_category_by_id(category_id: int, user_id: int) -> CategoryNamedTuple:
    """Return the concrete category by id"""
    try:
        db_category = await Categories.objects.get(id=category_id, user__id=user_id)
        return db_category
    except:
        raise HTTPException(
            status_code=404, detail="Category with this id doesn't exist"
        )



@category_exists_decorator
async def update_category_by_id(category_id: int, category_data: BaseCategory) -> None:
    """Update the concrete category using category id"""
    await Categories.objects.filter(id=category_id).update(**category_data.dict())


async def delete_category(category_id: int) -> None:
    """Delete the category using id"""
    await Categories.objects.filter(id=category_id).delete()