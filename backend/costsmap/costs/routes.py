from fastapi import APIRouter, Depends

from ..accounts.schemas import LoginRequiredResponse
from ..cards.schemas import Card404Error
from .schemas import CostOut, TotalCosts, CreateCost400Error, Cost404Error
from .dependencies import (
    GetAllCostsCommand, get_total_costs, CreateCostCommand,
    DeleteCostCommand
)


router = APIRouter()


@router.get('/', response_model=list[CostOut], responses={
    401: {"model": LoginRequiredResponse},
})
def all_costs(
    costs: list[CostOut] = Depends(GetAllCostsCommand())
):
    """Return all costs for the month"""
    return costs


@router.get('/total/', response_model=TotalCosts, responses={
    401: {"model": LoginRequiredResponse},
})
def total_costs(total_costs: TotalCosts = Depends(get_total_costs)):
    """Return total costs for the month"""
    return total_costs


@router.post('/', response_model=CostOut, status_code=201, responses={
    401: {"model": LoginRequiredResponse},
    400: {"model": CreateCost400Error},
    404: {"model": Card404Error},
})
def create_cost(created_cost: CostOut = Depends(CreateCostCommand())):
    """Create a new cost for the user"""
    return created_cost


@router.delete('/{operation_id}/', status_code=204, dependencies=[Depends(DeleteCostCommand())], responses={
    401: {"model": LoginRequiredResponse},
    404: {"model": Cost404Error}
})
def delete_cost():
    return
