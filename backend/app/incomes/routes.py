from uuid import UUID

from fastapi import APIRouter, Depends, Query

from .models import Income
from .dependencies import use_incomes_set
from .services import IncomesSet
from .schemas import IncomeIn
from ..utils.dates import get_current_month


router = APIRouter()

income_response_schema = Income.get_pydantic(exclude={'owner', 'card__owner'})


@router.get('/', response_model=list[income_response_schema])
async def all_incomes(month: str | None = Query(None, regex=r"\d{4}-\d{2}"), incomes_set: IncomesSet = Depends(use_incomes_set)):
    """Returns all current user incomes for the month"""
    month = month if month else get_current_month()
    incomes = await incomes_set.all(month)
    return incomes


@router.post('/', response_model=income_response_schema)
async def new_income(income_data: IncomeIn, incomes_set: IncomesSet = Depends(use_incomes_set)):
    """Creates new income for current user"""
    income = await incomes_set.create(income_data)
    return income


@router.delete('/{income_uuid}/', status_code=204)
async def delete_income(income_uuid: UUID, incomes_set: IncomesSet = Depends(use_incomes_set)):
    """Deletes concrete income for current user"""
    income = await incomes_set.get_concrete(str(income_uuid))
    await incomes_set.delete(income)


@router.put('/{income_uuid}/', response_model=income_response_schema)
async def update_income(income_uuid: UUID, income_data: IncomeIn, incomes_set: IncomesSet = Depends(use_incomes_set)):
    """Updates concrete income for current user"""
    income = await incomes_set.get_concrete(str(income_uuid))
    await incomes_set.update(income, income_data)
