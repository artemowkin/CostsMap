from fastapi import APIRouter, Depends

from .schemas import CostOut, TotalCosts
from .dependencies import (
    get_all_costs_for_the_month, get_total_costs
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
