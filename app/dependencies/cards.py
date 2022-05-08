from fastapi import Depends
from fastapi.exceptions import HTTPException

from .accounts import get_current_user
from ..schemas.accounts import UserOut
from ..schemas.cards import CardOut, Card, Transfer
from ..services.cards import (
    get_all_user_cards, create_new_user_card, get_concrete_user_card,
    update_concrete_user_card, delete_concrete_user_card,
    transfer_money_between_cards
)


async def get_all_cards(user: UserOut = Depends(get_current_user)):
    """Return all cards for user"""
    assert user.id is not None
    cards = await get_all_user_cards(user.id)
    cards_out = [CardOut.from_orm(card) for card in cards]
    return cards_out


async def create_new_card(
    card_info: Card, user: UserOut = Depends(get_current_user)
):
    """Create a new card"""
    assert user.id is not None
    created_card_id = await create_new_user_card(card_info, user.id)
    card_out = CardOut(**card_info.dict(), id=created_card_id)
    return card_out


async def get_concrete_card(
    card_id: int, user: UserOut = Depends(get_current_user)
):
    """Return a concrete user card by id"""
    assert user.id is not None
    card_db = await get_concrete_user_card(card_id, user.id)
    card_out = CardOut.from_orm(card_db)
    return card_out


async def update_concrete_card(
    card_info: Card, updating_card: CardOut = Depends(get_concrete_card)
):
    """Update the concrete card using data from request"""
    await update_concrete_user_card(updating_card.id, card_info)
    card_out = CardOut(
        **card_info.dict(), id=updating_card.id, amount=updating_card.amount
    )
    return card_out


async def delete_concrete_card(
    deleting_card: CardOut = Depends(get_concrete_card)
):
    """Delete the concrete user card by id"""
    await delete_concrete_user_card(deleting_card.id)


def _validate_to_amount(to_amount: int | None):
    if to_amount is None:
        exc_detail = (
            "`to_amount` is required if cards currencies are not the same"
        )
        raise HTTPException(status_code=400, detail=exc_detail)


def _validate_has_card_transfer_money(card, transfer_sum):
    assert card.amount is not None
    if card.amount < transfer_sum:
        raise HTTPException(
            status_code=400, detail="Card amount is less than transfer sum"
        )


async def transfer_between_cards(
    transfer_info: Transfer,
    user: UserOut = Depends(get_current_user)
):
    """Transfer money between two cards from transfer_info"""
    assert user.id is not None
    from_card = await get_concrete_user_card(transfer_info.from_id, user.id)
    _validate_has_card_transfer_money(from_card, transfer_info.from_amount)
    to_card = await get_concrete_user_card(transfer_info.to_id, user.id)
    if from_card.currency != to_card.currency:
        _validate_to_amount(transfer_info.to_amount)
    else:
        transfer_info.to_amount = transfer_info.from_amount

    await transfer_money_between_cards(
        from_card, to_card, transfer_info
    )
