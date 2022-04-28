from fastapi import APIRouter, Depends

from ..schemas.categories import CategoryOut
from ..dependencies.categories import get_all_categories_for_month


router = APIRouter()


@router.get('/', response_model=list[CategoryOut])
def all_categories(
    categories: list[CategoryOut] = Depends(get_all_categories_for_month)
):
    """Return all categories for the month"""
    return categories
