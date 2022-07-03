from fastapi import APIRouter, Depends

from .schemas import IncomeOut, TotalIncomes
from .dependencies import (
    get_all_incomes_for_the_month, get_total_incomes,
    create_new_income, delete_income_by_id
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


@router.post('/', response_model=IncomeOut)
def create_income(created_income: IncomeOut = Depends(create_new_income)):
    """Create a new income for the user"""
    return created_income


@router.delete('/{income_id}/', status_code=204, dependencies=[Depends(delete_income_by_id)])
def delete_cost():
    pass
