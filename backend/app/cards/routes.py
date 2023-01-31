from uuid import UUID

from fastapi import APIRouter, Depends

from .services import CardsSet
from .dependencies import use_cards_set
from .schemas import CardIn, CardOut


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
async def concrete_card(card_uuid: UUID, cards_set: CardsSet = Depends(use_cards_set)):
    """Returns concrete user card by uuid"""
    card = await cards_set.get_concrete(str(card_uuid))
    return CardOut.from_orm(card)


@router.delete('/{card_uuid}/', status_code=204)
async def delete_card(card_uuid: UUID, cards_set: CardsSet = Depends(use_cards_set)):
    """Deletes concrete user card by uuid"""
    card = await cards_set.get_concrete(str(card_uuid))
    await cards_set.delete_concrete(card.uuid)


@router.put('/{card_uuid}/', response_model=CardOut)
async def update_card(
        card_uuid: UUID, card_data: CardIn, cards_set: CardsSet = Depends(use_cards_set)
    ):
    """Updates concrete user card by uuid using data from request"""
    card = await cards_set.get_concrete(str(card_uuid))
    updated_card = await cards_set.update(card, card_data)
    return CardOut.from_orm(updated_card)
