from fastapi import APIRouter, Depends, Query

from .dependencies import use_incomes_set, valid_income_uuid
from .services import IncomesSet
from .schemas import IncomeIn, IncomeOut
from .models import Income
from ..utils.dates import get_current_month


router = APIRouter()


@router.get('/', response_model=list[IncomeOut])
async def all_incomes(
    month: str | None = Query(None, regex=r"\d{4}-\d{2}"),
    incomes_set: IncomesSet = Depends(use_incomes_set)
):
    """Returns all current user incomes for the month"""
    month = month if month else get_current_month()
    incomes = await incomes_set.all(month)
    return [IncomeOut.from_orm(income) for income in incomes]


@router.post('/', response_model=IncomeOut)
async def new_income(income_data: IncomeIn, incomes_set: IncomesSet = Depends(use_incomes_set)):
    """Creates new income for current user"""
    income = await incomes_set.create(income_data)
    return IncomeOut.from_orm(income)


@router.delete('/{income_uuid}/', status_code=204)
async def delete_income(
    income: Income = Depends(valid_income_uuid),
    incomes_set: IncomesSet = Depends(use_incomes_set)
):
    """Deletes concrete income for current user"""
    await incomes_set.delete(income)


@router.put('/{income_uuid}/', response_model=IncomeOut)
async def update_income(
    income_data: IncomeIn,
    income: Income = Depends(valid_income_uuid),
    incomes_set: IncomesSet = Depends(use_incomes_set)
):
    """Updates concrete income for current user"""
    updated_income = await incomes_set.update(income, income_data)
    return IncomeOut.from_orm(updated_income)
