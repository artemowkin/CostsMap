from fastapi import APIRouter, Depends

from .services import CardsSet
from .dependencies import use_cards_set, valid_card_uuid
from .schemas import CardIn, CardOut
from .models import Card


router = APIRouter()


@router.get('/', response_model=list[CardOut])
async def all_cards(
        cards_set: CardsSet = Depends(use_cards_set)
    ):
    """Returns all cards of current user"""
    all_cards = await cards_set.all()
    return [CardOut.from_orm(card) for card in all_cards]


@router.post('/', response_model=CardOut)
async def create_card(card_data: CardIn, cards_set: CardsSet = Depends(use_cards_set)):
    """Creates new card for current user"""
    created_card = await cards_set.create(card_data)
    return CardOut.from_orm(created_card)


@router.get('/{card_uuid}/', response_model=CardOut)
async def concrete_card(card: Card = Depends(valid_card_uuid)):
    """Returns concrete user card by uuid"""
    return CardOut.from_orm(card)


@router.delete('/{card_uuid}/', status_code=204)
async def delete_card(card: Card = Depends(valid_card_uuid), cards_set: CardsSet = Depends(use_cards_set)):
    """Deletes concrete user card by uuid"""
    await cards_set.delete_concrete(card.uuid)


@router.put('/{card_uuid}/', response_model=CardOut)
async def update_card(
        card_data: CardIn, card: Card = Depends(valid_card_uuid), cards_set: CardsSet = Depends(use_cards_set)
    ):
    """Updates concrete user card by uuid using data from request"""
    updated_card = await cards_set.update(card, card_data)
    return CardOut.from_orm(updated_card)
