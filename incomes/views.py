from django.urls import reverse_lazy

from costs.services.costs import CostService
from .forms import IncomeForm
from .services import IncomeService
from .services.commands import GetIncomesStatisticCommand
from utils.views import (
    DateGenericView, HistoryGenericView, StatisticPageGenericView,
    CreateGenericView, ChangeGenericView, DeleteGenericView
)


class IncomesForTheDateView(DateGenericView):
    """View to render user incomes for the date"""

    service = IncomeService()
    template_name = 'incomes/incomes.html'
    context_object_name = 'incomes'


class CreateIncomeView(CreateGenericView):
    """View to create a new income"""

    form_class = IncomeForm
    template_name = 'incomes/add_income.html'
    service = IncomeService()


class ChangeIncomeView(ChangeGenericView):
    """View to change an income"""

    service = IncomeService()
    form_class = IncomeForm
    template_name = 'incomes/change_income.html'
    context_object_name = 'income'


class DeleteIncomeView(DeleteGenericView):
    """View to delete an income"""

    template_name = 'incomes/delete_income.html'
    success_url = reverse_lazy('today_incomes')
    service = IncomeService()


class IncomesHistoryView(HistoryGenericView):
    """View to render all user incomes"""

    service = IncomeService()
    template_name = 'incomes/history_incomes.html'
    context_object_name = 'incomes'


class IncomesStatisticPageView(StatisticPageGenericView):
    """View to return statistic with user incomes for the month"""

    template_name = 'incomes/incomes_statistic.html'
    cost_service = CostService()
    income_service = IncomeService()
    command = GetIncomesStatisticCommand
