from fastapi import APIRouter, Depends

from ..schemas.costs import Cost, CostOut
from ..dependencies.costs import (
    get_all_costs_for_the_month
)


router = APIRouter()


@router.get('/', response_model=list[CostOut])
def all_costs(
    costs: list[CostOut] = Depends(get_all_costs_for_the_month)
):
    """Return all costs for the month"""
    return costs
