from decimal import Decimal

from fastapi import HTTPException, status
from asyncpg.exceptions import UniqueViolationError

from ..authentication.models import User
from .models import Card
from .schemas import CardIn


def _handle_unique_violation(func):
    """Decorator that handles unique violation error when creating/updating cards"""

    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except UniqueViolationError:
            raise HTTPException(status.HTTP_409_CONFLICT, "Card with this title already exists")

    return wrapper


class CardsSet:
    """Service with logic for cards
    
    :param user: User instance 
    """

    def __init__(self, user: User):
        self._user = user
        self._model = Card

    async def all(self) -> list[Card]:
        """Returns all user cards
        
        :returns: All cards filtered by user
        """
        all_user_cards = await self._model.objects.filter(owner__uuid=self._user.uuid).all()
        return all_user_cards

    @_handle_unique_violation
    async def create(self, card_data: CardIn) -> Card:
        """Create the new card for user
        
        :param card_data: Card creation data
        :raises: HTTPException(409) if card with this title already exists
        :returns: Created card instance
        """
        created_card = await Card.objects.create(**card_data.dict(), owner=self._user)
        return created_card

    async def get_concrete(self, card_uuid: str) -> Card:
        """Returns concrete user card by uuid
        
        :param card_uuid: Getting card uuid
        :raises: HTTPException(404) if card with this uuid doesn't exist
        :returns: Card instance with this uuid
        """
        card = await self._model.objects.get_or_none(uuid=card_uuid, owner__uuid=self._user.uuid)
        if not card:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Card with this uuid for current user doesn't exist")

        return card

    async def delete_concrete(self, card_uuid: str) -> None:
        """Deletes concrete user card
        
        :param card_uuid: Deleting card uuid
        """
        await self._model.objects.delete(uuid=card_uuid, owner__uuid=self._user.uuid)

    async def add_cost(self, card: Card, amount: Decimal):
        """Updates user card amount with cost
        
        :param card: Updating card instance
        :param amount: Cost amount
        """
        new_card_amount = card.amount - amount
        await card.update(amount=new_card_amount)
        await card.load()

    async def add_income(self, card: Card, amount: Decimal):
        """Updates user card amount with income
        
        :param card: Updating card instance
        :param amount: Income amount
        """
        new_card_amount = card.amount + amount
        await card.update(amount=new_card_amount)
        await card.load()

    @_handle_unique_violation
    async def update(self, card: Card, card_data: CardIn) -> Card:
        """Updates user card data
        
        :param card: Updating card instance
        :param card_data: New card data
        :raises: HTTPException(409) if card with new title from card_data already exists
        """
        await card.update(**card_data.dict())
        await card.load()
        return card
