from fastapi import HTTPException

from ..cards.models import CardNamedTuple
from ..accounts.models import UserNamedTuple
from .schemas import IncomeIn
from .models import Incomes, IncomeNamedTuple
from ..card_operations_generics.services import CardOperationGetter


class IncomesGetter(CardOperationGetter):
    """Service with get incomes operations"""

    def _get_model(self) -> type[Incomes]:
        """Return income model"""
        return Incomes

    def _get_total_sum_query(self) -> str:
        """Return query string to get total incomes sum"""
        return (
            "select sum(user_currency_amount) as total_incomes from incomes where "
            "user_id = :user_id and date >= date(:start_date) and date < date(:end_date);"
        )


async def create_db_income(user: UserNamedTuple, card: CardNamedTuple, income_data: IncomeIn) -> IncomeNamedTuple:
    """Create new income for the user and return created income id"""
    created_income = await Incomes.objects.create(**income_data.dict(), user=user, card=card)
    return created_income


async def delete_db_income(income) -> None:
    """Delete the concrete user income by id"""
    await income.delete()


def validate_creating_income_amount_currency(income_data: IncomeIn, income_card: CardNamedTuple, user: UserNamedTuple):
    """
    Validate income amount currency: if card and user currencies are differrent,
    income must contain card_currency_amount field
    """
    if income_card.currency != user.currency and income_data.card_currency_amount is None:
        err_msg = "Income for card with differrent currency than default must contain `card_currency_amount` field"
        raise HTTPException(status_code=400, detail=err_msg)
