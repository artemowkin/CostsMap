from ..schemas.accounts import UserOut
from app.db.categories import categories
from app.db.main import database


async def get_categories_with_costs_for_the_month(user: UserOut, month: str):
    """Return user categories with costs for the month"""
    get_query = categories.select().where(categories.c.user_id == user.id)
    db_categories = await database.fetch_all(get_query)
    return db_categories
