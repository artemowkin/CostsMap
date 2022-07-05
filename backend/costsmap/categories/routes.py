from fastapi import APIRouter, Depends

from ..accounts.schemas import LoginRequiredResponse
from .schemas import CategoryOut, CategoryUniqueTitleError, Category404Error
from .dependencies import (
    get_all_categories, create_concrete_category,
    get_concrete_category, update_concrete_category,
    delete_category_by_id
)


router = APIRouter()


@router.get('/', response_model=list[CategoryOut], responses={
    401: {"model": LoginRequiredResponse},
})
def all_categories(
    categories: list[CategoryOut] = Depends(get_all_categories)
):
    """Return all categories for the month"""
    return categories


@router.post('/', response_model=CategoryOut, status_code=201, responses={
    401: {"model": LoginRequiredResponse},
    400: {"model": CategoryUniqueTitleError},
})
def create_categories(
    category: CategoryOut = Depends(create_concrete_category)
):
    """Create a new category"""
    return category


@router.get('/{category_id}/', response_model=CategoryOut, responses={
    401: {"model": LoginRequiredResponse},
    404: {"model": Category404Error},
})
def get_concrete_category(
    category: CategoryOut = Depends(get_concrete_category)
):
    """Return the concrete category by ID"""
    return category


@router.put('/{category_id}/', response_model=CategoryOut, responses={
    401: {"model": LoginRequiredResponse},
    400: {"model": CategoryUniqueTitleError},
    404: {"model": Category404Error},
})
def update_concrete_category(
    category: CategoryOut = Depends(update_concrete_category)
):
    """Update the concrete category"""
    return category


@router.delete(
    '/{category_id}/',
    status_code=204,
    dependencies=[Depends(delete_category_by_id)],
    responses={
        401: {"model": LoginRequiredResponse},
        404: {"model": Category404Error},
    }
)
def delete_concrete_category():
    """Delete the concrete category by id"""
    pass
