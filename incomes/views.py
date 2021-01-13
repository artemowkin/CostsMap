from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import IncomeForm
from .services.commands import GetIncomesStatisticCommand
from incomes.services import (
    GetIncomesForTheDateService, GetIncomesTotalSumService, GetIncomesService,
    DeleteIncomeService, CreateIncomeService, ChangeIncomeService,
)
from utils.views import (
    DateGenericView, HistoryGenericView, StatisticPageGenericView,
    DeleteGenericView, DefaultView
)


class IncomesForTheDateView(DateGenericView):
    """View to render user incomes for the date"""

    template_name = 'incomes/incomes.html'
    context_object_name = 'incomes'
    date_service = GetIncomesForTheDateService
    total_sum_service = GetIncomesTotalSumService


class CreateIncomeView(DefaultView):
    """View to create a new income"""

    form_class = IncomeForm
    template_name = 'incomes/add_income.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.cleaned_data.update({'owner': request.user})
            income = CreateIncomeService.execute(form.cleaned_data)
            return redirect(income.get_absolute_url())

        return render(request, self.template_name, {'form': form})


class ChangeIncomeView(DefaultView):
    """View to change an income"""

    form_class = IncomeForm
    template_name = 'incomes/change_income.html'

    def get(self, request, pk):
        income = GetIncomesService.get_concrete(pk, request.user)
        form = self.form_class(instance=income)
        return render(
            request, self.template_name, {'form': form, 'income': income}
        )

    def post(self, request, pk):
        income = GetIncomesService.get_concrete(pk, request.user)
        form = self.form_class(request.POST, instance=income)
        if form.is_valid():
            form.cleaned_data.update({'income': income})
            income = ChangeIncomeService.execute(form.cleaned_data)
            return redirect(income.get_absolute_url())

        return render(
            request, self.template_name, {'form': form, 'income': income}
        )


class DeleteIncomeView(DeleteGenericView):
    """View to delete an income"""

    template_name = 'incomes/delete_income.html'
    context_object_name = 'income'
    success_url = reverse_lazy('today_incomes')
    get_service = GetIncomesService
    delete_service = DeleteIncomeService


class IncomesHistoryView(HistoryGenericView):
    """View to render all user incomes"""

    template_name = 'incomes/history_incomes.html'
    context_object_name = 'incomes'
    get_service = GetIncomesService
    total_sum_service = GetIncomesTotalSumService


class IncomesStatisticPageView(StatisticPageGenericView):
    """View to return statistic with user incomes for the month"""

    template_name = 'incomes/incomes_statistic.html'
    command = GetIncomesStatisticCommand
