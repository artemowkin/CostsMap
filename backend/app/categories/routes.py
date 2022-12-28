from uuid import UUID

from fastapi import APIRouter, Depends

from .models import Category
from .dependencies import use_categories_set
from .services import CategoriesSet
from .schemas import CategoryIn


router = APIRouter()


category_response_schema = Category.get_pydantic(exclude={'owner'})


@router.get('/', response_model=list[category_response_schema])
async def get_all(categories_set: CategoriesSet = Depends(use_categories_set)):
    all_categories = await categories_set.all()
    return all_categories


@router.post('/', response_model=category_response_schema)
async def create(
        category_data: CategoryIn,
        categories_set: CategoriesSet = Depends(use_categories_set)
    ):
    created_category = await categories_set.create(category_data)
    return created_category


@router.get('/{category_uuid}/', response_model=category_response_schema)
async def get_concrete(
        category_uuid: UUID,
        categories_set: CategoriesSet = Depends(use_categories_set)
    ):
    category = await categories_set.get_concrete(str(category_uuid))
    return category


@router.delete('/{category_uuid}/', status_code=204)
async def delete_concrete(
        category_uuid: UUID,
        categories_set: CategoriesSet = Depends(use_categories_set)
    ):
    category = await categories_set.get_concrete(str(category_uuid))
    await categories_set.delete_concrete(category)
