from datetime import date

from fastapi import Depends, Query

from databases import Database
from project.db import get_database
from accounts.schemas import UserOut
from accounts.dependencies import get_current_user
from cards.dependencies import get_concrete_user_card, get_concrete_card
from cards.schemas import CardOut
from cards.services import update_card_amount
from .services import (
    get_all_user_incomes_by_month, get_total_incomes_for_the_month,
    create_db_income, validate_creating_income_amount_currency
)
from .schemas import IncomeOut, TotalIncomes, Income, IncomeOut


today_string = date.today().strftime("%Y-%m")


async def get_all_incomes_for_the_month(
    month: str = Query(today_string, regex=r"\d{4}-\d{2}"),
    user: UserOut = Depends(get_current_user),
    db: Database = Depends(get_database)
) -> list[IncomeOut]:
    """Return all incomes for the month (current by default)"""
    db_incomes = await get_all_user_incomes_by_month(user, month, db)
    out_incomes = []
    for db_income in db_incomes:
        income_dict = dict(zip(db_income.keys(), db_income.values()))
        db_card = await get_concrete_user_card(db_income.card_id, user.id, db)
        income_dict['card'] = CardOut.from_orm(db_card)
        out_incomes.append(IncomeOut(**income_dict))

    return out_incomes


async def get_total_incomes(
    month: str = Query(today_string, regex=r"\d{4}-\d{2}"),
    user: UserOut = Depends(get_current_user),
    db: Database = Depends(get_database)
):
    """Return total incomes for the month for concrete user"""
    total_incomes = await get_total_incomes_for_the_month(user.id, month, db)
    return TotalIncomes(total_incomes=total_incomes)


async def create_new_income(
    income_data: Income,
    user: UserOut = Depends(get_current_user),
    db: Database = Depends(get_database)
):
    """Create new income and plus income amount to card"""
    async with db.transaction():
        creating_income_card = await get_concrete_card(income_data.card_id, user, db)
        validate_creating_income_amount_currency(income_data, creating_income_card, user)
        created_income_id = await create_db_income(user, income_data, db)
        income_amount = income_data.user_currency_amount if not income_data.card_currency_amount else income_data.card_currency_amount
        plussed_card_amount = (
            creating_income_card.amount + income_amount
        )
        await update_card_amount(user.id, income_data.card_id, plussed_card_amount, db)

    created_income_scheme = IncomeOut(id=created_income_id, card=creating_income_card,
                                      **income_data.dict())
    return created_income_scheme
