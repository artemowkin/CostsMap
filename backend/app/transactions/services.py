from abc import abstractmethod
from typing import Generic, TypeVar
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import delete
from sqlalchemy.sql.selectable import Select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from ..authentication.models import User
from ..cards.services import CardsSet
from ..cards.models import Card
from ..project.db import Base
from .schemas import BaseTransactionIn


T = TypeVar('T', bound=Base)

D = TypeVar('D', bound=BaseTransactionIn)


def _handle_not_found_error(func):

    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except NoResultFound:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                "Transaction with this id for current user doesn't exist"
            )

    return wrapper


class TransactionSet(Generic[T, D]):
    """Generic base class for card transactions
    
    :param _user: Current user instance
    :param _cards_set: Cards logic container
    """

    _user: User
    _cards_set: CardsSet
    _model: T
    _session: AsyncSession

    @abstractmethod
    def _get_select_all_statement(self, month: str) -> Select[tuple[T]]:
        ...

    async def all(self, month: str) -> list[T]:
        """Returns all user transactions
        
        :param month: Month to get transactions in format YYYY-MM
        :returns: All transactions filtered by user and month
        """
        stmt = self._get_select_all_statement(month)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    @abstractmethod
    def _get_select_concrete_statement(self, uuid: str) -> Select[tuple[T]]:
        ...

    @_handle_not_found_error
    async def get_concrete(self, uuid: str) -> T:
        """Returns concrete user transaction by uuid
        
        :param uuid: Transaction uuid
        :raises: HTTPException(404) if transaction with this uuid for user doesn't exist
        :returns: Getted transaction with this uuid
        """
        stmt = self._get_select_concrete_statement(uuid)
        result = await self._session.execute(stmt)
        return result.scalar_one()

    @abstractmethod
    async def _get_creation_statement(self, data: D) -> Select[tuple[T]]:
        ...

    @abstractmethod
    async def _add_transaction_to_card(self, transaction: T, data: D) -> None:
        ...

    async def create(self, data: D) -> T:
        """Creates a new transaction for user and card from data
        
        :param data: Creation transaction data
        :returns: Created transaction instance
        """
        stmt = await self._get_creation_statement(data)
        result = await self._session.execute(stmt)
        transaction = result.scalar_one()
        await self._add_transaction_to_card(transaction, data)
        return transaction

    @abstractmethod
    async def _discard_transaction_to_card(self, transaction: T) -> None:
        ...

    async def delete(self, transaction: T) -> None:
        """Deletes concrete user transaction
        
        :param transaction: Deleting transaction instance
        """
        await self._discard_transaction_to_card(transaction)
        stmt = delete(self._model).where(self._model.uuid == transaction.uuid)
        await self._session.execute(stmt)

    @abstractmethod
    async def _update_card_amount(self, old_card: Card, new_card: Card, old_transaction_amount: Decimal, data: D) -> None:
        ...

    @abstractmethod
    async def _get_update_statement(self, transaction: T, data: D) -> Select[tuple[T]]:
        ...

    async def update(self, transaction: T, data: D) -> T:
        """Updates concrete user transaction and card amount
        
        :param transaction: Updating transaction
        :param transaction_data: New transaction data
        :returns: Updated transaction instance
        """
        old_card, old_transaction_amount = transaction.card, transaction.amount
        new_card = await self._cards_set.get_concrete(str(data.card_id))
        if old_transaction_amount != data.amount:
            await self._update_card_amount(old_card, new_card, old_transaction_amount, data)

        stmt = await self._get_update_statement(transaction, data)
        result = await self._session.execute(stmt)
        return result.scalar_one()
