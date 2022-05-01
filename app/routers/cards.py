from fastapi import APIRouter, Depends

from ..schemas.cards import CardOut
from ..dependencies.cards import get_all_cards


router = APIRouter()


@router.get('/', response_model=list[CardOut])
def all_cards(cards: list[CardOut] = Depends(get_all_cards)):
    """Return all user cards"""
    return cards
