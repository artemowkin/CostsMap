from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render, redirect

from costs.services.costs import CostService
from .forms import IncomeForm
from .services import IncomeService
from .services.commands import GetIncomesStatisticCommand
from utils.views import (
    DateGenericView, HistoryGenericView, StatisticPageGenericView
)


class IncomesForTheDateView(DateGenericView):
    """View to render user incomes for the date"""

    service = IncomeService()
    template_name = 'incomes/incomes.html'
    context_object_name = 'incomes'


class CreateIncomeView(LoginRequiredMixin, View):
    """View to create a new income"""

    form_class = IncomeForm
    template_name = 'incomes/add_income.html'
    login_url = reverse_lazy('account_login')
    service = IncomeService()

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            income = self.service.create(form.cleaned_data, request.user)
            return redirect(income.get_absolute_url())

        return render(request, self.template_name, {'form': form})


class ChangeIncomeView(LoginRequiredMixin, View):
    """View to change an income"""

    service = IncomeService()
    form_class = IncomeForm
    template_name = 'incomes/change_income.html'
    login_url = reverse_lazy('account_login')

    def get(self, request, pk):
        income = self.service.get_concrete(pk, request.user)
        form = self.form_class(instance=income)
        return render(
            request, self.template_name, {'form': form, 'income': income}
        )

    def post(self, request, pk):
        income = self.service.get_concrete(pk, request.user)
        form = self.form_class(request.POST, instance=income)
        if form.is_valid():
            income = self.service.change(income, form)
            return redirect(income.get_absolute_url())

        return render(
            request, self.template_name, {'form': form, 'income': income}
        )


class DeleteIncomeView(LoginRequiredMixin, View):
    """View to delete an income"""

    template_name = 'incomes/delete_income.html'
    success_url = reverse_lazy('today_incomes')
    login_url = reverse_lazy('account_login')
    service = IncomeService()

    def get(self, request, pk):
        income = self.service.get_concrete(pk, request.user)
        return render(request, self.template_name, {'income': income})

    def post(self, request, pk):
        income = self.service.get_concrete(pk, request.user)
        self.service.delete(income)
        return redirect(self.success_url)


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
