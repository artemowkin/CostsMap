from decimal import Decimal
from typing import Callable, Coroutine, Any
from datetime import date

from fastapi import Query, Depends

from ..accounts.models import UserNamedTuple
from ..accounts.dependencies import get_current_user
from ..categories.services import get_category_by_id
from ..card_operations_generics.dependencies import (
    CardOperationDeleteCommand, CardOperationCreateCommand,
    GetAllCardOperationsCommand
)
from .schemas import CostOut, TotalCosts, CostIn
from .services import CostsGetter, create_db_cost, delete_db_cost


today_string = date.today().strftime("%Y-%m")


async def get_total_costs(month: str = Query(today_string, regex=r"\d{4}-\d{2}"),
        user: UserNamedTuple = Depends(get_current_user)):
    """Return total costs for the month for concrete user"""
    costs_getter = CostsGetter(user.id)
    total_costs = await costs_getter.get_total_for_the_month(month)
    return TotalCosts(total_costs=total_costs)


class GetAllCostsCommand(GetAllCardOperationsCommand):
    """Dependency for getting all costs"""

    def _get_getter_class(self) -> type[CostsGetter]:
        return CostsGetter

    def _get_schema(self) -> type[CostOut]:
        return CostOut

    async def _load_foreigns(self, operations) -> None:
        for cost in operations:
            await cost.card.load()
            await cost.category.load()


class CreateCostCommand(CardOperationCreateCommand):
    """Dependency for costs creating"""

    operation_name = "Cost"

    async def __call__(self, operation_data: CostIn, user: UserNamedTuple = Depends(get_current_user)):
        result = await super().__call__(operation_data, user)
        return result

    def _get_create_service(self) -> Callable[..., Coroutine[Any, Any, Any]]:
        return create_db_cost

    async def _get_extra_foreigns(self, operation_data: CostIn, user: UserNamedTuple) -> tuple:
        """Returns tuple with creating cost category"""
        cost_category = await get_category_by_id(operation_data.category_id, user.id)
        return (cost_category,)

    def _calculate_new_card_amount(self, card_amount: Decimal, operation_amount: Decimal) -> Decimal:
        """Subtract cost amount from card amount"""
        return card_amount - operation_amount

    async def _get_operation_schema(self, operation) -> CostOut:
        await operation.card.load()
        await operation.category.load()
        cost_schema = CostOut.from_orm(operation)
        return cost_schema


class DeleteCostCommand(CardOperationDeleteCommand):
    """Dependency for costs deleting"""

    def _get_getter_class(self) -> type[CostsGetter]:
        return CostsGetter

    def _get_delete_service(self) -> Callable[..., Coroutine[Any, Any, Any]]:
        return delete_db_cost

    def _calculate_new_card_amount(self, card_amount: Decimal, operation_amount: Decimal) -> Decimal:
        """Plus cost amount to card amount"""
        return card_amount + operation_amount
