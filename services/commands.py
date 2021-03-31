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
            user, date
        )
        self._income_date_service = income_services.GetIncomesForTheDateService(
            user, date
        )

    def get_dict_statistic(self) -> dict:
        """Return statistic in dict format. This method must
        be overwritten
        """
        raise NotImplementedError

    def execute(self) -> dict:
        """Return costs statistic in context dict format"""
        self.context_date = MonthContextDate(self._date)
        self.month_costs = self._cost_date_service.get_for_the_month()
        self.month_incomes = self._income_date_service.get_for_the_month()
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
        self._service = self.get_service_class(self._user, self._date)

    def execute(self):
        context_date = ContextDate
        date_entries = self._service.get_for_the_date()
        total_sum = self.total_sum_service_class.execute(date_entries)
        context = {
            self.context_object_name: date_entries,
            'total_sum': total_sum,
            'date': context_date
        }
        return context
