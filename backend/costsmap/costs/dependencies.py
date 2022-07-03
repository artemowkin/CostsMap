from datetime import date

from fastapi import Query, Depends

from ..project.models import database
from ..accounts.models import UserNamedTuple
from ..accounts.dependencies import get_current_user
from ..categories.services import get_category_by_id
from ..cards.services import update_card_amount, get_concrete_user_card
from .schemas import CostOut, TotalCosts, CostIn
from .services import CostsGetter, create_db_cost, delete_db_cost, validate_creating_cost_amount_currency


today_string = date.today().strftime("%Y-%m")


async def get_all_costs_for_the_month(month: str = Query(today_string, regex=r"\d{4}-\d{2}"),
        user: UserNamedTuple = Depends(get_current_user)) -> list[CostOut]:
    """Return all costs for the month (current by default)"""
    costs_getter = CostsGetter(user.id)
    db_costs = await costs_getter.get_all_for_the_month(month)
    await _load_costs_foreign_keys(db_costs)
    out_costs = [CostOut.from_orm(db_cost) for db_cost in db_costs]
    return out_costs


async def _load_costs_foreign_keys(costs):
    for cost in costs:
        await cost.card.load()
        await cost.category.load()


async def get_total_costs(month: str = Query(today_string, regex=r"\d{4}-\d{2}"),
        user: UserNamedTuple = Depends(get_current_user)):
    """Return total costs for the month for concrete user"""
    costs_getter = CostsGetter(user.id)
    total_costs = await costs_getter.get_total_for_the_month(month)
    return TotalCosts(total_costs=total_costs)


async def create_new_cost(cost_data: CostIn, user: UserNamedTuple = Depends(get_current_user)):
    """Create the new cost and subtract cost sum from card amount"""
    async with database.transaction():
        cost_card = await get_concrete_user_card(cost_data.card_id, user.id)
        validate_creating_cost_amount_currency(cost_data, cost_card, user)
        cost_category = await get_category_by_id(cost_data.category_id, user.id)
        cost_amount = cost_data.card_currency_amount if cost_data.card_currency_amount else cost_data.user_currency_amount
        subtracted_card_amount = cost_card.amount - cost_amount
        await update_card_amount(cost_card, subtracted_card_amount)
        created_cost = await create_db_cost(user, cost_card, cost_category, cost_data)

    created_cost_schema = await _get_cost_schema(created_cost)
    return created_cost_schema


async def _get_cost_schema(cost):
    await cost.card.load()
    await cost.category.load()
    cost_schema = CostOut.from_orm(cost)
    return cost_schema


async def delete_cost_by_id(cost_id: int, user: UserNamedTuple = Depends(get_current_user)):
    """Delete the concrete cost by id and plus cost sum to card amount"""
    costs_getter = CostsGetter(user.id)
    async with database.transaction():
        cost = await costs_getter.get_concrete(cost_id)
        cost_card = await get_concrete_user_card(cost.card.id, user.id)
        cost_amount = cost.card_currency_amount if cost.card_currency_amount else cost.user_currency_amount
        plussed_card_amount = cost_card.amount + cost_amount
        await update_card_amount(cost_card, plussed_card_amount)
        await delete_db_cost(cost)
