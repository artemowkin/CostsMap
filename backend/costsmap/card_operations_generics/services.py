from decimal import Decimal
from datetime import date
from abc import ABC, abstractmethod

from orm import Model, NoMatch
from fastapi import HTTPException
from dateutil.relativedelta import relativedelta

from ..project.models import database
from .models import CardOperationNamedTuple


class CardOperationGetter(ABC):
    """Abstract generic card operation class with get operations"""

    def __init__(self, user_id: int):
        self._user_id = user_id
        self._model = self._get_model()

    @abstractmethod
    def _get_model(self) -> type[Model]:
        """Return card operation model"""
        pass

    async def get_all_for_the_month(self, month: str) -> list[CardOperationNamedTuple]:
        """Return all card operations"""
        month_start_date = date.fromisoformat(month + '-01')
        month_end_date = month_start_date + relativedelta(months=1)
        db_operations = await self._model.objects.filter(
            user__id=self._user_id, date__gte=month_start_date, date__lt=month_end_date
        ).order_by('-date').all()
        return db_operations

    async def get_concrete(self, operation_id: int) -> CardOperationNamedTuple:
        """Return the concrete user card operation id"""
        try:
            db_operation = await self._model.objects.get(id=operation_id, user__id=self._user_id)
            return db_operation
        except NoMatch:
            raise HTTPException(
                status_code=404, detail=f"{self._model.__name__} with this id doesn't exist"
            )

    async def get_total_for_the_month(self, month: str) -> Decimal:
        """Return total card operations sum for the month"""
        month_start_date = date.fromisoformat(month + '-01')
        month_end_date = month_start_date + relativedelta(months=1)
        query = self._get_total_sum_query()
        total_sum = await database.fetch_val(query, {
            'user_id': self._user_id, 'start_date': month_start_date, 'end_date': month_end_date
        })
        return Decimal(total_sum or 0)

    @abstractmethod
    def _get_total_sum_query(self) -> str:
        """Return query string to get total sum for card operations"""
        pass
