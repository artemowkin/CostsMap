from fastapi import APIRouter, Depends

from .schemas import IncomeOut, TotalIncomes
from .dependencies import (
    GetAllIncomesCommand, get_total_incomes,
    CreateIncomeCommand, DeleteIncomeCommand
)


router = APIRouter()


@router.get('/', response_model=list[IncomeOut])
def all_incomes(
    incomes: list[IncomeOut] = Depends(GetAllIncomesCommand())
):
    """Return all incomes for the month (current by default)"""
    return incomes


@router.get('/total/', response_model=TotalIncomes)
def total_incomes(total_incomes: TotalIncomes = Depends(get_total_incomes)):
    """Return total incomes for the month"""
    return total_incomes


@router.post('/', response_model=IncomeOut, status_code=201)
def create_income(created_income: IncomeOut = Depends(CreateIncomeCommand())):
    """Create a new income for the user"""
    return created_income


@router.delete('/{operation_id}/', status_code=204, dependencies=[Depends(DeleteIncomeCommand())])
def delete_cost():
    pass
