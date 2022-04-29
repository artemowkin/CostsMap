from fastapi import APIRouter, Depends

from ..schemas.categories import CategoryOut
from ..dependencies.categories import (
    get_all_categories_for_month, create_concrete_category
)


router = APIRouter()


@router.get('/', response_model=list[CategoryOut])
def all_categories(
    categories: list[CategoryOut] = Depends(get_all_categories_for_month)
):
    """Return all categories for the month"""
    return categories


@router.post('/', response_model=CategoryOut)
def create_categories(
    category: CategoryOut = Depends(create_concrete_category)
):
    """Return the concrete category by ID"""
    return category
