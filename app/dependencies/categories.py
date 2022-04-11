from fastapi import Depends, HTTPException
from asyncpg.exceptions import UniqueViolationError

from app.schemas.categories import Category
from app.schemas.accounts import User
from app.db.categories import categories
from app.db.main import database
from .accounts import current_user


async def create_category(
    category_data: Category, user: User = Depends(current_user)
):
    """Create category from `category_data` for current user"""
    create_data = {'title': category_data.title, 'owner': user.id}
    create_sql = categories.insert().values(**create_data)
    try:
        created_category_id = await database.execute(create_sql)
    except UniqueViolationError:
        raise HTTPException(
            status_code=400, detail="category with this title already exists"
        )

    if not created_category_id:
        raise HTTPException(status_code=400, detail="category was not created")

    return category_data
