from uuid import UUID

from fastapi import APIRouter, Depends, Query

from .models import Category
from .dependencies import use_categories_set
from .services import CategoriesSet
from .schemas import CategoryIn, CategoryOut
from ..costs.services import CostsSet
from ..costs.dependencies import use_costs_set
from ..utils.dates import get_current_month


router = APIRouter()


async def _construct_category_out(month: str, category: Category, costs_set: CostsSet) -> CategoryOut:
    """Constructs category out schema with category costs sum
    
    :param month: Month in format YYYY-MM
    :param category: Constructing category
    :param costs_set: CostsSet to get category costs for the month
    """
    costs_sum = await costs_set.get_category_sum(category, month)
    schema = CategoryOut.from_orm(category)
    schema.costs_sum = costs_sum
    return schema


@router.get('/', response_model=list[CategoryOut])
async def get_all(
        month: str | None = Query(None, regex=r"\d{4}-\d{2}"),
        categories_set: CategoriesSet = Depends(use_categories_set),
        costs_set: CostsSet = Depends(use_costs_set)
    ):
    """Returns all current user categories"""
    month = month if month else get_current_month()
    all_categories = await categories_set.all()
    categories_out = [await _construct_category_out(month, category, costs_set) for category in all_categories]
    return categories_out


@router.post('/', response_model=CategoryOut)
async def create(
        category_data: CategoryIn,
        categories_set: CategoriesSet = Depends(use_categories_set)
    ):
    """Creates new category for current user"""
    created_category = await categories_set.create(category_data)
    return CategoryOut.from_orm(created_category)


@router.get('/{category_uuid}/', response_model=CategoryOut)
async def get_concrete(
        category_uuid: UUID,
        month: str | None = Query(None, regex=r"\d{4}-\d{2}"),
        categories_set: CategoriesSet = Depends(use_categories_set),
        costs_set: CostsSet = Depends(use_costs_set)
    ):
    """Returns cocnrete user category by uuid"""
    month = month if month else get_current_month()
    category = await categories_set.get_concrete(str(category_uuid))
    return await _construct_category_out(month, category, costs_set)


@router.delete('/{category_uuid}/', status_code=204)
async def delete_concrete(
        category_uuid: UUID,
        categories_set: CategoriesSet = Depends(use_categories_set)
    ):
    """Deletes concrete user category by uuid"""
    category = await categories_set.get_concrete(str(category_uuid))
    await categories_set.delete_concrete(category)


@router.put('/{category_uuid}/', response_model=CategoryOut)
async def update_category(
        category_uuid: UUID,
        category_data: CategoryIn,
        categories_set: CategoriesSet = Depends(use_categories_set),
        costs_set: CostsSet = Depends(use_costs_set)
    ):
    """Updates concrete user category by uuid using data from request"""
    month = get_current_month()
    category = await categories_set.get_concrete(str(category_uuid))
    updated_category = await categories_set.update(category, category_data)
    return await _construct_category_out(month, updated_category, costs_set)
