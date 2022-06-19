from fastapi import APIRouter, Depends

from .schemas import IncomeOut, TotalIncomes
from .dependencies import (
    get_all_incomes_for_the_month, get_total_incomes
)


router = APIRouter()


@router.get('/', response_model=list[IncomeOut])
def all_incomes(
    incomes: list[IncomeOut] = Depends(get_all_incomes_for_the_month)
):
    """Return all incomes for the month (current by default)"""
    return incomes


@router.get('/total/', response_model=TotalIncomes)
def total_incomes(total_incomes: TotalIncomes = Depends(get_total_incomes)):
    """Return total incomes for the month"""
    return total_incomes
