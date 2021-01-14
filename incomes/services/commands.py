import datetime

from django.contrib.auth import get_user_model

from costs.serializers import CostSerializer
from services.commands import GetStatisticBaseCommand
from .base import (
    GetIncomesService, GetIncomesTotalSumService, GetIncomesForTheDateService
)
from ..serializers import IncomeSerializer


User = get_user_model()


class GetIncomesHistoryCommand:
    """Command to return incomes history"""

    def __init__(self, user: User):
        self._user = user

    def execute(self) -> dict:
        all_incomes = GetIncomesService.get_all(self._user)
        total_sum = GetIncomesTotalSumService.execute(all_incomes)
        serializer = IncomeSerializer(all_incomes, many=True)
        context = {
            'incomes': serializer.data,
            'total_sum': total_sum
        }
        return context


class GetIncomesForTheDateCommand:
    """Command to return incomes for the concrete date"""

    def __init__(self, user: User, date: datetime.date):
        self._user = user
        self._date = date or datetime.date.today()

    def execute(self) -> dict:
        date_incomes = GetIncomesForTheDateService.get_for_the_date(
            self._user, self._date
        )
        total_sum = GetIncomesTotalSumService.execute(date_incomes)
        serializer = IncomeSerializer(date_incomes, many=True)
        context = {
            'incomes': serializer.data,
            'total_sum': total_sum,
            'date': self._date,
        }
        return context


class GetIncomesStatisticCommand(GetStatisticBaseCommand):
    """Command to return incomes statistic"""

    def get_dict_statistic(self):
        """Return incomes statistic in dict format"""
        income_serializer = IncomeSerializer(self.month_incomes, many=True)
        cost_serializer = CostSerializer(self.month_costs, many=True)
        return {
            'incomes': income_serializer.data,
            'costs': cost_serializer.data,
            'date': self._date,
            'total_sum': self.total_incomes,
            'profit': self.profit,
            'average_costs': self.average_costs,
        }
