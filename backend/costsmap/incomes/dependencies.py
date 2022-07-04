from decimal import Decimal
from typing import Callable, Coroutine, Any
from datetime import date

from fastapi import Depends, Query

from ..accounts.models import UserNamedTuple
from ..accounts.dependencies import get_current_user
from ..card_operations_generics.dependencies import (
    CardOperationDeleteCommand, CardOperationCreateCommand,
    GetAllCardOperationsCommand
)
from .services import IncomesGetter, create_db_income, delete_db_income
from .schemas import IncomeOut, TotalIncomes, IncomeIn, IncomeOut


today_string = date.today().strftime("%Y-%m")


async def get_total_incomes(month: str = Query(today_string, regex=r"\d{4}-\d{2}"),
        user: UserNamedTuple = Depends(get_current_user)):
    """Return total incomes for the month for concrete user"""
    incomes_getter = IncomesGetter(user.id)
    total_incomes = await incomes_getter.get_total_for_the_month(month)
    return TotalIncomes(total_incomes=total_incomes)


class GetAllIncomesCommand(GetAllCardOperationsCommand):
    """Dependency for getting all incomes"""

    def _get_getter_class(self) -> type[IncomesGetter]:
        return IncomesGetter

    def _get_schema(self) -> type[IncomeOut]:
        return IncomeOut

    async def _load_foreigns(self, operations) -> None:
        for income in operations:
            await income.card.load()


class CreateIncomeCommand(CardOperationCreateCommand):
    """Dependency for incomes creating"""

    operation_name = "Income"

    def _get_create_service(self) -> Callable[..., Coroutine[Any, Any, Any]]:
        return create_db_income

    async def _get_extra_foreigns(self, operation_data: IncomeIn, user: UserNamedTuple) -> tuple:
        (operation_data, user) # For skipping linter warnings
        return tuple()

    def _calculate_new_card_amount(self, card_amount: Decimal, operation_amount: Decimal) -> Decimal:
        """Plus income amount to card amount"""
        return card_amount + operation_amount

    async def _get_operation_schema(self, operation) -> IncomeOut:
        await operation.card.load()
        income_schema = IncomeOut.from_orm(operation)
        return income_schema


class DeleteIncomeCommand(CardOperationDeleteCommand):
    """Dependency for incomes deleting"""

    def _get_getter_class(self) -> type[IncomesGetter]:
        return IncomesGetter

    def _get_delete_service(self) -> Callable[..., Coroutine[Any, Any, Any]]:
        return delete_db_income

    def _calculate_new_card_amount(self, card_amount: Decimal, operation_amount: Decimal) -> Decimal:
        """Subtract income amount from card amount"""
        return card_amount - operation_amount
