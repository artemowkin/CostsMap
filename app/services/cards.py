from ..db.cards import cards
from ..db.main import database


async def get_all_user_cards(user_id: int):
    """Return all user cards using user id"""
    get_query = cards.select().where(cards.c.user_id == user_id)
    db_cards = await database.fetch_all(get_query)
    return db_cards
