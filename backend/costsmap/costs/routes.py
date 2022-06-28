from fastapi import APIRouter, Depends

from .schemas import CostOut, TotalCosts
from .dependencies import (
    get_all_costs_for_the_month, get_total_costs, create_new_cost,
    delete_cost_by_id
)


router = APIRouter()


@router.get('/', response_model=list[CostOut])
def all_costs(
    costs: list[CostOut] = Depends(get_all_costs_for_the_month)
):
    """Return all costs for the month"""
    return costs


@router.get('/total/', response_model=TotalCosts)
def total_costs(total_costs: TotalCosts = Depends(get_total_costs)):
    """Return total costs for the month"""
    return total_costs


@router.post('/', response_model=CostOut)
def create_cost(created_cost: CostOut = Depends(create_new_cost)):
    """Create a new cost for the user"""
    return created_cost


@router.delete('/{cost_id}/', status_code=204, dependencies=[Depends(delete_cost_by_id)])
def delete_cost():
    return
