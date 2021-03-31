import datetime

from django.contrib.auth import get_user_model

from services.commands import (
    GetStatisticBaseCommand, BaseGetForTheDateCommand
)
from .base import (
    GetIncomesService, GetIncomesTotalSumService, GetIncomesForTheDateService
)
from utils.date import ContextDate


User = get_user_model()


class GetIncomesHistoryCommand:
    """Command to return incomes history"""

    def __init__(self, user: User):
        self._user = user
        self._get_service = GetIncomesService(user)

    def execute(self) -> dict:
        all_incomes = self._get_service.get_all()
        total_incomes_service = GetIncomesTotalSumService()
        total_sum = total_incomes_service.execute(all_incomes)
        context = {
            'incomes': all_incomes,
            'total_sum': total_sum
        }
        return context


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
