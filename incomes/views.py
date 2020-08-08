"""Module with incomes views"""

from utils.views import (
    DateView,
    HistoryView,
    CreateView,
    ChangeView,
    DeleteView,
    StatisticPageView
)
from costs.services import CostService

from .services import IncomeService


class IncomesForTheDateView(DateView):

    """View to return incomes for the date

    Attributes
    ----------
    service : Service
        Income's service

    template_name : str
        Template to display income's for the date

    context_object_name : str
        Name of incomes in template

    """

    service = IncomeService()
    template_name = 'costs/incomes.html'
    context_object_name = 'incomes'


class CreateIncomeView(CreateView):

    """View to create a new income

    Attributes
    ----------
    service : Service
        Income's service

    template_name : str
        Template with form to create an income

    """

    service = IncomeService()
    template_name = 'costs/add_income.html'


class ChangeIncomeView(ChangeView):

    """View to change an income

    Attributes
    ----------
    service : Service
        Income's service

    template_name : str
        Template with form to change an income

    context_object_name : str
        Name of income object in template

    """

    service = IncomeService()
    template_name = 'costs/change_income.html'
    context_object_name = 'income'


class DeleteIncomeView(DeleteView):

    """View to delete an income

    Attributes
    ----------
    service : Service
        Income's service

    template_name : str
        Template with form to delete an income

    context_object_name : str
        Name of income object in template

    """

    service = IncomeService()
    template_name = 'costs/delete_income.html'
    context_object_name = 'income'


class IncomesHistoryView(HistoryView):

    """View to return all incomes for all time.

    Attributes
    ----------
    service : Service
        Income service

    template_name : str
        Template to display history of incomes

    context_object_name : str
        Name of incomes in template

    """

    service = IncomeService()
    template_name = 'costs/history_incomes.html'
    context_object_name = 'incomes'


class IncomesStatisticPageView(StatisticPageView):

    """View to return statistic with incomes for the month.

    Attributes
    ----------
    service : Service
        Income's service

    cost_service : Service
        Cost's service

    template_name : str
        Template to display statistic with incomes

    context_object_name : str
        Name of incomes in template

    """

    service = IncomeService()
    cost_service = CostService()
    template_name = 'costs/incomes_statistic.html'
    context_object_name = 'incomes'

    def get_context(self, request, date, *args, **kwargs):
        """Return context with costs"""
        context = super().get_context(request, date, *args, **kwargs)
        costs = self.cost_service.get_for_the_month(
            owner=request.user, date=date
        )
        context.update({'costs': costs})
        return context

