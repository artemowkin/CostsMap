import datetime

from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from services.commands import GetStatisticBaseCommand
from .categories import GetCategoriesService, get_category_costs
from ..serializers import CostSerializer
from .costs import (
    GetCostsTotalSumService, GetCostsForTheDateService, GetCostsService
)


User = get_user_model()


class GetCostsHistoryCommand:
    """Command to return costs history"""

    def __init__(self, user: User):
        self._user = user

    def execute(self) -> dict:
        all_costs = GetCostsService.get_all(self._user)
        total_sum = GetCostsTotalSumService.execute(all_costs)
        serializer = CostSerializer(all_costs, many=True)
        context = {
            'costs': serializer.data,
            'total_sum': total_sum
        }
        return context


class GetCostsForTheDateCommand:
    """Command to return costs for the concrete date"""

    def __init__(self, user: User, date: datetime.date):
        self._user = user
        self._date = date or datetime.date.today()

    def execute(self):
        date_costs = GetCostsForTheDateService.get_for_the_date(
            self._user, self._date
        )
        total_sum = GetCostsTotalSumService.execute(date_costs)
        serializer = CostSerializer(date_costs, many=True)
        context = {
            'costs': serializer.data,
            'total_sum': total_sum,
            'date': self._date,
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
        serializer = CostSerializer(costs, many=True)
        data = {
            'category': category.title,
            'total_sum': total_sum,
            'costs': serializer.data
        }
        return data


class GetCostsStatisticCommand(GetStatisticBaseCommand):
    """Command to return costs statistic"""

    def get_dict_statistic(self):
        """Return costs statistic in dict format"""
        serializer = CostSerializer(self.month_costs, many=True)
        return {
            'costs': serializer.data,
            'date': self._date,
            'total_sum': self.total_costs,
            'profit': self.profit,
            'average_costs': self.average_costs,
        }
