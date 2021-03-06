from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import IncomeForm
from .services.commands import (
    GetIncomesStatisticCommand, GetIncomesForTheDateCommand,
    GetIncomesHistoryCommand
)
from incomes.services import (
    GetIncomesForTheDateService, GetIncomesTotalSumService, GetIncomesService,
    DeleteIncomeService, CreateIncomeService, ChangeIncomeService,
)
from utils.views import (
    StatisticPageGenericView, DateGenericView, HistoryGenericView,
    DeleteGenericView, DefaultView
)


class IncomesForTheDateView(DateGenericView):
    """View to render user incomes for the date"""

    template_name = 'incomes/incomes.html'
    context_object_name = 'incomes'
    command = GetIncomesForTheDateCommand


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
            return self.form_valid(request, form)

        return render(request, self.template_name, {'form': form})

    def form_valid(self, request, form):
        form.cleaned_data.update({'owner': request.user})
        income = CreateIncomeService.execute(form.cleaned_data)
        return redirect(income.get_absolute_url())


class ChangeIncomeView(DefaultView):
    """View to change an income"""

    form_class = IncomeForm
    template_name = 'incomes/change_income.html'

    def get(self, request, pk):
        get_service = GetIncomesService(request.user)
        income = get_service.get_concrete(pk)
        form = self.form_class(instance=income)
        return render(
            request, self.template_name, {'form': form, 'income': income}
        )

    def post(self, request, pk):
        get_service = GetIncomesService(request.user)
        self.income = get_service.get_concrete(pk)
        form = self.form_class(request.POST, instance=self.income)
        if form.is_valid():
            return self.form_valid(request, form)

        return render(
            request, self.template_name, {'form': form, 'income': self.income}
        )

    def form_valid(self, request, form):
        form.cleaned_data.update({'income': self.income})
        income = ChangeIncomeService.execute(form.cleaned_data)
        return redirect(income.get_absolute_url())


class DeleteIncomeView(DeleteGenericView):
    """View to delete an income"""

    template_name = 'incomes/delete_income.html'
    context_object_name = 'income'
    success_url = reverse_lazy('today_incomes')
    get_service_class = GetIncomesService
    delete_service = DeleteIncomeService


class IncomesHistoryView(HistoryGenericView):
    """View to render all user incomes"""

    template_name = 'incomes/history_incomes.html'
    context_object_name = 'incomes'
    command = GetIncomesHistoryCommand


class IncomesStatisticPageView(StatisticPageGenericView):
    """View to return statistic with user incomes for the month"""

    template_name = 'incomes/incomes_statistic.html'
    command = GetIncomesStatisticCommand
