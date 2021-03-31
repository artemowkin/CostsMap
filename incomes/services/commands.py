import datetime

from django.contrib.auth import get_user_model

from services.commands import (
    GetStatisticBaseCommand, BaseGetForTheDateCommand, BaseGetHistoryCommand
)
from .base import (
    GetIncomesService, GetIncomesTotalSumService, GetIncomesForTheDateService
)
from utils.date import ContextDate


User = get_user_model()


class GetIncomesHistoryCommand(BaseGetHistoryCommand):
    """Command to return incomes history"""

    get_service_class = GetIncomesService
    total_sum_service_class = GetIncomesTotalSumService
    context_object_name = 'incomes'


class GetIncomesForTheDateCommand(BaseGetForTheDateCommand):
    """Command to return incomes for the concrete date"""

    get_service_class = GetIncomesForTheDateService
    total_sum_service_class = GetIncomesTotalSumService
    context_object_name = 'incomes'


class GetIncomesStatisticCommand(GetStatisticBaseCommand):
    """Command to return incomes statistic"""

    def get_dict_statistic(self):
        """Return incomes statistic in dict format"""
        return {
            'incomes': self.month_incomes,
            'costs': self.month_costs,
            'date': self.context_date,
            'total_sum': self.total_incomes,
            'profit': self.profit,
            'average_costs': self.average_costs,
        }
