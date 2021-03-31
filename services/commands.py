import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured

from utils.date import MonthContextDate, ContextDate
import costs.services as cost_services
import incomes.services as income_services


User = get_user_model()


class GetStatisticBaseCommand:
    """Base command to return statistic"""

    def __init__(self, user: User, date: datetime.date):
        self._user = user
        self._date = date
        self._cost_date_service = cost_services.GetCostsForTheDateService(
            user
        )
        self._income_date_service = income_services.GetIncomesForTheDateService(
            user
        )

    def get_dict_statistic(self) -> dict:
        """Return statistic in dict format. This method must
        be overwritten
        """
        raise NotImplementedError

    def execute(self) -> dict:
        """Return costs statistic in context dict format"""
        self.context_date = MonthContextDate(self._date)
        self.month_costs = self._cost_date_service.get_for_the_month(
            self._date
        )
        self.month_incomes = self._income_date_service.get_for_the_month(
            self._date
        )
        total_costs_service = cost_services.GetCostsTotalSumService()
        total_incomes_service = income_services.GetIncomesTotalSumService()
        self.total_costs = total_costs_service.execute(self.month_costs)
        self.total_incomes = total_incomes_service.execute(self.month_incomes)
        self.profit = self.total_incomes - self.total_costs
        self.average_costs = (
            cost_services.GetAverageCostsForTheDayService.execute({
                'user': self._user
            })
        )
        return self.get_dict_statistic()


class BaseGetForTheDateCommand:
    """Base class for commands to get model entries for the date"""

    get_service_class = None
    total_sum_service_class = None
    context_object_name = 'object_list'

    def __init__(self, user: User, date: datetime.date):
        if not self.get_service_class:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must include "
                "`get_service_class` attribute"
            )

        if not self.total_sum_service_class:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must include "
                "`total_sum_service_class` attribute"
            )

        self._user = user
        self._date = date
        self._get_service = self.get_service_class(self._user)
        self._total_sum_service = self.total_sum_service_class()

    def execute(self):
        context_date = ContextDate
        date_entries = self._get_service.get_for_the_date(self._date)
        total_sum = self._total_sum_service.execute(date_entries)
        context = {
            self.context_object_name: date_entries,
            'total_sum': total_sum,
            'date': context_date
        }
        return context
