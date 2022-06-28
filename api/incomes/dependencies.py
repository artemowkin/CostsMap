from datetime import date

from fastapi import Depends, Query

from project.models import database
from accounts.models import Users
from accounts.dependencies import get_current_user
from cards.services import update_card_amount, get_concrete_user_card
from .services import (
    get_all_user_incomes_by_month, get_total_incomes_for_the_month,
    create_db_income, validate_creating_income_amount_currency
)
from .schemas import IncomeOut, TotalIncomes, Income, IncomeOut


today_string = date.today().strftime("%Y-%m")


async def get_all_incomes_for_the_month(
    month: str = Query(today_string, regex=r"\d{4}-\d{2}"),
    user: Users = Depends(get_current_user)
) -> list[IncomeOut]:
    """Return all incomes for the month (current by default)"""
    db_incomes = await get_all_user_incomes_by_month(user.id, month)
    out_incomes = [IncomeOut.from_orm(db_income) for db_income in db_incomes]
    return out_incomes


async def get_total_incomes(
    month: str = Query(today_string, regex=r"\d{4}-\d{2}"),
    user: Users = Depends(get_current_user)
):
    """Return total incomes for the month for concrete user"""
    total_incomes = await get_total_incomes_for_the_month(user.id, month)
    return TotalIncomes(total_incomes=total_incomes)


async def create_new_income(
    income_data: Income,
    user: Users = Depends(get_current_user)
):
    """Create new income and plus income amount to card"""
    async with database.transaction():
        creating_income_card = await get_concrete_user_card(income_data.card_id, user.id)
        validate_creating_income_amount_currency(income_data, creating_income_card, user)
        created_income = await create_db_income(user, creating_income_card, income_data)
        income_amount = income_data.user_currency_amount if not income_data.card_currency_amount else income_data.card_currency_amount
        plussed_card_amount = (
            creating_income_card.amount + income_amount
        )
        await update_card_amount(user.id, income_data.card_id, plussed_card_amount)

    created_income_scheme = IncomeOut.from_orm(created_income)
    return created_income_scheme
