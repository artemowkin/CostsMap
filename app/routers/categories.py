from fastapi import APIRouter, Depends

from app.schemas.categories import Category
from app.dependencies.categories import create_category


router = APIRouter()


@router.post("/create", response_model=Category)
async def create_category(category: int = Depends(create_category)):
    return category
