import datetime

from django.views.generic import CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse
from django.forms import Form
from django.shortcuts import get_object_or_404

from costs.models import Cost
from .models import Income
from .forms import IncomeForm
import services.common as services_common
from utils.views import (
    DateGenericView, HistoryGenericView, StatisticPageGenericView,
    GetUserObjectMixin
)


class IncomesForTheDateView(DateGenericView):
    """View to render user incomes for the date

    Attributes
    ----------
    model : Type[Model]
        Income model
    template_name : str
        Template to display incomes for the date
    context_object_name : str
        Name of incomes queryset in template

    """

    model = Income
    template_name = 'incomes/incomes.html'
    context_object_name = 'incomes'


class CreateIncomeView(LoginRequiredMixin, CreateView):
    """View to create a new income"""

    model = Income
    form_class = IncomeForm
    template_name = 'incomes/add_income.html'
    login_url = reverse_lazy('account_login')

    def form_valid(self, form: Form) -> HttpResponse:
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ChangeIncomeView(LoginRequiredMixin, GetUserObjectMixin, UpdateView):
    """View to change an income"""

    model = Income
    form_class = IncomeForm
    template_name = 'incomes/change_income.html'
    context_object_name = 'income'
    login_url = reverse_lazy('account_login')


class DeleteIncomeView(LoginRequiredMixin, GetUserObjectMixin, DeleteView):
    """View to delete an income"""

    model = Income
    template_name = 'incomes/delete_income.html'
    context_object_name = 'income'
    success_url = reverse_lazy('today_incomes')
    login_url = reverse_lazy('account_login')


class IncomesHistoryView(HistoryGenericView):
    """View to render all user incomes"""

    model = Income
    template_name = 'incomes/history_incomes.html'
    context_object_name = 'incomes'


class IncomesStatisticPageView(StatisticPageGenericView):
    """View to return statistic with user incomes for the month"""

    model = Income
    cost_model = Cost
    template_name = 'incomes/incomes_statistic.html'
    context_object_name = 'incomes'

    def get_context_data(
            self, request: HttpRequest, date: datetime.date) -> dict:
        """Return context with costs"""
        context = super().get_context_data(request, date)
        costs = services_common.get_all_user_entries(
            self.cost_model, request.user
        )
        context.update({'costs': costs})
        return context
