from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete, update
from sqlalchemy.exc import NoResultFound

from ..authentication.models import User
from .models import Card
from .schemas import CardIn
from ..project.db import async_session


def _handle_unique_violation(func):
    """Decorator that handles unique violation error when creating/updating cards"""

    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except IntegrityError:
            raise HTTPException(status.HTTP_409_CONFLICT, "Card with this title already exists")

    return wrapper


def _handle_not_found_error(func):

    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except NoResultFound:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Card with this uuid for current user doesn't exist")

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
        async with async_session() as session:
            stmt = select(Card).where(Card.owner_id == self._user.uuid)
            result = await session.execute(stmt)
            return result.scalars().all()

    @_handle_unique_violation
    async def create(self, card_data: CardIn) -> Card:
        """Create the new card for user
        
        :param card_data: Card creation data
        :raises: HTTPException(409) if card with this title already exists
        :returns: Created card instance
        """
        async with async_session() as session:
            card = Card(**card_data.dict(), owner_id=self._user.uuid)
            session.add(card)
            await session.commit()
            return card

    @_handle_not_found_error
    async def get_concrete(self, card_uuid: str) -> Card:
        """Returns concrete user card by uuid
        
        :param card_uuid: Getting card uuid
        :raises: HTTPException(404) if card with this uuid doesn't exist
        :returns: Card instance with this uuid
        """
        async with async_session() as session:
            stmt = select(Card).where(Card.uuid == card_uuid, Card.owner_id == self._user.uuid)
            result = await session.execute(stmt)
            return result.scalar_one()

    async def delete_concrete(self, card_uuid: str) -> None:
        """Deletes concrete user card
        
        :param card_uuid: Deleting card uuid
        """
        async with async_session() as session:
            stmt = delete(Card).where(Card.uuid == card_uuid, User.uuid == self._user.uuid)
            await session.execute(stmt)
            await session.commit()

    async def add_cost(self, card: Card, amount: Decimal):
        """Updates user card amount with cost
        
        :param card: Updating card instance
        :param amount: Cost amount
        """
        async with async_session() as session:
            new_card_amount = card.amount - amount
            card.amount = new_card_amount
            await session.commit()

    async def add_income(self, card: Card, amount: Decimal):
        """Updates user card amount with income
        
        :param card: Updating card instance
        :param amount: Income amount
        """
        async with async_session() as session:
            new_card_amount = card.amount + amount
            card.amount = new_card_amount
            await session.commit()

    @_handle_unique_violation
    async def update(self, card: Card, card_data: CardIn) -> Card:
        """Updates user card data
        
        :param card: Updating card instance
        :param card_data: New card data
        :raises: HTTPException(409) if card with new title from card_data already exists
        """
        async with async_session() as session:
            stmt = update(Card).values(**card_data.dict()).where(Card.uuid == card.uuid)
            await session.execute(stmt)
            stmt = select(Card).where(Card.uuid == card.uuid)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()
