from uuid import UUID

from fastapi import APIRouter, Depends

from .models import Category
from .dependencies import use_categories_set
from .services import CategoriesSet
from .schemas import CategoryIn, CategoryOut


router = APIRouter()


async def _construct_category_out(category: Category, categories_set: CategoriesSet) -> CategoryOut:
    costs_sum = await categories_set.get_costs_sum(category)
    return CategoryOut(**category.dict(), costs_sum=costs_sum)


@router.get('/', response_model=list[CategoryOut])
async def get_all(categories_set: CategoriesSet = Depends(use_categories_set)):
    all_categories = await categories_set.all()
    categories_out = [await _construct_category_out(category, categories_set) for category in all_categories]
    return categories_out


@router.post('/', response_model=CategoryOut)
async def create(
        category_data: CategoryIn,
        categories_set: CategoriesSet = Depends(use_categories_set)
    ):
    created_category = await categories_set.create(category_data)
    return CategoryOut(**created_category.dict(), costs_sum=0)


@router.get('/{category_uuid}/', response_model=CategoryOut)
async def get_concrete(
        category_uuid: UUID,
        categories_set: CategoriesSet = Depends(use_categories_set)
    ):
    category = await categories_set.get_concrete(str(category_uuid))
    costs_sum = await categories_set.get_costs_sum(category)
    return CategoryOut(**category.dict(), costs_sum=costs_sum)


@router.delete('/{category_uuid}/', status_code=204)
async def delete_concrete(
        category_uuid: UUID,
        categories_set: CategoriesSet = Depends(use_categories_set)
    ):
    category = await categories_set.get_concrete(str(category_uuid))
    await categories_set.delete_concrete(category)


@router.put('/{category_uuid}/', response_model=CategoryOut)
async def update_category(
        category_uuid: UUID,
        category_data: CategoryIn,
        categories_set: CategoriesSet = Depends(use_categories_set)
    ):
    category = await categories_set.get_concrete(str(category_uuid))
    updated_category = await categories_set.update(category, category_data)
    costs_sum = await categories_set.get_costs_sum(category)
    return CategoryOut(**updated_category.dict(), costs_sum=costs_sum)
