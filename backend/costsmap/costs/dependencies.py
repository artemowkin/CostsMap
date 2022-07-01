from datetime import date

from fastapi import Query, Depends

from ..project.models import database
from ..accounts.models import UserNamedTuple
from ..accounts.dependencies import get_current_user
from ..categories.services import get_category_by_id
from ..cards.services import update_card_amount, get_concrete_user_card
from ..cards.dependencies import get_concrete_card
from .schemas import CostOut, TotalCosts, Cost
from .services import (
    get_all_user_costs_by_month, get_total_costs_for_the_month,
    create_db_cost, delete_db_cost, get_concrete_user_cost,
    validate_creating_cost_amount_currency
)


today_string = date.today().strftime("%Y-%m")


async def get_all_costs_for_the_month(
    month: str = Query(today_string, regex=r"\d{4}-\d{2}"),
    user: UserNamedTuple = Depends(get_current_user),
) -> list[CostOut]:
    """Return all costs for the month (current by default)"""
    db_costs = await get_all_user_costs_by_month(user.id, month)
    out_costs = [CostOut.from_orm(db_cost) for db_cost in db_costs]
    return out_costs


async def get_total_costs(
    month: str = Query(today_string, regex=r"\d{4}-\d{2}"),
    user: UserNamedTuple = Depends(get_current_user)
):
    """Return total costs for the month for concrete user"""
    total_costs = await get_total_costs_for_the_month(user.id, month)
    return TotalCosts(total_costs=total_costs)


async def create_new_cost(
    cost_data: Cost,
    user: UserNamedTuple = Depends(get_current_user)
):
    """Create the new cost and subtract cost sum from card amount"""
    async with database.transaction():
        created_cost_card = await get_concrete_user_card(cost_data.card_id, user.id)
        validate_creating_cost_amount_currency(cost_data, created_cost_card, user)
        created_cost_category = await get_category_by_id(cost_data.category_id, user.id)
        created_cost = await create_db_cost(user, created_cost_card, created_cost_category, cost_data)
        cost_amount = cost_data.card_currency_amount if cost_data.card_currency_amount else cost_data.user_currency_amount
        subtracted_card_amount = created_cost_card.amount - cost_amount
        await update_card_amount(user.id, cost_data.card_id, subtracted_card_amount)

    created_cost_scheme = CostOut.from_orm(created_cost)
    return created_cost_scheme


async def delete_cost_by_id(
    cost_id: int,
    user: UserNamedTuple = Depends(get_current_user)
):
    """Delete the concrete cost by id and plus cost sum to card amount"""
    async with database.transaction():
        deleting_cost = await get_concrete_user_cost(cost_id, user.id)
        deleting_cost_card = await get_concrete_card(deleting_cost.card.id, user)
        plussed_card_amount = deleting_cost_card.amount + deleting_cost.amount
        await update_card_amount(user.id, deleting_cost_card.id, plussed_card_amount)
        await delete_db_cost(cost_id, user.id)
