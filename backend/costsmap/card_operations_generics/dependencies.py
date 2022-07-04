from typing import Callable, Coroutine, Any
from decimal import Decimal
from datetime import date
from abc import ABC, abstractmethod

from fastapi import Depends, HTTPException, Query

from ..accounts.models import UserNamedTuple
from ..accounts.dependencies import get_current_user
from ..cards.services import get_concrete_user_card, update_card_amount
from ..project.models import database
from .services import CardOperationGetter
from .schemas import CardOperationIn, CardOperationOut
from .models import CardOperationNamedTuple


today_string = date.today().strftime("%Y-%m")


def _get_operation_amount(operation: CardOperationNamedTuple | CardOperationIn) -> Decimal:
    """Return the operation card currency amount if exists else user currency amount"""
    if operation.card_currency_amount:
        return operation.card_currency_amount

    return operation.user_currency_amount


class GetAllCardOperationsCommand(ABC):
    """Abstract dependency that returns all card operations"""

    def __init__(self):
        self._getter_class = self._get_getter_class()
        self._schema = self._get_schema()

    @abstractmethod
    def _get_getter_class(self) -> type[CardOperationGetter]:
        """Return the getter instance"""
        pass

    @abstractmethod
    def _get_schema(self) -> type[CardOperationOut]:
        pass

    async def __call__(self, month: str = Query(today_string, regex=r"\d{4}-\d{2}"),
            user: UserNamedTuple = Depends(get_current_user)):
        """Get all card operations dependency call method"""
        getter = self._getter_class(user.id)
        operations = await getter.get_all_for_the_month(month)
        await self._load_foreigns(operations)
        out_operations = [self._schema.from_orm(operation) for operation in operations]
        return out_operations

    @abstractmethod
    async def _load_foreigns(self, operations) -> None:
        pass


class CardOperationCreateCommand(ABC):
    """Abstract dependency that creates the card operation"""

    operation_name: str = "Card operation"

    def __init__(self) -> None:
        self._create_service = self._get_create_service()

    @abstractmethod
    def _get_create_service(self) -> Callable[..., Coroutine[Any, Any, Any]]:
        pass

    async def __call__(self, operation_data: CardOperationIn, user: UserNamedTuple = Depends(get_current_user)):
        """
        Create card operation dependency call method. Creates the operation and changes card amount
        """
        async with database.transaction():
            operation_card = await get_concrete_user_card(operation_data.card_id, user.id)
            self._validate_operation_currency(operation_data.card_currency_amount, operation_card.currency, user.currency)
            extra_foreigns = await self._get_extra_foreigns(operation_data, user)
            operation_amount = _get_operation_amount(operation_data)
            new_card_amount = self._calculate_new_card_amount(operation_card.amount, operation_amount)
            await update_card_amount(operation_card, new_card_amount)
            created_operation = await self._create_service(user, operation_card, *extra_foreigns, operation_data)

        created_operation_schema = await self._get_operation_schema(created_operation)
        return created_operation_schema

    def _validate_operation_currency(self, operation_card_amount: Decimal | None,
            card_currency: str, user_currency: str) -> None:
        """`card_currency_amount` field is required when card currency doesn't equal user currency"""
        if card_currency != user_currency and operation_card_amount is None:
            err_msg = f"{self.operation_name} for card with differrent currency than default must contain `card_currency_amount` field"
            raise HTTPException(status_code=400, detail=err_msg)

    @abstractmethod
    async def _get_extra_foreigns(self, operation_data: CardOperationIn, user: UserNamedTuple) -> tuple:
        pass

    @abstractmethod
    def _calculate_new_card_amount(self, card_amount: Decimal, operation_amount: Decimal) -> Decimal:
        """Return new card amount"""
        pass

    @abstractmethod
    async def _get_operation_schema(self, operation) -> CardOperationOut:
        pass


class CardOperationDeleteCommand(ABC):
    """Abstract dependency that deletes the card operation"""

    def __init__(self) -> None:
        self._getter_class = self._get_getter_class()
        self._delete_service = self._get_delete_service()

    @abstractmethod
    def _get_getter_class(self) -> type[CardOperationGetter]:
        """Return the getter instance"""
        pass

    @abstractmethod
    def _get_delete_service(self) -> Callable[..., Coroutine[Any, Any, Any]]:
        """Return the delete service function for deleting operation"""
        pass

    async def __call__(self, operation_id: int, user: UserNamedTuple = Depends(get_current_user)) -> None:
        """
        Delete card operation dependency call method. Deletes the operation and changes card amount
        """
        getter = self._getter_class(user.id)
        async with database.transaction():
            operation = await getter.get_concrete(operation_id)
            operation_card = await get_concrete_user_card(operation.card.id, user.id)
            operation_amount = _get_operation_amount(operation)
            new_card_amount = self._calculate_new_card_amount(operation_card.amount, operation_amount)
            await update_card_amount(operation_card, new_card_amount)
            await self._delete_service(operation)

    @abstractmethod
    def _calculate_new_card_amount(self, card_amount: Decimal, operation_amount: Decimal) -> Decimal:
        """Return new card amount"""
        pass
