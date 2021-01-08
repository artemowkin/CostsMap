from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy

from ..forms import CostForm
from ..services.categories import CategoryService
from ..services import CostService
from ..services.commands import GetCostsStatisticCommand
from incomes.services import IncomeService
from utils.views import (
    DateGenericView, HistoryGenericView, StatisticPageGenericView,
    DeleteGenericView, DefaultView
)


class CostsForTheDateView(DateGenericView):
    """View to render costs for the date"""

    service = CostService()
    template_name = 'costs/costs.html'
    context_object_name = 'costs'


class CostsHistoryView(HistoryGenericView):
    """View to render all costs for all time."""

    service = CostService()
    template_name = 'costs/history_costs.html'
    context_object_name = 'costs'


class CreateCostView(DefaultView):
    """View to create a new cost"""

    form_class = CostForm
    template_name = 'costs/add_cost.html'
    service = CostService()
    category_service = CategoryService()

    def get(self, request):
        form = self.form_class()
        self.category_service.set_form_user_categories(form, request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        self.category_service.set_form_user_categories(form, request.user)
        if form.is_valid():
            cost = self.service.create(form.cleaned_data, request.user)
            return redirect(cost.get_absolute_url())

        return render(request, self.template_name, {'form': form})


class ChangeCostView(DefaultView):
    """View to change a cost"""

    service = CostService()
    category_service = CategoryService()
    form_class = CostForm
    template_name = 'costs/change_cost.html'

    def get(self, request, pk):
        cost = self.service.get_concrete(pk, request.user)
        form = self.form_class(instance=cost)
        self.category_service.set_form_user_categories(form, request.user)
        return render(
            request, self.template_name, {'form': form, 'cost': cost}
        )

    def post(self, request, pk):
        cost = self.service.get_concrete(pk, request.user)
        form = self.form_class(request.POST, instance=cost)
        self.category_service.set_form_user_categories(form, request.user)
        if form.is_valid():
            cost = self.service.change(cost, form)
            return redirect(cost.get_absolute_url())

        return render(
            request, self.template_name, {'form': form, 'cost': cost}
        )


class DeleteCostView(DeleteGenericView):
    """View to delete a cost"""

    template_name = 'costs/delete_cost.html'
    success_url = reverse_lazy('today_costs')
    service = CostService()
    context_object_name = 'cost'


class StatisticView(DefaultView):
    """View to return json with costs statistic"""

    service = CostService()

    def get(self, request, date):
        data = self.service.get_statistic_for_the_month(request.user, date)
        return JsonResponse(data, safe=False)


class CostsStatisticPageView(StatisticPageGenericView):
    """View to render statistic with costs for the month"""

    template_name = 'costs/costs_statistic.html'
    cost_service = CostService()
    income_service = IncomeService()
    command = GetCostsStatisticCommand


class CostStatisticForTheLastYear(DefaultView):
    """View to return json statistic with costs by months
    for the last year
    """

    service = CostService()

    def get(self, request, date):
        data = self.service.get_statistic_for_the_year(request.user, date)
        return JsonResponse(data, safe=False)
