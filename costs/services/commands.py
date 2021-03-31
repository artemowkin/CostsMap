import datetime

from django.contrib.auth import get_user_model

from services.commands import (
    GetStatisticBaseCommand, BaseGetForTheDateCommand, BaseGetHistoryCommand
)
from .costs import (
    GetCostsTotalSumService, GetCostsForTheDateService, GetCostsService
)


User = get_user_model()


class GetCostsHistoryCommand(BaseGetHistoryCommand):
    """Command to return costs history"""

    get_service_class = GetCostsService
    total_sum_service_class = GetCostsTotalSumService
    context_object_name = 'costs'


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
