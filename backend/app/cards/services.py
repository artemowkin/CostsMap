from decimal import Decimal

from fastapi import HTTPException, status
from asyncpg.exceptions import UniqueViolationError

from ..authentication.models import User
from .models import Card
from .schemas import CardIn


def _handle_unique_violation(func):

    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except UniqueViolationError:
            raise HTTPException(status.HTTP_409_CONFLICT, "Card with this title already exists")

    return wrapper


class CardsSet:

    def __init__(self, user: User):
        self._user = user
        self._model = Card

    async def all(self) -> list[Card]:
        all_user_cards = await self._model.objects.filter(owner__uuid=self._user.uuid).all()
        return all_user_cards

    @_handle_unique_violation
    async def create(self, card_data: CardIn) -> Card:
        created_card = await Card.objects.create(**card_data.dict(), owner=self._user)
        return created_card

    async def get_concrete(self, card_uuid: str) -> Card:
        card = await self._model.objects.get_or_none(uuid=card_uuid, owner__uuid=self._user.uuid)
        if not card:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Card with this uuid for current user doesn't exist")

        return card

    async def delete_concrete(self, card_uuid: str) -> None:
        await self._model.objects.delete(uuid=card_uuid, owner__uuid=self._user.uuid)

    async def add_cost(self, card: Card, amount: Decimal):
        new_card_amount = card.amount - amount
        await card.update(amount=new_card_amount)
        await card.load()

    async def add_income(self, card: Card, amount: Decimal):
        new_card_amount = card.amount + amount
        await card.update(amount=new_card_amount)
        await card.load()

    @_handle_unique_violation
    async def update(self, card: Card, card_data: CardIn) -> Card:
        await card.update(**card_data.dict())
        await card.load()
        return card
