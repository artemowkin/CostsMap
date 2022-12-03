from fastapi import APIRouter

from .schemas import CategoryOut, CategoryIn
from .services import CategoriesSet


router = APIRouter()


@router.post('/', response_model=CategoryOut)
async def create_category(category_data: CategoryIn):
    categories_set = CategoriesSet()
    created_category = await categories_set.create(category_data)
    return created_category


@router.get('/', response_model=list[CategoryOut])
async def get_all_categories():
    categories_set = CategoriesSet()
    all_categories = await categories_set.get_all()
    return all_categories
