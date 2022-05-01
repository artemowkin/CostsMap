from fastapi import APIRouter, Depends

from ..schemas.cards import CardOut
from ..dependencies.cards import get_all_cards, create_new_card


router = APIRouter()


@router.get('/', response_model=list[CardOut])
def all_cards(cards: list[CardOut] = Depends(get_all_cards)):
    """Return all user cards"""
    return cards


@router.post('/', response_model=CardOut)
def create_card(card: CardOut = Depends(create_new_card)):
    """Create a new card for current user"""
    return card
