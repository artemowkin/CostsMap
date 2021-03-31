import datetime

from django.contrib.auth import get_user_model

from services.commands import (
    GetStatisticBaseCommand, BaseGetForTheDateCommand
)
from .costs import (
    GetCostsTotalSumService, GetCostsForTheDateService, GetCostsService
)


User = get_user_model()


class GetCostsHistoryCommand:
    """Command to return costs history"""

    def __init__(self, user: User):
        self._user = user
        self._get_costs_service = GetCostsService(self._user)

    def execute(self) -> dict:
        all_costs = self._get_costs_service.get_all()
        total_sum = GetCostsTotalSumService.execute(all_costs)
        context = {
            'costs': all_costs,
            'total_sum': total_sum
        }
        return context


class GetCostsForTheDateCommand(BaseGetForTheDateCommand):
    """Command to return costs for the concrete date"""

    get_service_class = GetCostsForTheDateService
    total_sum_service_class = GetCostsTotalSumService
    context_object_name = 'costs'


class GetCostsStatisticCommand(GetStatisticBaseCommand):
    """Command to return costs statistic"""

    def get_dict_statistic(self):
        """Return costs statistic in dict format"""
        return {
            'costs': self.month_costs,
            'date': self.context_date,
            'total_sum': self.total_costs,
            'profit': self.profit,
            'average_costs': self.average_costs,
        }
