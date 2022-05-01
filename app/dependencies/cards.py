from fastapi import Depends

from .accounts import get_current_user
from ..schemas.accounts import UserOut
from ..schemas.cards import CardOut, Card
from ..services.cards import get_all_user_cards, create_new_user_card


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
