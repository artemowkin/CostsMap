from uuid import UUID

from fastapi import APIRouter, Depends, Query

from .models import Cost
from .dependencies import use_costs_set
from .services import CostsSet
from .schemas import CostIn
from ..utils.dates import get_current_month


router = APIRouter()


cost_response_schema = Cost.get_pydantic(exclude={'owner', 'card__owner', 'category__owner'})


@router.get('/', response_model=list[cost_response_schema])
async def all_costs(month: str | None = Query(None, regex=r"\d{4}-\d{2}"), costs_set: CostsSet = Depends(use_costs_set)):
    """Returns all current user costs for the month"""
    month = month if month else get_current_month()
    costs = await costs_set.all(month)
    return costs


@router.post('/', response_model=cost_response_schema)
async def new_cost(cost_data: CostIn, costs_set: CostsSet = Depends(use_costs_set)):
    """Creates new cost for current user"""
    cost = await costs_set.create(cost_data)
    return cost


@router.delete('/{cost_uuid}/', status_code=204)
async def delete_cost(cost_uuid: UUID, costs_set: CostsSet = Depends(use_costs_set)):
    """Deletes concrete cost for current user by uuid"""
    cost = await costs_set.get_concrete(str(cost_uuid))
    await costs_set.delete(cost)


@router.put('/{cost_uuid}/', response_model=cost_response_schema)
async def update_cost(cost_uuid: UUID, cost_data: CostIn, costs_set: CostsSet = Depends(use_costs_set)):
    """Updates concrete cost for current user by uuid using data from request"""
    cost = await costs_set.get_concrete(str(cost_uuid))
    await costs_set.update(cost, cost_data)
