import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet

from .costs import (
    GetCostsService, GetCostsTotalSumService, GetCostsForTheDateService
)
from ..serializers import CostSerializer


User = get_user_model()


class ListCostsCommand:
    """Base command to get list of costs"""

    get_service = None
    total_sum_service = GetCostsTotalSumService()
    serializer_class = CostSerializer

    def __init__(self, user: User):
        if not self.get_service:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have `get_service` attribute"
            )

        self._user = user
        self._service = self.get_service(user)

    def execute(self) -> dict:
        costs = self.get_costs()
        total_costs_sum = self.total_sum_service.execute(costs)
        serialized_costs = self.serializer_class(costs, many=True).data
        return {
            'total_sum': total_costs_sum, 'costs': serialized_costs
        }

    def get_costs(self):
        """Abstract method to get list of costs"""
        pass


class GetAllCostsCommand(ListCostsCommand):
    """Command to get all user costs"""

    get_service = GetCostsService

    def get_costs(self) -> QuerySet:
        return self._service.get_all()


class DateCostsListCommand(ListCostsCommand):
    """Base command for commands to get costs for the date"""

    get_service = GetCostsForTheDateService

    def __init__(self, user: User, date: datetime.date):
        super().__init__(user)
        self._date = date


class GetCostsForTheMonthCommand(DateCostsListCommand):
    """Command to get user costs for the concrete month"""

    def get_costs(self) -> QuerySet:
        return self._service.get_for_the_month(self._date)


class GetCostsForTheDateCommand(DateCostsListCommand):
    """Command to get user costs for the concrete year"""

    def get_costs(self) -> QuerySet:
        return self._service.get_for_the_date(self._date)
