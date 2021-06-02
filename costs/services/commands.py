import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet

from services.commands import ListEntriesCommand, DateEntriesListCommand
from .base import (
    GetCostsService, GetCostsTotalSumService, GetCostsForTheDateService
)
from ..serializers import CostSerializer


User = get_user_model()


class CostsListMixin:
    """Mixin with costs class attributes"""

    total_sum_service = GetCostsTotalSumService()
    serializer_class = CostSerializer
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
