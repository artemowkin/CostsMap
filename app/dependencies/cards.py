from fastapi import Depends

from .accounts import get_current_user
from ..schemas.accounts import UserOut
from ..schemas.cards import CardOut
from ..services.cards import get_all_user_cards


async def get_all_cards(user: UserOut = Depends(get_current_user)):
    """Return all cards for user"""
    cards = await get_all_user_cards(user.id)
    cards_out = [CardOut.from_orm(card) for card in cards]
    return cards_out
