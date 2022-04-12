from fastapi import APIRouter, Depends

from app.schemas.categories import (
    Category, Category404, CategoryDeleted, Category400
)
from app.dependencies.categories import (
    create_category, get_user_categories, get_category_by_title,
    delete_category_by_title, update_category_by_title
)


router = APIRouter()


@router.post(
    "/create", response_model=Category,
    responses={400: {'model': Category400}}
)
async def create_category(category: Category = Depends(create_category)):
    """Create a new category for current user with the following `title`"""
    return category


@router.get("", response_model=list[Category])
async def get_all_categories(
    categories: list[Category] = Depends(get_user_categories)
):
    """Return all categories of current user"""
    return categories


@router.get(
    "/{category_title}", response_model=Category,
    responses={404: {'model': Category404}}
)
async def get_concrete_category(
    category: Category = Depends(get_category_by_title)
):
    """Return a concrete category by `title`"""
    return category


@router.delete(
    "/{category_title}",
    dependencies=[Depends(delete_category_by_title)],
    response_model=CategoryDeleted,
    responses={404: {'model': Category404}}
)
def delete_category():
    """Delete a concrete category by `title`"""
    return {'deleted': True}


@router.put(
    "/{category_title}", response_model=Category,
    responses={404: {'model': Category404}}
)
async def update_category(
    category: Category = Depends(update_category_by_title)
):
    """Update a concrete category by `title` field"""
    return category
