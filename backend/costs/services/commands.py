from django.db.models import QuerySet

from services.commands import ListEntriesCommand, DateEntriesListCommand
from .base import (
    GetCostsService, GetCostsTotalSumService, GetCostsForTheDateService
)
from ..serializers import ImmutableCostSerializer


class CostsListMixin:
    """Mixin with costs class attributes"""

    total_sum_service = GetCostsTotalSumService()
    serializer_class = ImmutableCostSerializer
    queryset_name = 'costs'


class GetAllCostsCommand(CostsListMixin, ListEntriesCommand):
    """Command to get all user costs"""

    get_service = GetCostsService


class GetCostsForTheMonthCommand(CostsListMixin, DateEntriesListCommand):
    """Command to get user costs for the concrete month"""

    get_service = GetCostsForTheDateService

    def get_entries(self) -> QuerySet:
        return self._service.get_for_the_month(self._date)


class GetCostsForTheDateCommand(CostsListMixin, DateEntriesListCommand):
    """Command to get user costs for the concrete date"""

    get_service = GetCostsForTheDateService

    def get_entries(self) -> QuerySet:
        return self._service.get_for_the_date(self._date)
