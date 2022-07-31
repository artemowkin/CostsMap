from decimal import Decimal

from orm.exceptions import NoMatch
from fastapi import HTTPException
from asyncpg.exceptions import UniqueViolationError
from sqlite3 import IntegrityError

from ..accounts.models import UserNamedTuple
from .models import Cards, CardNamedTuple
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


async def get_all_user_cards(user_id: int) -> list[CardNamedTuple]:
    """Return all user cards using user id"""
    db_cards = await Cards.objects.filter(user__id=user_id).order_by('id').all()
    return db_cards


@unique_card_handler
async def create_new_user_card(card_info: Card, user: UserNamedTuple) -> CardNamedTuple:
    """Create a new card for user and return it"""
    created_card = await Cards.objects.create(**card_info.dict(), user=user)
    return created_card


async def get_concrete_user_card(card_id: int, user_id: int) -> CardNamedTuple:
    """Return a concrete user card using card id and user id"""
    try:
        card_db = await Cards.objects.filter(user__id=user_id, id=card_id).get()
        return card_db
    except NoMatch:
        raise HTTPException(status_code=404, detail="Card with this id doesn't exist")



@unique_card_handler
async def update_concrete_user_card(card_id: int, card_info: Card) -> None:
    """Update the concrete card in db"""
    await Cards.objects.filter(id=card_id).update(**card_info.dict())


async def delete_concrete_user_card(card_id: int) -> None:
    """Delete the concrete card in db"""
    await Cards.objects.filter(id=card_id).delete()


async def transfer_money_between_cards(from_card, to_card, transfer_info: Transfer) -> None:
    """Transfer money between two cards"""
    from_result_amount = from_card.amount - transfer_info.from_amount
    to_result_amount = to_card.amount + transfer_info.to_amount

    async with Cards.registry.database.transaction():
        await Cards.objects.filter(id=from_card.id).update(amount=from_result_amount)
        await Cards.objects.filter(id=to_card.id).update(amount=to_result_amount)


async def update_card_amount(card: CardNamedTuple, new_amount: Decimal) -> None:
    if new_amount < 0:
        raise HTTPException(status_code=400, detail="Operation amount is more than card amount")

    await card.update(amount=new_amount)
