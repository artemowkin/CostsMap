from datetime import date

from fastapi import Query, Depends
from databases import Database

from project.db import get_database
from .services import (
    get_all_user_costs_by_month, get_total_costs_for_the_month
)
from categories.services import get_category_by_id
from categories.dependencies import get_concrete_category
from categories.schemas import CategoryOut
from accounts.schemas import UserOut
from accounts.dependencies import get_current_user
from cards.services import get_concrete_user_card, subtract_cost_from_card
from cards.schemas import CardOut
from cards.dependencies import get_concrete_card
from .schemas import CostOut, TotalCosts, Cost
from .services import create_db_cost


today_string = date.today().strftime("%Y-%m")


async def get_all_costs_for_the_month(
    month: str = Query(today_string, regex=r"\d{4}-\d{2}"),
    user: UserOut = Depends(get_current_user),
    db: Database = Depends(get_database)
):
    """Return all costs for the month (current by default)"""
    assert user.id
    db_costs = await get_all_user_costs_by_month(user, month, db)
    out_costs = []
    for db_cost in db_costs:
        costs_dict = dict(zip(db_cost.keys(), db_cost.values()))
        db_category = await get_category_by_id(db_cost.category_id, user, db)
        db_card = await get_concrete_user_card(db_cost.card_id, user.id, db)
        costs_dict['category'] = CategoryOut.from_orm(db_category)
        costs_dict['card'] = CardOut.from_orm(db_card)
        out_costs.append(CostOut(**costs_dict))

    return out_costs


async def get_total_costs(
    month: str = Query(today_string, regex=r"\d{4}-\d{2}"),
    user: UserOut = Depends(get_current_user),
    db: Database = Depends(get_database)
):
    """Return total costs for the month for concrete user"""
    assert user.id
    total_costs = await get_total_costs_for_the_month(user.id, month, db)
    return TotalCosts(total_costs=total_costs)


async def create_new_cost(
    cost_data: Cost,
    user: UserOut = Depends(get_current_user),
    db: Database = Depends(get_database)
):
    async with db.transaction():
        created_cost_id = await create_db_cost(user, cost_data, db)
        created_cost_category = await get_concrete_category(cost_data.category_id, user, db)
        created_cost_card = await get_concrete_card(cost_data.card_id, user, db)
        subtracted_card_amount = created_cost_card.amount - cost_data.amount
        await subtract_cost_from_card(cost_data.card_id, subtracted_card_amount, db)

    created_cost_scheme = CostOut(
        id=created_cost_id,
        category=created_cost_category,
        card=created_cost_card,
        **cost_data.dict()
    )
    return created_cost_scheme
