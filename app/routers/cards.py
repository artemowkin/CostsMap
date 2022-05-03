from fastapi import APIRouter, Depends

from ..schemas.cards import CardOut
from ..dependencies.cards import (
    get_all_cards, create_new_card, get_concrete_card,
    update_concrete_card
)


router = APIRouter()


@router.get('/', response_model=list[CardOut])
def all_cards(cards: list[CardOut] = Depends(get_all_cards)):
    """Return all user cards"""
    return cards


@router.post('/', response_model=CardOut)
def create_card(card: CardOut = Depends(create_new_card)):
    """Create a new card for current user"""
    return card


@router.get('/{card_id}/', response_model=CardOut)
def concrete_card(card: CardOut = Depends(get_concrete_card)):
    """Return a concrete user card"""
    return card


@router.put('/{card_id}/', response_model=CardOut)
def update_card(card: CardOut = Depends(update_concrete_card)):
    """Update the concrete card using card id"""
    return card
