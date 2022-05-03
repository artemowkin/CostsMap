from fastapi import HTTPException
from asyncpg.exceptions import UniqueViolationError
from sqlite3 import IntegrityError

from ..db.cards import cards
from ..db.main import get_database
from ..schemas.cards import Card


database = get_database()


def unique_card_handler(func):

    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            return result
        except (UniqueViolationError, IntegrityError):
            raise HTTPException(
                status_code=400,
                detail="Card with this title already exists"
            )

    return wrapper


async def get_all_user_cards(user_id: int):
    """Return all user cards using user id"""
    get_query = cards.select().where(cards.c.user_id == user_id)
    db_cards = await database.fetch_all(get_query)
    return db_cards


@unique_card_handler
async def create_new_user_card(card_info: Card, user_id: int) -> int:
    """Create a new card for user and return its id"""
    create_query = cards.insert().values(**card_info.dict(), user_id=user_id)
    created_card_id = await database.execute(create_query)
    return created_card_id


async def get_concrete_user_card(card_id: int, user_id: int):
    """Return a concrete user card using card id and user id"""
    get_query = cards.select().where(
        cards.c.id == card_id, cards.c.user_id == user_id
    )
    card_db = await database.fetch_one(get_query)
    if not card_db: raise HTTPException(
        status_code=404, detail="Card with this id doesn't exist"
    )
    return card_db
