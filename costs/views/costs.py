from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy

from ..forms import CostForm
from ..services.commands import GetCostsStatisticCommand
from costs.services import (
    GetCostsForTheDateService, GetCostsTotalSumService, GetCostsService,
    CreateCostService, ChangeCostService, DeleteCostService,
    GetStatisticForTheMonthService, GetStatisticForTheYearService
)
from costs.services.categories import (
    GetCategoriesService, set_form_categories
)
from utils.views import (
    StatisticPageGenericView, DefaultView, DateGenericView,
    HistoryGenericView, DeleteGenericView
)


class CostsForTheDateView(DateGenericView):
    """View to render costs for the date"""

    template_name = 'costs/costs.html'
    context_object_name = 'costs'
    date_service = GetCostsForTheDateService
    total_sum_service = GetCostsTotalSumService


class CostsHistoryView(HistoryGenericView):
    """View to render all costs for all time."""

    template_name = 'costs/history_costs.html'
    context_object_name = 'costs'
    get_service = GetCostsService
    total_sum_service = GetCostsTotalSumService


class CreateCostView(DefaultView):
    """View to create a new cost"""

    form_class = CostForm
    template_name = 'costs/add_cost.html'

    def get(self, request):
        form = self.form_class()
        user_categories = GetCategoriesService.get_all(request.user)
        set_form_categories(form, user_categories)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        user_categories = GetCategoriesService.get_all(request.user)
        set_form_categories(form, user_categories)
        if form.is_valid():
            form.cleaned_data.update({'owner': request.user})
            cost = CreateCostService.execute(form.cleaned_data)
            return redirect(cost.get_absolute_url())

        return render(request, self.template_name, {'form': form})


class ChangeCostView(DefaultView):
    """View to change a cost"""

    form_class = CostForm
    template_name = 'costs/change_cost.html'

    def get(self, request, pk):
        cost = GetCostsService.get_concrete(pk, request.user)
        form = self.form_class(instance=cost)
        user_categories = GetCategoriesService.get_all(request.user)
        set_form_categories(form, user_categories)
        return render(
            request, self.template_name, {'form': form, 'cost': cost}
        )

    def post(self, request, pk):
        cost = GetCostsService.get_concrete(pk, request.user)
        form = self.form_class(request.POST, instance=cost)
        user_categories = GetCategoriesService.get_all(request.user)
        set_form_categories(form, user_categories)
        if form.is_valid():
            form.cleaned_data.update({'cost': cost})
            cost = ChangeCostService.execute(form.cleaned_data)
            return redirect(cost.get_absolute_url())

        return render(
            request, self.template_name, {'form': form, 'cost': cost}
        )


class DeleteCostView(DeleteGenericView):
    """View to delete a cost"""

    template_name = 'costs/delete_cost.html'
    success_url = reverse_lazy('today_costs')
    context_object_name = 'cost'
    get_service = GetCostsService
    delete_service = DeleteCostService


class StatisticView(DefaultView):
    """View to return json with costs statistic"""

    def get(self, request, date):
        data = GetStatisticForTheMonthService.execute({
            'user': request.user,
            'date': date
        })
        return JsonResponse(data, safe=False)


class CostsStatisticPageView(StatisticPageGenericView):
    """View to render statistic with costs for the month"""

    template_name = 'costs/costs_statistic.html'
    command = GetCostsStatisticCommand


class CostStatisticForTheLastYear(DefaultView):
    """View to return json statistic with costs by months
    for the last year
    """

    def get(self, request, date):
        data = GetStatisticForTheYearService.execute({
            'user': request.user,
            'date': date
        })
        return JsonResponse(data, safe=False)
