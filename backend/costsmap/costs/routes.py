from fastapi import APIRouter, Depends

from .schemas import CostOut, TotalCosts
from .dependencies import (
    GetAllCostsCommand, get_total_costs, CreateCostCommand,
    DeleteCostCommand
)


router = APIRouter()


@router.get('/', response_model=list[CostOut])
def all_costs(
    costs: list[CostOut] = Depends(GetAllCostsCommand())
):
    """Return all costs for the month"""
    return costs


@router.get('/total/', response_model=TotalCosts)
def total_costs(total_costs: TotalCosts = Depends(get_total_costs)):
    """Return total costs for the month"""
    return total_costs


@router.post('/', response_model=CostOut, status_code=201)
def create_cost(created_cost: CostOut = Depends(CreateCostCommand())):
    """Create a new cost for the user"""
    return created_cost


@router.delete('/{operation_id}/', status_code=204, dependencies=[Depends(DeleteCostCommand())])
def delete_cost():
    return
