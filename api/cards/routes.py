from fastapi import APIRouter, Depends

from cards.schemas import CardOut
from cards.dependencies import (
    get_all_cards, create_new_card, get_concrete_card,
    update_concrete_card, delete_concrete_card,
    transfer_between_cards
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


@router.delete(
    '/{card_id}/',
    status_code=204,
    dependencies=[Depends(delete_concrete_card)]
)
def delete_card():
    """Delete the concrete card using card id"""
    pass


@router.post(
    '/transfer/',
    status_code=204,
    dependencies=[Depends(transfer_between_cards)]
)
def transfer():
    """Transfer money between two cards"""
    pass
