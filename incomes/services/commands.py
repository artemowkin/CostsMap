import datetime

from django.contrib.auth import get_user_model

from services.commands import GetStatisticBaseCommand
from .base import (
    GetIncomesService, GetIncomesTotalSumService, GetIncomesForTheDateService
)
from utils.date import ContextDate


User = get_user_model()


class GetIncomesHistoryCommand:
    """Command to return incomes history"""

    def __init__(self, user: User):
        self._user = user

    def execute(self) -> dict:
        all_incomes = GetIncomesService.get_all(self._user)
        total_sum = GetIncomesTotalSumService.execute(all_incomes)
        context = {
            'incomes': all_incomes,
            'total_sum': total_sum
        }
        return context


class GetIncomesForTheDateCommand:
    """Command to return incomes for the concrete date"""

    def __init__(self, user: User, date: datetime.date):
        self._user = user
        self._date = date

    def execute(self) -> dict:
        context_date = ContextDate(self._date)
        date_incomes = GetIncomesForTheDateService.get_for_the_date(
            self._user, self._date
        )
        total_sum = GetIncomesTotalSumService.execute(date_incomes)
        context = {
            'incomes': date_incomes,
            'total_sum': total_sum,
            'date': context_date,
        }
        return context


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
