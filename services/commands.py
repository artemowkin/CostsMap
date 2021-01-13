import datetime

from django.contrib.auth import get_user_model

from utils.date import MonthContextDate
import costs.services as cost_services
import incomes.services as income_services


User = get_user_model()


class GetStatisticBaseCommand:
    """Base command to return statistic"""

    def __init__(self, user: User, date: datetime.date):
        self._user = user
        self._date = date
        self._cost_date_service = cost_services.GetCostsForTheDateService
        self._income_date_service = income_services.GetIncomesForTheDateService

    def get_dict_statistic(self) -> dict:
        """Return statistic in dict format. This method must
        be overwritten
        """
        raise NotImplementedError

    def execute(self) -> dict:
        """Return costs statistic in context dict format"""
        self.context_date = MonthContextDate(self._date)
        self.month_costs = self._cost_date_service.get_for_the_month(
            self._user, self._date
        )
        self.month_incomes = self._income_date_service.get_for_the_month(
            self._user, self._date
        )
        self.total_costs = cost_services.GetCostsTotalSumService.execute(
            self.month_costs
        )
        self.total_incomes = income_services.GetIncomesTotalSumService.execute(
            self.month_incomes
        )
        self.profit = self.total_incomes - self.total_costs
        self.average_costs = (
            cost_services.GetAverageCostsForTheDayService.execute({
                'user': self._user
            })
        )
        return self.get_dict_statistic()
