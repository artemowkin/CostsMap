from fastapi import APIRouter, Depends

from ..accounts.schemas import LoginRequiredResponse
from ..cards.schemas import Card404Error
from .schemas import IncomeOut, TotalIncomes, Income404Error, CreateIncome400Error
from .dependencies import (
    GetAllIncomesCommand, get_total_incomes,
    CreateIncomeCommand, DeleteIncomeCommand
)


router = APIRouter()


@router.get('/', response_model=list[IncomeOut], responses={
    401: {"model": LoginRequiredResponse},
})
def all_incomes(
    incomes: list[IncomeOut] = Depends(GetAllIncomesCommand())
):
    """Return all incomes for the month (current by default)"""
    return incomes


@router.get('/total/', response_model=TotalIncomes, responses={
    401: {"model": LoginRequiredResponse},
})
def total_incomes(total_incomes: TotalIncomes = Depends(get_total_incomes)):
    """Return total incomes for the month"""
    return total_incomes


@router.post('/', response_model=IncomeOut, status_code=201, responses={
    401: {"model": LoginRequiredResponse},
    400: {"model": CreateIncome400Error},
    404: {"model": Card404Error},
})
def create_income(created_income: IncomeOut = Depends(CreateIncomeCommand())):
    """Create a new income for the user"""
    return created_income


@router.delete('/{operation_id}/', status_code=204, dependencies=[Depends(DeleteIncomeCommand())], responses={
    401: {"model": LoginRequiredResponse},
    404: {"model": Income404Error},
})
def delete_income():
    pass
