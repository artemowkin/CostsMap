from ..schemas.accounts import UserOut
from ..schemas.categories import BaseCategory
from app.db.categories import categories
from app.db.main import database


async def get_categories_with_costs_for_the_month(user: UserOut, month: str):
    """Return user categories with costs for the month"""
    get_query = categories.select().where(categories.c.user_id == user.id)
    db_categories = await database.fetch_all(get_query)
    return db_categories


async def create_category(category: BaseCategory, user: UserOut):
    """Create a new category and return its id"""
    create_query = categories.insert().values(
        **category.dict(), user_id=user.id
    )
    category_id = await database.execute(create_query)
    return category_id
