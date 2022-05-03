from fastapi import Depends

from .accounts import get_current_user
from ..schemas.accounts import UserOut
from ..schemas.cards import CardOut, Card
from ..services.cards import (
    get_all_user_cards, create_new_user_card, get_concrete_user_card,
    update_concrete_user_card
)


async def get_all_cards(user: UserOut = Depends(get_current_user)):
    """Return all cards for user"""
    cards = await get_all_user_cards(user.id)
    cards_out = [CardOut.from_orm(card) for card in cards]
    return cards_out


async def create_new_card(
    card_info: Card, user: UserOut = Depends(get_current_user)
):
    """Create a new card"""
    created_card_id = await create_new_user_card(card_info, user.id)
    card_out = CardOut(**card_info.dict(), id=created_card_id)
    return card_out


async def get_concrete_card(
    card_id: int, user: UserOut = Depends(get_current_user)
):
    """Return a concrete user card by id"""
    card_db = await get_concrete_user_card(card_id, user.id)
    card_out = CardOut.from_orm(card_db)
    return card_out


async def update_concrete_card(
    card_info: Card, updating_card: CardOut = Depends(get_concrete_card)
):
    """Update the concrete card using data from request"""
    await update_concrete_user_card(updating_card.id, card_info)
    print(updating_card.amount)
    card_out = CardOut(
        **card_info.dict(), id=updating_card.id, amount=updating_card.amount
    )
    return card_out
