from decimal import Decimal
from datetime import date

from fastapi import HTTPException
from dateutil.relativedelta import relativedelta

from project.models import database
from cards.models import Cards
from accounts.models import Users
from .schemas import Income
from .models import Incomes


async def get_all_user_incomes_by_month(user_id: int, month: str) -> list[Incomes]:
    """Return all user incomes for the month"""
    month_start_date = date.fromisoformat(month + '-01')
    month_end_date = month_start_date + relativedelta(months=1)
    db_incomes = await Incomes.objects.filter(
        user__id=user_id, date__gte=month_start_date, date__lt=month_end_date
    ).order_by('-date').all()
    return db_incomes


async def get_total_incomes_for_the_month(user_id: int, month: str) -> Decimal:
    """Return total incomes for the month"""
    month_start_date = date.fromisoformat(month + '-01')
    month_end_date = month_start_date + relativedelta(months=1)
    query = (
        "select sum(user_currency_amount) as total_incomes from incomes where "
        "user_id = :user_id and date >= date(:start_date) and date < date(:end_date);"
    )
    total_incomes = await database.fetch_val(query, {
        'user_id': user_id, 'start_date': month_start_date, 'end_date': month_end_date
    })
    return Decimal(total_incomes or 0)


async def create_db_income(user: Users, card: Cards, income_data: Income) -> Incomes:
    """Create new income for the user and return created income id"""
    created_income = await Incomes.objects.create(**income_data.dict(), user=user, card=card)
    return created_income


def validate_creating_income_amount_currency(income_data: Income, income_card: Cards, user: Users):
    """
    Validate income amount currency: if card and user currencies are differrent,
    income must contain card_currency_amount field
    """
    if income_card.currency != user.currency and income_data.card_currency_amount is None:
        err_msg = "Income for card with differrent currency than default must contain `card_currency_amount field`"
        raise HTTPException(status_code=400, detail=err_msg)
