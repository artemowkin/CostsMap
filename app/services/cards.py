from fastapi import HTTPException
from asyncpg.exceptions import UniqueViolationError
from sqlite3 import IntegrityError

from ..db.cards import cards
from ..schemas.cards import Card
from ..settings import config


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
    db_cards = await config.database.fetch_all(get_query)
    return db_cards


@unique_card_handler
async def create_new_user_card(card_info: Card, user_id: int) -> int:
    """Create a new card for user and return its id"""
    create_query = cards.insert().values(**card_info.dict(), user_id=user_id)
    created_card_id = await config.database.execute(create_query)
    return created_card_id


async def get_concrete_user_card(card_id: int, user_id: int):
    """Return a concrete user card using card id and user id"""
    get_query = cards.select().where(
        cards.c.id == card_id, cards.c.user_id == user_id
    )
    card_db = await config.database.fetch_one(get_query)
    if not card_db: raise HTTPException(
        status_code=404, detail="Card with this id doesn't exist"
    )
    return card_db


@unique_card_handler
async def update_concrete_user_card(card_id: int, card_info: Card):
    """Update the concrete card in db"""
    update_query = cards.update().values(**card_info.dict()).where(
        cards.c.id == card_id
    )
    await config.database.execute(update_query)


async def delete_concrete_user_card(card_id: int):
    """Delete the concrete card in db"""
    delete_query = cards.delete().where(cards.c.id == card_id)
    await config.database.execute(delete_query)
