from django.urls import reverse_lazy

from .forms import IncomeForm
from .models import Income
from .services.commands import GetIncomesStatisticCommand
import incomes.services as income_services
from utils.views import (
    DateGenericView, HistoryGenericView, StatisticPageGenericView,
    CreateGenericView, ChangeGenericView, DeleteGenericView
)


class IncomesForTheDateView(DateGenericView):
    """View to render user incomes for the date"""

    model = Income
    template_name = 'incomes/incomes.html'
    context_object_name = 'incomes'

    def get_total_sum(self, incomes):
        return income_services.get_total_sum(incomes)


class CreateIncomeView(CreateGenericView):
    """View to create a new income"""

    model = Income
    form_class = IncomeForm
    template_name = 'incomes/add_income.html'


class ChangeIncomeView(ChangeGenericView):
    """View to change an income"""

    model = Income
    form_class = IncomeForm
    template_name = 'incomes/change_income.html'
    context_object_name = 'income'


class DeleteIncomeView(DeleteGenericView):
    """View to delete an income"""

    model = Income
    template_name = 'incomes/delete_income.html'
    context_object_name = 'income'
    success_url = reverse_lazy('today_incomes')


class IncomesHistoryView(HistoryGenericView):
    """View to render all user incomes"""

    model = Income
    template_name = 'incomes/history_incomes.html'
    context_object_name = 'incomes'

    def get_total_sum(self, incomes):
        return income_services.get_total_sum(incomes)


class IncomesStatisticPageView(StatisticPageGenericView):
    """View to return statistic with user incomes for the month"""

    template_name = 'incomes/incomes_statistic.html'
    command = GetIncomesStatisticCommand
