import datetime

from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from services.commands import GetStatisticBaseCommand
from .categories import GetCategoriesService, get_category_costs
from .costs import (
    GetCostsTotalSumService, GetCostsForTheDateService, GetCostsService
)

from utils.date import ContextDate


User = get_user_model()


class GetCostsHistoryCommand:
    """Command to return costs history"""

    def __init__(self, user: User):
        self._user = user

    def execute(self) -> dict:
        all_costs = GetCostsService.get_all(self._user)
        total_sum = GetCostsTotalSumService.execute(all_costs)
        context = {
            'costs': all_costs,
            'total_sum': total_sum
        }
        return context


class GetCostsForTheDateCommand:
    """Command to return costs for the concrete date"""

    def __init__(self, user: User, date: datetime.date):
        self._user = user
        self._date = date

    def execute(self):
        context_date = ContextDate(self._date)
        date_costs = GetCostsForTheDateService.get_for_the_date(
            self._user, self._date
        )
        total_sum = GetCostsTotalSumService.execute(date_costs)
        context = {
            'costs': date_costs,
            'total_sum': total_sum,
            'date': context_date,
        }
        return context


class GetCategoryCostsCommand:
    """Command to return category costs"""

    def __init__(self, category_pk, user):
        self._category_pk = category_pk
        self._user = user

    def execute(self) -> dict:
        """Return category costs, costs total sum and category itself
        in dict format
        """
        category = GetCategoriesService.get_concrete(
            self._category_pk, self._user
        )
        costs = get_category_costs(category)
        total_sum = GetCostsTotalSumService.execute(costs)
        return {'costs': costs, 'category': category, 'total_sum': total_sum}


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
