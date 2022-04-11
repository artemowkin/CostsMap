from fastapi import APIRouter, Depends

from app.schemas.categories import Category
from app.dependencies.categories import create_category, get_user_categories


router = APIRouter()


@router.post("/create", response_model=Category)
async def create_category(category: int = Depends(create_category)):
    """Create a new category for current user with the following `title`"""
    return category


@router.get("/", response_model=list[Category])
async def get_all_categories(
    categories: list[Category] = Depends(get_user_categories)
):
    """Get all categories of current user"""
    return categories
