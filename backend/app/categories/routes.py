from uuid import UUID

from fastapi import APIRouter, Depends

from .models import Category
from .dependencies import use_categories_set
from .services import CategoriesSet
from .schemas import CategoryIn, CategoryOut
from ..costs.services import CostsSet
from ..costs.dependencies import use_costs_set


router = APIRouter()


async def _construct_category_out(category: Category, costs_set: CostsSet) -> CategoryOut:
    """Constructs category out schema with category costs sum"""
    costs_sum = await costs_set.get_category_sum(category)
    return CategoryOut(**category.dict(), costs_sum=costs_sum)


@router.get('/', response_model=list[CategoryOut])
async def get_all(
        categories_set: CategoriesSet = Depends(use_categories_set),
        costs_set: CostsSet = Depends(use_costs_set)
    ):
    """Returns all current user categories"""
    all_categories = await categories_set.all()
    categories_out = [await _construct_category_out(category, costs_set) for category in all_categories]
    return categories_out


@router.post('/', response_model=CategoryOut)
async def create(
        category_data: CategoryIn,
        categories_set: CategoriesSet = Depends(use_categories_set)
    ):
    """Creates new category for current user"""
    created_category = await categories_set.create(category_data)
    return CategoryOut(**created_category.dict(), costs_sum=0)


@router.get('/{category_uuid}/', response_model=CategoryOut)
async def get_concrete(
        category_uuid: UUID,
        categories_set: CategoriesSet = Depends(use_categories_set),
        costs_set: CostsSet = Depends(use_costs_set)
    ):
    """Returns cocnrete user category by uuid"""
    category = await categories_set.get_concrete(str(category_uuid))
    costs_sum = await costs_set.get_category_sum(category)
    return CategoryOut(**category.dict(), costs_sum=costs_sum)


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
    category = await categories_set.get_concrete(str(category_uuid))
    updated_category = await categories_set.update(category, category_data)
    costs_sum = await costs_set.get_category_sum(category)
    return CategoryOut(**updated_category.dict(), costs_sum=costs_sum)
