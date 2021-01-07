import datetime

from django.contrib.auth import get_user_model

from utils.date import MonthContextDate
from costs.services.costs import CostService
from incomes.services import IncomeService


User = get_user_model()


class GetStatisticBaseCommand:
    """Base command to return statistic"""

    def __init__(
            self, cost_service: CostService,
            income_service: IncomeService, user: User, date: datetime.date):
        self._cost_service = cost_service
        self._income_service = income_service
        self._user = user
        self._date = date

    def get_dict_statistic(self) -> dict:
        """Return statistic in dict format. This method must
        be overwritten
        """
        raise NotImplementedError

    def execute(self) -> dict:
        """Return costs statistic in context dict format"""
        self.context_date = MonthContextDate(self._date)
        self.month_costs = self._cost_service.get_for_the_month(
            self._user, self._date
        )
        self.month_incomes = self._income_service.get_for_the_month(
            self._user, self._date
        )
        self.total_costs = self._cost_service.get_total_sum(self.month_costs)
        self.total_incomes = self._income_service.get_total_sum(
            self.month_incomes
        )
        self.profit = self.total_incomes - self.total_costs
        self.average_costs = self._cost_service.get_average_costs_for_the_day(
            self._user
        )
        return self.get_dict_statistic()
