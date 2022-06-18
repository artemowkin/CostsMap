from decimal import Decimal

from fastapi import HTTPException
from asyncpg.exceptions import UniqueViolationError
from sqlite3 import IntegrityError
from databases import Database

from .db import cards
from .schemas import Card, Transfer


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


async def get_all_user_cards(user_id: int, db: Database):
    """Return all user cards using user id"""
    get_query = cards.select().where(cards.c.user_id == user_id).order_by(cards.c.id)
    db_cards = await db.fetch_all(get_query)
    return db_cards


@unique_card_handler
async def create_new_user_card(card_info: Card, user_id: int, db: Database) -> int:
    """Create a new card for user and return its id"""
    create_query = cards.insert().values(**card_info.dict(), user_id=user_id)
    created_card_id = await db.execute(create_query)
    return created_card_id


async def get_concrete_user_card(card_id: int, user_id: int, db: Database):
    """Return a concrete user card using card id and user id"""
    get_query = cards.select().where(
        cards.c.id == card_id, cards.c.user_id == user_id
    )
    card_db = await db.fetch_one(get_query)
    if not card_db: raise HTTPException(
        status_code=404, detail="Card with this id doesn't exist"
    )
    return card_db


@unique_card_handler
async def update_concrete_user_card(card_id: int, card_info: Card, db: Database):
    """Update the concrete card in db"""
    update_query = cards.update().values(**card_info.dict()).where(
        cards.c.id == card_id
    )
    await db.execute(update_query)


async def delete_concrete_user_card(card_id: int, db: Database):
    """Delete the concrete card in db"""
    delete_query = cards.delete().where(cards.c.id == card_id)
    await db.execute(delete_query)


async def transfer_money_between_cards(
        from_card, to_card, transfer_info: Transfer, db: Database):
    """Transfer money between two cards"""
    from_result_amount = from_card.amount - transfer_info.from_amount
    to_result_amount = to_card.amount + transfer_info.to_amount

    update_query_from = cards.update().values(
        amount=from_result_amount).where(cards.c.id == from_card.id)
    update_query_to = cards.update().values(
        amount=to_result_amount).where(cards.c.id == to_card.id)

    async with db.transaction():
        await db.execute(update_query_from)
        await db.execute(update_query_to)


async def subtract_cost_from_card(card_id: int, new_amount: Decimal, db: Database) -> None:
    if new_amount < 0:
        raise HTTPException(status_code=400, detail="Cost amount is more than card amount")

    query = cards.update().values(amount=new_amount).where(cards.c.id == card_id)
    await db.execute(query)
